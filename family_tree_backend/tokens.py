#!/usr/bin/env python3

import jwt

def inspect_jwt(token):
    try:
        # Decode the JWT without verifying the signature (verify=False).
        # In a production environment, you should set verify=True and provide the correct key or public key.
        decoded_token = jwt.decode(token, verify=False)

        # Extract information from the decoded token
        user_id = decoded_token.get("user_id")
        expiration_time = decoded_token.get("exp")

        # Print or use the extracted information as needed
        print("User ID:", user_id)
        print("Token expiration time:", expiration_time)

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")

        # Replace "your_jwt_token_here" with the actual JWT you want to inspect
jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im5vZGhpYW1ibzAxQGdtYWlsLmNvbSIsImV4cCI6MTcwMDEzMjA2NCwiZW1haWwiOiJub2RoaWFtYm8wMUBnbWFpbC5jb20ifQ.siLDXB1OrK7J6kfz2OR_sCzZi12b7Nyq-JW6GYWM0QM"
inspect_jwt(jwt_token)

