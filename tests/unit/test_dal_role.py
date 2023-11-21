from sqlalchemy.orm import sessionmaker

from models.user_models import Role
import models.role_dal_functions as dal
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


class TestDalRole():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

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

        self.session.commit()
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

        self.session.commit()
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

        self.session.commit()
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

        self.session.commit()

        # check role deleted
        role = (self.session.query(Role)
                    .filter(Role.id == ValueStorage.role_id)
                    .first())

        assert role is None

    def test_delete_role_with_error(self):
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
