from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os
from sqlalchemy.orm import sessionmaker

from ..conftest import ValueStorage

from authentication.auth_models import (AuthenticationManager,
                                        INVALID_TOKEN,
                                        INVALID_PASSWORD)
from db import engine, Base
from models.user_dal_functions import (create_user,
                                       get_user_by_id)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


class TestAuthentication():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()
        cls.auth = AuthenticationManager()

    def teardown_class(self):
        Base.metadata.drop_all(engine)
        self.session.close()
        pass

    def test_create_tokens(self):
        """
        GIVEN a user id
        WHEN you call create_token using the id
        THEN two token are return with the correct payload
        """

        user_id = 2

        result = self.auth.create_tokens(user_id)

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

    def test_password_authentication(self, user_fix):
        """
        GIVEN an email and a correct password
        WHEN you call password_authentication
        THEN two token are returned with the correct payload
        """
        result = create_user(user_fix)
        ValueStorage.user_id = result['user_id']

        email = user_fix['email']
        password = user_fix['password']

        result = self.auth.password_authentication(email, password)

        assert result['status'] == "ok"

        decoded_access_token = jwt.decode(
            jwt=result['access'],
            key=SECRET_KEY,
            algorithms=["HS256"]
            )
        assert decoded_access_token['type'] == 'access'
        assert decoded_access_token['user_id'] == ValueStorage.user_id

        decoded_refresh_token = jwt.decode(
            jwt=result['refresh'],
            key=SECRET_KEY,
            algorithms=["HS256"]
            )
        assert decoded_refresh_token['type'] == 'refresh'
        assert decoded_refresh_token['user_id'] == ValueStorage.user_id

    def test_password_authentication_with_wrong_password(self):
        """
        GIVEN an email and an incorrect password
        WHEN you call password_authentication
        THEN the status ko and the error are returned
        """
        result = get_user_by_id(ValueStorage.user_id)

        email = result['user'].email
        password = 'wrong_password'

        result = self.auth.password_authentication(email, password)

        assert result['status'] == "ko"
        assert result['error'] == INVALID_PASSWORD

    def test_request_token_with_refresh(self):
        """
        GIVEN a refresh_token
        WHEN you call request_token_with_refresh
        THEN a new access token is returned
        """
        user_id = 2

        result = self.auth.create_tokens(user_id)

        refresh_token = result['refresh']

        result = self.auth.request_token_with_refresh(refresh_token)

        assert result['status'] == 'ok'

        decoded_access_token = jwt.decode(
            jwt=result['access'],
            key=SECRET_KEY,
            algorithms=["HS256"]
            )
        assert decoded_access_token['type'] == 'access'
        assert decoded_access_token['user_id'] == user_id

        decoded_refresh_token = jwt.decode(
            jwt=result['refresh'],
            key=SECRET_KEY,
            algorithms=["HS256"]
            )
        assert decoded_refresh_token['type'] == 'refresh'
        assert decoded_refresh_token['user_id'] == user_id

    def test_request_token_with_refresh_with_access_token(self):
        """
        GIVEN an acces_token
        WHEN you call request_token_with_refresh
        THEN the status ko and the error are returned
        """
        user_id = 2

        result = self.auth.create_tokens(user_id)

        refresh_token = result['access']

        result = self.auth.request_token_with_refresh(refresh_token)

        assert result['status'] == 'ko'
        assert result['error'] == INVALID_TOKEN

    def test_request_token_with_refresh_with_expired_token(self):
        """
        GIVEN an expired refresh_token
        WHEN you call request_token_with_refresh
        THEN the status ko and the error are returned
        """
        user_id = 2

        refresh_payload = {
            'user_id': user_id,
            'type': 'refresh',
            'exp': datetime.utcnow() - timedelta(minutes=5)
            }

        refresh_token = jwt.encode(payload=refresh_payload,
                                   key=SECRET_KEY,
                                   algorithm="HS256")

        result = self.auth.request_token_with_refresh(refresh_token)

        assert result['status'] == 'ko'
        assert result['error'] == INVALID_TOKEN

    def test_check_token(self):
        """
        GIVEN an access_token
        WHEN you call check_access_token
        THEN user_id from the token is returned
        """
        user_id = 2

        result = self.auth.create_tokens(user_id)

        access_token = result['access']

        result = self.auth.check_token(access_token)

        assert result['status'] == 'ok'
        assert result['user_id'] == user_id

    def test_check_token_with_expired_token(self):
        """
        GIVEN a refresh_token
        WHEN you call check_token
        THEN the status ko and the error are returned
        """
        user_id = 2

        access_payload = {
            'user_id': user_id,
            'type': 'access',
            'exp': datetime.utcnow() - timedelta(minutes=5)
            }

        access_token = jwt.encode(payload=access_payload,
                                  key=SECRET_KEY,
                                  algorithm="HS256")

        result = self.auth.check_token(access_token)

        assert result['status'] == 'ko'
        assert result['error'] == INVALID_TOKEN
