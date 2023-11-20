from sqlalchemy.orm import sessionmaker

from models.user_models import User
from models.client_models import Client, Contract, Event
import models.client_dal_functions as dal
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


class TestDalClient():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_client(self, client_fix, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_client using the dictionnary
        THEN the client is created in the database
             and the status and team.id are returned
        """
        user = User(employee_number=user_fix['employee_number'],
                    first_name=user_fix['first_name'],
                    last_name=user_fix['last_name'],
                    email=user_fix['email'],
                    password=user_fix['password'],
                    active=user_fix['active'],
                    team_id=user_fix['team_id']
                    )
        self.session.add(user)
        self.session.commit()
        ValueStorage.user_id = user.id

        client_fix['commercial_contact_id'] = user.id

        result = dal.create_client(client_fix)

        assert result['status'] == "ok"

        self.session.commit()
        ValueStorage.client_id = result['client_id']
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client.first_name == client_fix['first_name']

    def test_create_client_with_error(self, client_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_client using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        # no commercial contact defined = error
        result = dal.create_client(client_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_client(self, client_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_client using the dictionnary
        THEN the client is updated in the database
             and the status and team.id are returned
        """
        client_dict = {}
        client_dict['id'] = ValueStorage.client_id
        new_name = client_fix['first_name'] + " mod"
        client_dict['first_name'] = new_name

        result = dal.update_client(client_dict)

        assert result['status'] == "ok"
        assert result['client_id'] == ValueStorage.client_id

        self.session.commit()
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client.first_name == new_name

    def test_update_client_with_error(self, client_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_client using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        client_dict = {}
        client_dict['id'] = 999
        new_name = client_fix['first_name'] + " mod"
        client_dict['first_name'] = new_name

        result = dal.update_client(client_dict)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_deactivate_client(self):
        """
        GIVEN a client_id
        WHEN you call dal.deactivate_client using the id
        THEN the client is deactivated in the database
             and the status and client.id are returned
        """
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())
        assert client.active is True

        result = dal.deactivate_client(client.id)

        assert result['status'] == "ok"
        assert result['client_id'] == client.id

        self.session.commit()
        self.session.refresh(client)

        assert client.active is False

    def test_deactivate_client_with_error(self):
        """
        GIVEN a client_id
        WHEN you call dal.deactivate_client using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        client_id = 999

        result = dal.deactivate_client(client_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_activate_client(self):
        """
        GIVEN a client_id
        WHEN you call dal.activate_client using the id
        THEN the client is activated in the database
             and the status and client.id are returned
        """
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())
        assert client.active is False

        result = dal.activate_client(client.id)

        assert result['status'] == "ok"
        assert result['client_id'] == client.id

        self.session.commit()
        self.session.refresh(client)

        assert client.active is True

    def test_activate_client_with_error(self):
        """
        GIVEN a client_id
        WHEN you call dal.activate_client using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        client_id = 999

        result = dal.activate_client(client_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_client_by_id(self):
        """
        GIVEN a client_id
        WHEN you call dal.get_client_by_id using the id
        THEN the status and client are returned
        """
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        result = dal.get_client_by_id(ValueStorage.client_id)

        assert result['status'] == "ok"

        assert result['client'].id == client.id
        assert result['client'].first_name == client.first_name

    def test_get_client_by_id_with_error(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.get_client_by_id using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        client_id = 999

        result = dal.get_client_by_id(client_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND
