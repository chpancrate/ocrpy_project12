from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import jwt
import os

from models.user_dal_functions import get_user_by_email
from db import DB_RECORD_NOT_FOUND

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_DELAY = int(os.getenv("ACCESS_TOKEN_DELAY"))
REFRESH_TOKEN_DELAY = int(os.getenv("REFRESH_TOKEN_DELAY"))

INVALID_TOKEN = "Invalid token"
INVALID_PASSWORD = "Invalid password"

JSON_TOKEN_DIRNAME = "tokens/"
JSON_TOKEN_FILENAME = JSON_TOKEN_DIRNAME + 'tokens.json'


class AuthenticationManager():

    def create_tokens(self, user_id):
        """ create access token and refresh token for a user
        param :
        user_id
        return: dictionnary with keys
        'access': token with short lifetime for ressource access
        'refresh': token with longer lifetime to get new acces token
        """

        access_payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DELAY)
            }

        access_token = jwt.encode(payload=access_payload,
                                  key=SECRET_KEY,
                                  algorithm="HS256")

        refresh_payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_DELAY)
            }

        refresh_token = jwt.encode(payload=refresh_payload,
                                   key=SECRET_KEY,
                                   algorithm="HS256")

        result = {
            'access': access_token,
            'refresh': refresh_token
            }
        return result

    def password_authentication(self, email, password):
        """ check if password and email match
        create access token and refresh token for the user
        param :
        email
        password
        return: dictionnary with keys
        'status': ok or ko
        'access': token with short lifetime for ressource access (if status ok)
        'refresh': token with longer lifetime to get new acces token
                   (if status ok)
        'error': error (if status ko)
        """
        get_user_result = get_user_by_email(email)

        if get_user_result['status'] == 'ok':
            user = get_user_result['user']
            if user.is_password_correct(password):
                tokens = self.create_tokens(user.id)
                result = tokens
                result['status'] = "ok"
            else:
                result = {}
                result['status'] = 'ko'
                result['error'] = INVALID_PASSWORD
        else:
            result = {}
            result['status'] = 'ko'
            result['error'] = DB_RECORD_NOT_FOUND

        return result

    def request_token_with_refresh(self, refresh_token):
        """ check refresh token and create access and refresh token
         for the user
        in token
        param :
        refresh_token
        return: dictionnary with keys
        'status': ok or ko
        'access': token with short lifetime for ressource access (if status ok)
        'refresh': token with longer lifetime to get new acces token
                  (if status ok)
        'error': error (if status ko)
        """

        try:
            decoded_token = jwt.decode(jwt=refresh_token,
                                       key=SECRET_KEY,
                                       algorithms=["HS256"])

            if decoded_token['type'] == 'refresh':
                # if the token is a valid refresh token
                # create an access and refresh tokens
                user_id = decoded_token['user_id']
                tokens = self.create_tokens(user_id)
                result = tokens
                result['status'] = 'ok'
            else:
                # if not a refresh token raise error
                result = {}
                result['status'] = 'ko'
                result['error'] = INVALID_TOKEN
        except jwt.ExpiredSignatureError:
            result = {}
            result['status'] = 'ko'
            result['error'] = INVALID_TOKEN

        return result

    def check_token(self, token):
        """ check token and extract data from payload
        param :
        token : an access or refresh token
        return: dictionnary with keys
        'status': ok or ko
        'user_id': user id stored in token (if status ok)
        'error': error (if status ko)
        """
        result = {}
        result['status'] = 'ok'
        try:
            decoded_token = jwt.decode(jwt=token,
                                       key=SECRET_KEY,
                                       algorithms=["HS256"])

            if decoded_token['type'] in ['access', 'refresh']:
                # if the token is valid access token retrieve data in payload
                result['user_id'] = decoded_token['user_id']
            else:
                # if not return error
                result['status'] = 'ko'
                result['error'] = INVALID_TOKEN
        except jwt.ExpiredSignatureError:
            # if token expired return error
            result['status'] = 'ko'
            result['error'] = INVALID_TOKEN

        return result

    def save_tokens_to_file(self, tokens):
        """ save the token passed to a tokens.json file"""
        if not os.path.exists(JSON_TOKEN_DIRNAME):
            os.makedirs(JSON_TOKEN_DIRNAME)

        with open(JSON_TOKEN_FILENAME, "w") as file_json:
            json.dump(tokens, file_json)

    def get_tokens_from_file(self):
        """ get the tokens from the tokens.json file"""
        with open(JSON_TOKEN_FILENAME, "r") as file_json:
            tokens = json.load(file_json)

        return tokens
