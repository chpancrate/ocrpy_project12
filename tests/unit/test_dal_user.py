from argon2 import PasswordHasher
from sqlalchemy.orm import sessionmaker

from models.user_models import User, Team, Role
import models.user_dal_functions as dal
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND,
                DB_TEAM_NOT_EMPTY
                )
from ..conftest import ValueStorage


class TestDalUser():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        Base.metadata.drop_all(engine)
        self.session.close()

    def test_create_user(self, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_user using the dictionnary
        THEN the user is created in the database
             and the status and user.id are returned
        """
        result = dal.create_user(user_fix)

        assert result['status'] == "ok"

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
        THEN the user is updatede in the database
             and the status and user.id are returned
        """
        user_fix['id'] = ValueStorage.user_id
        new_name = user_fix['first_name'] + " mod"
        user_fix['first_name'] = new_name

        result = dal.update_user(user_fix)

        assert result['status'] == "ok"
        assert result['user_id'] == ValueStorage.user_id

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

    def test_delete_user(self):
        """
        GIVEN an existing user id
        WHEN you call delete_user with the user id
        THEN the user is deleted in database and the status ok is returned
        """
        # check user exist
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())

        assert user

        result = dal.delete_user(ValueStorage.user_id)

        assert result['status'] == "ok"
        assert result['user_id'] == ValueStorage.user_id

        self.session.expire_all()

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


class TestDalTeam():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        Base.metadata.drop_all(engine)
        self.session.close()

    def test_create_team(self, team_fix, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_team using the dictionnary
        THEN the team is created in the database
             and the status and team.id are returned
        """
        role = Role(name=role_fix['name'],
                    active=role_fix['active']
                    )
        self.session.add(role)
        self.session.commit()
        ValueStorage.role_id = role.id

        team_fix['role_id'] = role.id

        result = dal.create_team(team_fix)

        assert result['status'] == "ok"

        ValueStorage.team_id = result['team_id']
        team = (self.session.query(Team)
                .filter(Team.id == ValueStorage.team_id)
                .first())

        assert team.name == team_fix['name']

    def test_create_team_with_error(self, team_fix, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_team using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        team_fix['role_id'] = ValueStorage.role_id

        result = dal.create_team(team_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_team(self, team_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_team using the dictionnary
        THEN the team is updated in the database
             and the status and team.id are returned
        """
        team_dict = {}
        team_dict['id'] = ValueStorage.team_id
        new_name = team_fix['name'] + " mod"
        team_dict['name'] = new_name

        result = dal.update_team(team_dict)

        assert result['status'] == "ok"
        assert result['team_id'] == ValueStorage.team_id

        team = (self.session.query(Team)
                .filter(Team.id == ValueStorage.team_id)
                .first())

        assert team.name == new_name

    def test_update_team_with_error(self, team_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_team using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        team_dict = {}
        team_dict['id'] = 999
        new_name = team_fix['name'] + " mod"
        team_dict['name'] = new_name

        result = dal.update_team(team_dict)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_deactivate_team(self):
        """
        GIVEN a team_id
        WHEN you call dal.deactivate_team using the id
        THEN the team is deactivated in the database
             and the status and team.id are returned
        """
        team = (self.session.query(Team)
                .filter(Team.id == ValueStorage.team_id)
                .first())
        assert team.active is True

        result = dal.deactivate_team(team.id)

        assert result['status'] == "ok"
        assert result['team_id'] == team.id

        self.session.refresh(team)

        assert team.active is False

    def test_deactivate_team_with_error(self):
        """
        GIVEN a team_id
        WHEN you call dal.deactivate_team using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        team_id = 999

        result = dal.deactivate_team(team_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_activate_team(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.activate_team using the id
        THEN the team is activated
             and the status and user.id are returned
        """
        team = (self.session.query(Team)
                .filter(Team.id == ValueStorage.team_id)
                .first())
        assert team.active is False

        result = dal.activate_team(team.id)

        assert result['status'] == "ok"
        assert result['team_id'] == team.id

        self.session.refresh(team)

        assert team.active is True

    def test_activate_team_with_error(self):
        """
        GIVEN a team_id
        WHEN you call dal.activate_team using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        team_id = 999

        result = dal.activate_team(team_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_team_by_id(self):
        """
        GIVEN a team_id
        WHEN you call dal.get_team_by_id using the id
        THEN the status and team are returned
        """
        team = (self.session.query(Team)
                .filter(Team.id == ValueStorage.team_id)
                .first())

        result = dal.get_team_by_id(ValueStorage.team_id)

        assert result['status'] == "ok"

        assert result['team'].id == team.id
        assert result['team'].name == team.name

    def test_get_team_by_id_with_error(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.get_team_by_id using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        team_id = 999

        result = dal.get_team_by_id(team_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_delete_team_with_user(self, user_fix):
        """
        GIVEN a team id
        WHEN you call dal.delete_team using the id
             and a user uses the team
        THEN the team is not deleted
             the status ko is returned
             the error team not empty is returned
        """
        # Create user
        result = dal.create_user(user_fix)

        # check team exist
        team = (self.session.query(Team)
                    .filter(Team.id == ValueStorage.team_id)
                    .first())

        assert team

        # add user to team
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())
        user.team_id = team.id

        self.session.commit()

        result = dal.delete_team(ValueStorage.team_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_TEAM_NOT_EMPTY

    def test_delete_team(self):
        """
        GIVEN a team id
        WHEN you call dal.delete_team using the id
        THEN the team is deleted in the database
             and the status and team_id are returned
        """
        # check team exist
        team = (self.session.query(Team)
                    .filter(Team.id == ValueStorage.team_id)
                    .first())

        assert team

        # remove user (added in previous test)
        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())
        user.team_id = None

        self.session.commit()

        result = dal.delete_team(ValueStorage.team_id)

        assert result['status'] == "ok"
        assert result['team_id'] == ValueStorage.team_id

        self.session.expire_all()

        # check team deleted
        team = (self.session.query(Team)
                    .filter(Team.id == ValueStorage.team_id)
                    .first())

        assert team is None


class TestDalRole():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        Base.metadata.drop_all(engine)
        self.session.close()

    def test_create_role(self, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_role using the dictionnary
        THEN the role is created in the database
             and the status and role_id are returned
        """
        result = dal.create_role(role_fix)

        assert result['status'] == "ok"

        ValueStorage.role_id = result['role_id']
        role = (self.session.query(Role)
                .filter(Role.id == ValueStorage.role_id)
                .first())

        assert role.name == role_fix['name']

    def test_create_role_with_error(self, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_role using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        result = dal.create_role(role_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_role(self, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_role using the dictionnary
        THEN the role is updated in the database
             and the status and role_id are returned
        """
        role_dict = {}
        role_dict['id'] = ValueStorage.role_id
        new_name = role_fix['name'] + " mod"
        role_dict['name'] = new_name
        result = dal.update_role(role_dict)

        assert result['status'] == "ok"
        assert result['role_id'] == ValueStorage.role_id

        ValueStorage.role_id = result['role_id']
        role = (self.session.query(Role)
                .filter(Role.id == ValueStorage.role_id)
                .first())

        assert role.name == new_name

    def test_update_role_with_error(self, role_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_role using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        role_dict = {}
        role_dict['id'] = 999
        new_name = role_fix['name'] + " mod"
        role_dict['name'] = new_name
        result = dal.update_role(role_dict)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_deactivate_role(self):
        """
        GIVEN a role id
        WHEN you call dal.deactivate_team using the dictionnary
        THEN the role is deactivated in the database
             and the status and role_id are returned
        """
        role = (self.session.query(Role)
                .filter(Role.id == ValueStorage.role_id)
                .first())

        assert role.active is True

        result = dal.deactivate_role(role.id)

        assert result['status'] == "ok"
        assert result['role_id'] == role.id

        self.session.refresh(role)

        assert role.active is False

    def test_deactivate_role_with_error(self):
        """
        GIVEN a role id
        WHEN you call dal.deactivate_team using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        role_id = 999

        result = dal.deactivate_role(role_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_activate_role(self):
        """
        GIVEN a role id
        WHEN you call dal.activate_team using the dictionnary
        THEN the role is activated in the database
             and the status and role_id are returned
        """
        role = (self.session.query(Role)
                .filter(Role.id == ValueStorage.role_id)
                .first())

        assert role.active is False

        result = dal.activate_role(role.id)

        assert result['status'] == "ok"
        assert result['role_id'] == role.id

        self.session.refresh(role)

        assert role.active is True

    def test_activate_role_with_error(self):
        """
        GIVEN a role id
        WHEN you call dal.activate_team using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        role_id = 999

        result = dal.activate_role(role_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_role_by_id(self):
        """
        GIVEN a role_id
        WHEN you call dal.get_role_by_id using the id
        THEN the status and role are returned
        """
        role = (self.session.query(Role)
                .filter(Role.id == ValueStorage.role_id)
                .first())

        result = dal.get_role_by_id(ValueStorage.role_id)

        assert result['status'] == "ok"

        assert result['role'].id == role.id
        assert result['role'].name == role.name

    def test_get_role_by_id_with_error(self):
        """
        GIVEN a role_id
        WHEN you call dal.get_role_by_id using the id
        THEN the status and role are returned
        """
        role_id = 999

        result = dal.get_role_by_id(role_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_delete_role(self):
        """
        GIVEN a role id
        WHEN you call dal.delete_role using the id
        THEN the role is deleted in the database
             and the status and role_id are returned
        """
        # check role exist
        role = (self.session.query(Role)
                    .filter(Role.id == ValueStorage.role_id)
                    .first())

        assert role

        result = dal.delete_role(ValueStorage.role_id)

        assert result['status'] == "ok"
        assert result['role_id'] == ValueStorage.role_id

        self.session.expire_all()

        # check role deleted
        role = (self.session.query(Role)
                    .filter(Role.id == ValueStorage.role_id)
                    .first())

        assert role is None

    def test_delete_role_with_error(self, team_fix):
        """
        GIVEN a role id
        WHEN you call dal.delete_role using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        role_id = 999

        result = dal.delete_role(role_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND
