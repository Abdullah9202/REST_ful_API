# RESTful API Description

This is a RESTful API built using Python Flask and Flask-SQLAlchemy. It provides endpoints for performing CRUD (Create, Read, Update, Delete) operations on a local SQL database. The API supports HTTP methods such as GET, PUT, PATCH, and DELETE.

## Features

* GET: Retrieve data from the database.
* POST: Create a new record in the database.
* PUT: Replace the record in the database.
* PATCH: Update an existing record in the database.
* DELETE: Remove a record from the database.

## Technologies Used

* Flask: Python web framework for building the API endpoints.
* Flask-SQLAlchemy: Flask extension for working with SQL databases.
* SQLite: Local database used for storing data.

## Endpoints

* GET /random: Retrieve a random cafe record from the database.
* GET /all: Retrieve all cafe records from the database.
* GET /search: Search for cafe records based on location.
* POST /add: Add a new cafe record to the database.
* PATCH /update-price/{cafe_id}: Update the price of a cafe record in the database.
* DELETE /delete-cafe/{cafe_id}: Delete a cafe record from the database.

## Error Handling

* If a requested resource is not found, a 404 Not Found error is returned.
* If there is a server error, a 500 Internal Server Error is returned.
* Unauthorized access is handled with a 401 Unauthorized error.
* Method Not Allowed error (405) is returned if an unsupported HTTP method is used.

## Server Configuration

The API is hosted locally on the Flask development server with the following configuration:

* Host: 127.0.0.1
* Port: 5000

## Known Issues

* Currently, the API is not using CSRF (Cross Site Request Forgery) Protection but it will be added soon.
* Error handling could be improved to provide more informative error messages.

Overall, this RESTful API provides basic CRUD functionality for managing cafe records in a local SQL database.

## Important Note

API Key is in the text file named api_key.txt that is located in API directory.
