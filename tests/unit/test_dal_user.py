from argon2 import PasswordHasher
from sqlalchemy.orm import sessionmaker

from models.user_models import User
from models.client_models import Client
import models.user_dal_functions as dal
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


class TestDalUser():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_user(self, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_user using the dictionnary
        THEN the user is created in the database
             and the status and user.id are returned
        """
        result = dal.create_user(user_fix)

        assert result['status'] == "ok"

        self.session.commit()
        ValueStorage.user_id = result['user_id']
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user.email == user_fix['email']

    def test_create_user_with_error(self, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_user using the dictionnary
             and an error occured
        THEN the user is not created in the database
             and the status ko and the error are returned
        """
        # recreate user from previous test gives an error
        result = dal.create_user(user_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_user(self, user_fix):
        """
        GIVEN a user and a dictionnary of data
        WHEN you call dal.upadate_user using the dictionnary
        THEN the user is updated in the database
             and the status and user.id are returned
        """
        user_fix['id'] = ValueStorage.user_id
        new_name = user_fix['first_name'] + " mod"
        user_fix['first_name'] = new_name

        result = dal.update_user(user_fix)

        assert result['status'] == "ok"
        assert result['user_id'] == ValueStorage.user_id

        self.session.commit()
        user = (self.session.query(User)
                .filter(User.id == ValueStorage.user_id)
                .first())

        assert user.first_name == new_name

    def test_update_user_with_error(self, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_user using the dictionnary
             and an error occured
        THEN the user is not updated in the database
             and the status ko and the error are returned
        """
        # set a wrong id
        user_fix['id'] = 999

        result = dal.update_user(user_fix)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

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

        self.session.commit()
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
        assert result['error'] == DB_RECORD_NOT_FOUND

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

        self.session.commit()
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
        assert result['error'] == DB_RECORD_NOT_FOUND

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

        self.session.commit()
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
        assert result['error'] == DB_RECORD_NOT_FOUND

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
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_user_by_email(self, user_fix):
        """
        GIVEN an existing user email
        WHEN you call get_user_by_email with the user id
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                    .filter(User.email == user_fix['email'])
                    .first())

        result = dal.get_user_by_email(user_fix['email'])

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
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_user_by_employee_id(self, user_fix):
        """
        GIVEN an existing user employee_number
        WHEN you call get_user_by_employee_id with the user employee_number
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                .filter(User.employee_number == user_fix['employee_number'])
                .first())

        result = dal.get_user_by_employee_id(user_fix['employee_number'])

        assert result['status'] == "ok"

        assert result['user'].id == user.id
        assert result['user'].first_name == user.first_name
        assert result['user'].last_name == user.last_name

    def test_get_user_by_employee_id_with_error(self):
        """
        GIVEN a user employee number
        WHEN you call get_user_by_employee_id with the user employee_number
             and an error occured
        THEN the status ko is returned with the error
        """
        # set a wrong id
        employee_number = 999

        result = dal.get_user_by_employee_id(employee_number)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_all_users(self, user_fix):
        """
        GIVEN
        WHEN you call get_all_users with the user employee_number
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        result = dal.get_all_users()

        assert result['status'] == "ok"

        assert result['users'][0].id == user.id
        assert result['users'][0].first_name == user.first_name
        assert result['users'][0].last_name == user.last_name

    def test_get_client_list_for_user(self, client_fix):
        """
        GIVEN an existing user employee_number
        WHEN you call get_user_by_employee_id with the user employee_number
        THEN the status ok is returned with the user object
        """
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        client = Client(first_name=client_fix['first_name'],
                        last_name=client_fix['last_name'],
                        email=client_fix['email'],
                        telephone=client_fix['telephone'],
                        enterprise=client_fix['enterprise'],
                        commercial_contact_id=user.id,
                        active=client_fix['active'],
                        )

        self.session.add(client)
        self.session.commit()
        ValueStorage.client_id = client.id

        result = dal.get_client_list_for_user(user.id)

        assert result['status'] == "ok"

        assert result['data'][0].id == client.id
        assert result['data'][0].first_name == client.first_name
        assert result['data'][0].last_name == client.last_name

    def test_delete_user(self):
        """
        GIVEN an existing user id
        WHEN you call delete_user with the user id
        THEN the user is deleted in database and the status ok is returned
        """
        # remove client added in last test from user
        affected_rows = (self.session.query(Client)
                         .filter(Client.id == ValueStorage.client_id)
                         .delete())

        assert affected_rows == 1
        self.session.commit()

        # check user exist
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user

        result = dal.delete_user(ValueStorage.user_id)

        assert result['status'] == "ok"
        assert result['user_id'] == ValueStorage.user_id

        self.session.commit()

        # check user deleted
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user is None

    def test_delete_user_with_error(self):
        """
        GIVEN an existing user id
        WHEN you call delete_user with the user id
             and an error occured
        THEN the status ko is returned with the error
        """
        user_id = 999

        result = dal.delete_user(user_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND
