from argon2 import PasswordHasher
from sqlalchemy.orm import sessionmaker

from models.user_models import User
import models.user_dal_functions as dal
from db import engine, Base
from ..conftest import ValueStorage


class TestDalUser():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        Base.metadata.drop_all(engine)
        self.session.close()

    def test_create_user(self, user1_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_user using the dictionnary
        THEN the user is created in the database
             and the status and user.id are returned
        """
        result = dal.create_user(user1_fix)

        assert result['status'] == "ok"

        ValueStorage.user_id = result['user_id']
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user.email == "test1@email.com"

    def test_create_user_with_error(self, user1_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_user using the dictionnary
             and an error occured
        THEN the user is not created in the database
             and the status ko and the error are returned
        """
        # recreate user from previous test gives an error
        result = dal.create_user(user1_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_user(self, user1_fix):
        """
        GIVEN a user and a dictionnary of data
        WHEN you call dal.upadate_user using the dictionnary
        THEN the user is updatede in the database
             and the status and user.id are returned
        """
        """
        user = User(employee_number=user2_fix['employee_number'],
                    first_name=user2_fix['first_name'],
                    last_name=user2_fix['last_name'],
                    email=user2_fix['email'],
                    password=user2_fix['password'])

        self.session.add(user)
        self.session.commit()
        """
        user1_fix['id'] = ValueStorage.user_id
        user1_fix['first_name'] = "firstname 1 mod"

        result = dal.update_user(user1_fix)

        assert result['status'] == "ok"
        assert result['user_id'] == ValueStorage.user_id

        user = (self.session.query(User)
                .filter(User.id == ValueStorage.user_id)
                .first())

        assert user.first_name == "firstname 1 mod"

    def test_update_user_with_error(self, user1_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_user using the dictionnary
             and an error occured
        THEN the user is not updated in the database
             and the status ko and the error are returned
        """
        # set a wrong id
        user1_fix['id'] = 999

        result = dal.update_user(user1_fix)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND

    def test_deactivate_user(self):
        """
        GIVEN a user
        WHEN you call deactivate_user with the user id
        THEN the user active filed is set to False in the database
        and the status and user.id are returned
        """

        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user.active is True

        result = dal.deactivate_user(user.id)

        assert result['status'] == "ok"
        assert result['user_id'] == user.id

        self.session.refresh(user)

        assert user.active is False

    def test_deactivate_user_with_error(self):
        """
        GIVEN a user id
        WHEN you call deactivate_user with the user id
             and an error occurred
        THEN the status ko is returned and an error
        """
        # set a wrong id
        user_id = 999

        result = dal.deactivate_user(user_id)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND

    def test_activate_user(self):
        """
        GIVEN a user
        WHEN you call activate_user with the user id
        THEN the user active field is set to True in the database
        and the status and user.id are returned
        """

        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user.active is False

        result = dal.activate_user(user.id)

        assert result['status'] == "ok"
        assert result['user_id'] == user.id

        self.session.refresh(user)

        assert user.active is True

    def test_activate_user_with_error(self):
        """
        GIVEN a user id
        WHEN you call activate_user with the user id
             and an error occurred
        THEN the status ko is returned and an error
        """
        # set a wrong id
        user_id = 999

        result = dal.activate_user(user_id)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND

    def test_update_user_password(self):
        """
        GIVEN an existing user and a new password
        WHEN you call update_user_password
        THEN the password is updated
             and the status ok is returned with the user_id
        """
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        user_dict = {
            'id': user.id,
            'password': 'newpassword'
        }

        result = dal.update_user_password(user_dict)

        assert result['status'] == "ok"
        assert result['user_id'] == user.id

        self.session.refresh(user)

        ph = PasswordHasher()
        assert ph.verify(user.password, 'newpassword')

    def test_update_user_password_with_error(self):
        """
        GIVEN an existing user and a new password
        WHEN you call update_user_password and an error occured
        THEN the status ko is returned with the error
        """
        # set a wrong id
        user_dict = {
            'id': 999,
            'password': 'newpassword'
        }

        result = dal.update_user_password(user_dict)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND

    def test_get_user_by_id(self):
        """
        GIVEN an existing user id
        WHEN you call get_user_by_id with the user id
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        result = dal.get_user_by_id(ValueStorage.user_id)

        assert result['status'] == "ok"

        assert result['user'].id == user.id
        assert result['user'].first_name == user.first_name
        assert result['user'].last_name == user.last_name

    def test_get_user_by_id_with_error(self):
        """
        GIVEN a user id
        WHEN you call get_user_by_id with the user id and an error occured
        THEN the status ko is returned with the error
        """
        # set a wrong id
        user_id = 999

        result = dal.get_user_by_id(user_id)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND

    def test_get_user_by_email(self, user1_fix):
        """
        GIVEN an existing user email
        WHEN you call get_user_by_email with the user id
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                    .filter(User.email == user1_fix['email'])
                    .first())

        result = dal.get_user_by_email(user1_fix['email'])

        assert result['status'] == "ok"

        assert result['user'].id == user.id
        assert result['user'].first_name == user.first_name
        assert result['user'].last_name == user.last_name

    def test_get_user_by_email_with_error(self):
        """
        GIVEN a user id
        WHEN you call get_user_by_id with the user id and an error occured
        THEN the status ko is returned with the error
        """
        # set a wrong id
        email = 'wrong@email.com'

        result = dal.get_user_by_email(email)

        assert result['status'] == "ko"
        assert result['error'] == dal.MSG_RECORD_NOT_FOUND
