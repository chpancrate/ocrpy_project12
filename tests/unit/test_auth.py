from dotenv import load_dotenv
import jwt
import os

import authentication.auth_functions as auth

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class TestAuthentication():

    def setup_class(cls):
        pass

    def teardown_class(self):
        pass

    def test_create_tokens(self):
        """
        GIVEN a user id
        WHEN you call create_token using the id
        THEN two token are return with the correct payload
        """

    user_id = 2

    result = auth.create_tokens(user_id)

    acces_token = result['access']
    refresh_token = result['refresh']

    decoded_acces_token = jwt.decode(jwt=acces_token,
                                     key=SECRET_KEY,
                                     algorithms=["HS256"])

    assert decoded_acces_token['user_id'] == user_id

    decoded_refresh_token = jwt.decode(jwt=refresh_token,
                                       key=SECRET_KEY,
                                       algorithms=["HS256"])

    assert decoded_refresh_token['user_id'] == user_id
