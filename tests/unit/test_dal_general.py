from sqlalchemy.orm import sessionmaker

from models.user_models import User, Role, Team
import models.general_dal_functions as dal

from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


class TestDalDelete():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_initialisation(self,
                            user_fix,
                            team_fix,
                            role_fix):
        """
        Create user, team, role for testing scenarii below
        """
        role = Role(
            name=role_fix['name'],
            active=True
        )
        self.session.add(role)
        self.session.commit()

        team = Team(
            name=team_fix['name'],
            role_id=role.id,
            active=True
        )
        self.session.add(team)
        self.session.commit()

        user = User(employee_number=user_fix['employee_number'],
                    first_name=user_fix['first_name'],
                    last_name=user_fix['last_name'],
                    email=user_fix['email'],
                    password=user_fix['password'],
                    active=user_fix['active'],
                    team_id=team.id
                    )
        self.session.add(user)
        self.session.commit()
        ValueStorage.user_id = user.id

    def test_get_user_role(self, role_fix):
        """
        GIVEN a user_id
        WHEN you call dal.get_user_role using the id
        THEN the role of the user is returned
             the status ok is returned
        """
        user_id = ValueStorage.user_id

        result = dal.get_user_role(user_id)

        assert result['status'] == "ok"
        assert result['user_role'] == role_fix['name']

    def test_get_user_role_with_error(self, role_fix):
        """
        GIVEN a user_id
        WHEN you call dal.get_user_role using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        user_id = 999

        result = dal.get_user_role(user_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND
