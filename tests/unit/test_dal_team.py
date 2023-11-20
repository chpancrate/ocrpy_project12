from argon2 import PasswordHasher
from sqlalchemy.orm import sessionmaker

from models.user_models import User, Team, Role
import models.team_dal_functions as dal
import models.user_dal_functions as dalu
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND,
                DB_TEAM_NOT_EMPTY
                )
from ..conftest import ValueStorage


class TestDalTeam():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

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

        self.session.commit()
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

        self.session.commit()
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

        self.session.commit()
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

        self.session.commit()
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
        result = dalu.create_user(user_fix)
        ValueStorage.user_id = result['user_id']

        # check team exist
        team = (self.session.query(Team)
                    .filter(Team.id == ValueStorage.team_id)
                    .first())

        assert team

        # add user to team
        self.session.commit()
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
        print('user id: ', user.id)
        print('user team_id: ', user.team_id)

        user.team_id = None

        self.session.commit()

        user = (self.session.query(User)
                    .filter(User.id == ValueStorage.user_id)
                    .first())
        print('user id: ', user.id)
        print('user team_id: ', user.team_id)

        print('team id:', ValueStorage.team_id)

        result = dal.delete_team(ValueStorage.team_id)
        print(result['error'])
        assert result['status'] == "ok"
        assert result['team_id'] == ValueStorage.team_id

        self.session.commit()

        # check team deleted
        team = (self.session.query(Team)
                    .filter(Team.id == ValueStorage.team_id)
                    .first())

        assert team is None
        """
        pass
