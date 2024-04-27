import secrets
import string


def generate_api_key(length=32):
    # Define the characters to choose from for the API key
    characters = string.ascii_letters + string.digits

    # Generate a random API key using the defined characters
    api_key = ''.join(secrets.choice(characters) for _ in range(length))

    return api_key


# Generate a random API key of length 32 characters
random_api_key = generate_api_key()
print("Random API Key:", random_api_key)
