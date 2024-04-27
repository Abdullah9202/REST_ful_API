from flask import Flask, jsonify, render_template, request, redirect, url_for
from sqlalchemy.orm.exc import NoResultFound
from flask_wtf.csrf import generate_csrf
from flask_wtf.csrf import CSRFProtect
import random
# My Files
from Class.cafe_temp import db, Cafe
from myfunction.myfunc import to_dict

# Init App
app = Flask(__name__, template_folder="templates")

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CSRF Token
# app.config['SECRET_KEY'] = 'R,,@8fer3fer345'
# app.config['WTF_CSRF_ENABLED'] = True

# Init CSRF Protection
# csrf = CSRFProtect(app)
# csrf.init_app(app)

# Init db with Flask App
db.init_app(app)


# Home Route
@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


# HTTP GET - Read Record
# Random Route
@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()  # Convert query object to list
    random_cafe = random.choice(all_cafes)
    # return jsonify(
    #     id=random_cafe.id,
    #     name=random_cafe.name,
    #     map_url=random_cafe.map_url,
    #     location=random_cafe.location,
    #     seats=random_cafe.seats,
    #     has_toilet=random_cafe.has_toilet,
    #     has_wifi=random_cafe.has_wifi,
    #     has_sockets=random_cafe.has_sockets,
    #     can_take_calls=random_cafe.can_take_calls,
    #     coffee_price=random_cafe.coffee_price
    # )

    # Using Dict Comp to jsonify
    return jsonify(cafe=to_dict(random_cafe)), 200


###############################################
# ==> Another Approach for Large DB
# Random Route
# @app.route("/random")
# def get_random_cafe():
#     # Getting the row number in DB
#     row_count = db.session.query(Cafe).count()
#     # Generating random number for skipping some records
#     rand_offset = random.randint(0, row_count - 1)
#     # Returning the first record after rand_offset
#     rand_cafe = db.session.query(rand_offset).first()
#     return render_template(template_name_or_list="random.html", cafe=rand_cafe)


# All Route
@app.route("/all")
def get_all_cafe():
    all_cafes = db.session.query(Cafe).all()  # Convert query object to list
    # Convert each cafe object to a dict and storing in list
    cafe_list = [to_dict(cafe) for cafe in all_cafes]
    return jsonify(cafes=cafe_list), 200


# Search Route
@app.route("/search")
def search_cafe():
    cafe_location = request.args.get('location')  # Get the value of the 'location' query parameter
    # Validation for 'loc' argument in URl
    if cafe_location is None:
        error_msg = {'error': 'Location parameter is missing'}
        return jsonify(error_msg), 400  # Returning error msg if 'location' argument was not found

    target_cafe = []  # List to hold the names of targeted cafes
    all_cafes = db.session.query(Cafe).all()  # Converting query objects to list
    
    # Iterating on DB
    for cafe in all_cafes:
        # Matching the cafe location with the location provided by user
        if cafe.location == cafe_location:
            # Appending in list
            target_cafe.append(to_dict(cafe))

    # Validation
    if target_cafe:
        return jsonify(cafes=target_cafe)
    else:
        error_msg = {'error': f'No cafe was found in {cafe_location}'}
        return jsonify(error_msg), 400  # Return with HTTP status code 400 (Bad Request) if cafe not found


# HTTP POST - Create Record
# Add Route
@app.route("/add", methods=["POST"])
def add_cafe():
    if request.method == "POST":
        try:
            new_cafe = Cafe(
                name=request.args.get('name'),
                location=request.args.get('location'),
                seats=request.args.get('seats'),
                img_url=request.args.get('img_url'),
                map_url=request.args.get('map_url'),
                coffee_price=request.args.get('coffee_price'),
                has_wifi=bool(request.args.get('has_wifi')),
                has_toilet=bool(request.args.get('has_toilet')),
                has_sockets=bool(request.args.get('has_sockets')),
                can_take_calls=bool(request.args.get('can_take_calls')),
            )
        except KeyError:
            return jsonify(error={"Bad Request": "One or all the keys are missing or invalid."}), 400
        else:
            try:
                with app.app_context():
                    db.session.add(new_cafe)
                    db.session.commit()
                return jsonify(success={"Success": "Successfully added the cafe in Database"}), 200
            except Exception as err:
                return jsonify(error={"Database error": str(err)}), 500
    else:
        return jsonify(error={"error": "Request Method Not Allowed."}), 405


# HTTP PUT/PATCH - Update Record
# Price Update Route
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    # Request Validation
    if request.method == "PATCH":
        # Counting the DB ids
        total_ids = db.session.query(Cafe).count()
        # Checking if the entered ID greater than DB ids
        if int(cafe_id) > total_ids:
            return jsonify(error={"Not Found": f"Sorry! The Cafe with {cafe_id} ID was not found in database."}), 404
        # Updating in DB
        try:
            target_cafe = db.session.query(Cafe).get(cafe_id)
        except NoResultFound:
            return jsonify(error={"Not Found": "Sorry! The requested cafe was not found in the database."}), 404
        else:
            target_cafe.coffee_price = request.args.get('coffee_price')
            db.session.commit()
            return jsonify(success={"Success": "Price updated successfully."}), 200
    else:
        return jsonify(error={"Method Error": "Request Method Not Allowed."}), 405


# Cafe Replace Route
@app.route("/replace-cafe/<int:cafe_id>", methods=["PUT"])
def replace_cafe(cafe_id):
    # Request Validation
    if request.method == "PUT":
        # Counting in DB ids
        total_ids = db.session.query(Cafe).count()
        # Checking if the entered ID is in DB
        if int(cafe_id) > total_ids or int(cafe_id) < 1 or not db.session.query(db.exists().where(Cafe.id == cafe_id)).scalar():
            return jsonify(error={"Not Found": f"Sorry! The Cafe with {cafe_id} ID was not found in database So, it cannot be replaced."}), 404
        
        # Getting the API Key from file
        try:
            api_file = open(file="API/api_key.txt")
        except FileNotFoundError:
            return jsonify(error={"Internal Error": "Sorry! API key file is not found in database."})
        else:
            api_key = api_file.read()
            api_file.close()
            
        # Validating the API key entered by user
        if api_key == request.args.get("api-key") or api_key == request.headers["api-key"]:
            # Updating the DB
            try:
                target_cafe = db.session.query(Cafe).get(cafe_id)
            except NoResultFound:
                return jsonify(error={"Not Found": f"Sorry! The cafe with ID {cafe_id} was not found in the database."}), 404
            else:
                # Taking the args and replacing with the previous data in DB
                try:
                    target_cafe.name = request.args.get("name")
                    target_cafe.location = request.args.get("location")
                    target_cafe.seats = request.args.get("seats")
                    target_cafe.img_url = request.args.get("img_url")
                    target_cafe.map_url = request.args.get("map_url")
                    target_cafe.coffee_price = request.args.get("coffee_price")
                    target_cafe.has_wifi = bool(request.args.get("has_wifi"))
                    target_cafe.has_toilet = bool(request.args.get("has_toilet"))
                    target_cafe.has_sockets = bool(request.args.get("has_sockets"))
                    target_cafe.can_take_calls = bool(request.args.get("can_take_calls"))
                except KeyError:
                    return jsonify(error={"Bad Request": "One or all the keys are missing or invalid."}), 400
                else:
                    db.session.commit()
                    return jsonify(success={"Success": "Cafe replaced successfully."}), 200
    else:
        return jsonify(error={"Method Error": "Request Method Not Allowed."}), 405


# HTTP DELETE - Delete Record
@app.route("/delete-cafe/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    # Request validation
    if request.method == "DELETE":
        # Counting the DB ids
        total_ids = db.session.query(Cafe).count()
        # Checking if the entered ID greater than DB ids
        if int(cafe_id) > total_ids or int(cafe_id) < 1 or not db.session.query(db.exists().where(Cafe.id == cafe_id)).scalar():
            return jsonify(error={"Not Found": f"Sorry! The Cafe with {cafe_id} ID was not found in database So, it cannot be deleted."}), 404
        
        # Getting the API key from the file
        try:
            api_file = open(file="API/api_key.txt", mode='r')
        except FileNotFoundError:
            return jsonify(error={"Internal Error": "Sorry! API key file is not found in database."})
        else:
            api_key = api_file.read()
            api_file.close()

        # Validating the API Key entered by user
        if api_key == request.args.get("api-key") or api_key == request.headers["api-key"]:
            # Updating the DB
            try:
                target_cafe = db.session.query(Cafe).get(cafe_id)
            except NoResultFound:
                return jsonify(error={"Not Found": f"Sorry! The cafe with ID {cafe_id} was not found in the database."}), 404
            else:
                db.session.delete(target_cafe)
                db.session.commit()
                return jsonify(success={"Success": f"Cafe with ID {cafe_id} has been deleted successfully."}), 200
        else:
            return jsonify(error={"Unauthorized": "Invalid API Key."}), 401

    else:
        return jsonify(error={"Method Error": "Request Method Not Allowed."}), 405


# Executing as script
if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
    