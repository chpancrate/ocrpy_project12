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


class TestDalContract():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_contract(self, contract_fix, client_fix, user_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_contract using the dictionnary
        THEN the contract is created in the database
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
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dal.create_contract(contract_fix)

        assert result['status'] == "ok"

        self.session.commit()
        ValueStorage.contract_id = result['contract_id']
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract.status == contract_fix['status']

    def test_create_contract_with_error(self, contract_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_contract using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        # no commercial contact defined = error
        result = dal.create_contract(contract_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_contract(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_contract using the dictionnary
        THEN the contract is updated in the database
             and the status and team.id are returned
        """
        contract_dict = {}
        contract_dict['id'] = ValueStorage.contract_id
        new_status = 'signed'
        contract_dict['status'] = new_status

        result = dal.update_contract(contract_dict)

        assert result['status'] == "ok"
        assert result['contract_id'] == ValueStorage.contract_id

        self.session.commit()
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract.status == new_status

    def test_update_contract_with_error(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_contract using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        contract_dict = {}
        contract_dict['id'] = 999
        new_status = 'signed'
        contract_dict['status'] = new_status

        result = dal.update_contract(contract_dict)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_deactivate_contract(self):
        """
        GIVEN a contract_id
        WHEN you call dal.deactivate_contract using the id
        THEN the contract is deactivated in the database
             and the status and contract.id are returned
        """
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())
        assert contract.active is True

        result = dal.deactivate_contract(contract.id)

        assert result['status'] == "ok"
        assert result['contract_id'] == contract.id

        self.session.commit()
        self.session.refresh(contract)

        assert contract.active is False

    def test_deactivate_contract_with_error(self):
        """
        GIVEN a contract_id
        WHEN you call dal.deactivate_contract using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        contract_id = 999

        result = dal.deactivate_contract(contract_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_activate_contract(self):
        """
        GIVEN a contract_id
        WHEN you call dal.activate_contract using the id
        THEN the contract is activated in the database
             and the status and contract.id are returned
        """
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())
        assert contract.active is False

        result = dal.activate_contract(contract.id)

        assert result['status'] == "ok"
        assert result['contract_id'] == contract.id

        self.session.commit()
        self.session.refresh(contract)

        assert contract.active is True

    def test_activate_contract_with_error(self):
        """
        GIVEN a contract_id
        WHEN you call dal.activate_contract using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        contract_id = 999

        result = dal.activate_contract(contract_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_contract_by_id(self):
        """
        GIVEN a contract_id
        WHEN you call dal.get_contract_by_id using the id
        THEN the status and contract are returned
        """
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        result = dal.get_contract_by_id(ValueStorage.contract_id)

        assert result['status'] == "ok"

        assert result['contract'].id == contract.id
        assert result['contract'].status == contract.status
        assert result['contract'].total_amount == contract.total_amount

    def test_get_contract_by_id_with_error(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.get_contract_by_id using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        contract_id = 999

        result = dal.get_contract_by_id(contract_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND


class TestDalEvent():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_create_event(self, event_fix, user_fix, client_fix, contract_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_event using the dictionnary
        THEN the event is created in the database
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
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dal.create_contract(contract_fix)
        self.session.commit()
        ValueStorage.contract_id = result['contract_id']

        event_fix['contract_id'] = ValueStorage.contract_id

        result = dal.create_event(event_fix)

        assert result['status'] == "ok"

        self.session.commit()
        ValueStorage.event_id = result['event_id']
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event.title == event_fix['title']

    def test_create_event_with_error(self, event_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.create_event using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        # no commercial contact defined = error
        result = dal.create_event(event_fix)

        assert result['status'] == "ko"
        assert result['error']

    def test_update_event(self, event_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_event using the dictionnary
        THEN the event is updated in the database
             and the status and team.id are returned
        """
        event_dict = {}
        event_dict['id'] = ValueStorage.event_id
        new_title = event_fix['title'] + ' mod'
        event_dict['title'] = new_title

        result = dal.update_event(event_dict)

        assert result['status'] == "ok"
        assert result['event_id'] == ValueStorage.event_id

        self.session.commit()
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event.title == new_title

    def test_update_event_with_error(self, event_fix):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.update_event using the dictionnary
             and an error occured
        THEN the status ko is returned and an error
        """
        event_dict = {}
        event_dict['id'] = 999
        new_title = event_fix['title'] + ' mod'
        event_dict['title'] = new_title

        result = dal.update_event(event_dict)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_deactivate_event(self):
        """
        GIVEN a event_id
        WHEN you call dal.deactivate_event using the id
        THEN the event is deactivated in the database
             and the status and event.id are returned
        """
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())
        assert event.active is True

        result = dal.deactivate_event(event.id)

        assert result['status'] == "ok"
        assert result['event_id'] == event.id

        self.session.commit()
        self.session.refresh(event)

        assert event.active is False

    def test_deactivate_event_with_error(self):
        """
        GIVEN a event_id
        WHEN you call dal.deactivate_event using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        event_id = 999

        result = dal.deactivate_event(event_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_activate_event(self):
        """
        GIVEN a event_id
        WHEN you call dal.activate_event using the id
        THEN the event is activated in the database
             and the status and event.id are returned
        """
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())
        assert event.active is False

        result = dal.activate_event(event.id)

        assert result['status'] == "ok"
        assert result['event_id'] == event.id

        self.session.commit()
        self.session.refresh(event)

        assert event.active is True

    def test_activate_event_with_error(self):
        """
        GIVEN a event_id
        WHEN you call dal.activate_event using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        event_id = 999

        result = dal.activate_event(event_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_get_event_by_id(self):
        """
        GIVEN a event_id
        WHEN you call dal.get_event_by_id using the id
        THEN the status and event are returned
        """
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        result = dal.get_event_by_id(ValueStorage.event_id)

        assert result['status'] == "ok"

        assert result['event'].id == event.id
        assert result['event'].title == event.title
        assert result['event'].start_date == event.start_date

    def test_get_event_by_id_with_error(self):
        """
        GIVEN a dictionnary with the needed data
        WHEN you call dal.get_event_by_id using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        event_id = 999

        result = dal.get_event_by_id(event_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND


class TestDalDelete():

    def setup_class(cls):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        cls.session = Session()

    def teardown_class(self):
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_initialisation(self,
                            event_fix,
                            user_fix,
                            client_fix,
                            contract_fix):
        """
        Create user, client, contract and event for testing scenarii below
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
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dal.create_contract(contract_fix)
        self.session.commit()
        ValueStorage.contract_id = result['contract_id']

        event_fix['contract_id'] = ValueStorage.contract_id

        result = dal.create_event(event_fix)

        self.session.commit()
        ValueStorage.event_id = result['event_id']

    def test_delete_event(self):
        """
        GIVEN an event id
        WHEN you call dal.delete_event using the id
        THEN the event is deleted in the database
             and the status and event_id are returned
        """
        # check event exist
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event

        result = dal.delete_event(ValueStorage.event_id)

        assert result['status'] == "ok"
        assert result['event_id'] == ValueStorage.event_id

        self.session.commit()

        # check event deleted
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event is None

    def test_delete_event_with_error(self):
        """
        GIVEN a role id
        WHEN you call dal.delete_role using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        event_id = 999

        result = dal.delete_event(event_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_delete_contract(self):
        """
        GIVEN an contract id
        WHEN you call dal.delete_contract using the id
        THEN the contract is deleted in the database
             and the status and contract_id are returned
        """
        # check contract exist
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract

        result = dal.delete_contract(ValueStorage.contract_id)

        assert result['status'] == "ok"
        assert result['contract_id'] == ValueStorage.contract_id

        self.session.commit()

        # check contract deleted
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract is None

    def test_delete_contract_with_error(self):
        """
        GIVEN a role id
        WHEN you call dal.delete_role using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        contract_id = 999

        result = dal.delete_contract(contract_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_delete_client(self):
        """
        GIVEN an client id
        WHEN you call dal.delete_client using the id
        THEN the client is deleted in the database
             and the status and client_id are returned
        """
        # check client exist
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client

        result = dal.delete_client(ValueStorage.client_id)

        assert result['status'] == "ok"
        assert result['client_id'] == ValueStorage.client_id

        self.session.commit()

        # check client deleted
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client is None

    def test_delete_client_with_error(self):
        """
        GIVEN a role id
        WHEN you call dal.delete_role using the id
             and an error occured
        THEN the status ko is returned and an error
        """
        client_id = 999

        result = dal.delete_client(client_id)

        assert result['status'] == "ko"
        assert result['error'] == DB_RECORD_NOT_FOUND

    def test_reinitialisation(self,
                              event_fix,
                              user_fix,
                              client_fix,
                              contract_fix):
        """
        Create client, contract and event for testing scenarii below
        """
        client_fix['commercial_contact_id'] = ValueStorage.user_id

        result = dal.create_client(client_fix)
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dal.create_contract(contract_fix)
        self.session.commit()
        ValueStorage.contract_id = result['contract_id']

        event_fix['contract_id'] = ValueStorage.contract_id

        result = dal.create_event(event_fix)

        self.session.commit()
        ValueStorage.event_id = result['event_id']

    def test_client_full_delete(self):
        """
        GIVEN a client id for a client with contracts and events
        WHEN you call dal.delete_client using the id
        THEN the client is deleted in the database
             along with its contracts and events
             and the status and client_id are returned
        """
        # check client exist
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client

        # check contract exist
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract

        # check event exist
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event

        result = dal.delete_client(ValueStorage.client_id)

        assert result['status'] == "ok"
        assert result['client_id'] == ValueStorage.client_id

        self.session.commit()

        # check client deleted
        client = (self.session.query(Client)
                  .filter(Client.id == ValueStorage.client_id)
                  .first())

        assert client is None

        # check contract deleted
        contract = (self.session.query(Contract)
                    .filter(Contract.id == ValueStorage.contract_id)
                    .first())

        assert contract is None

        # check event deleted
        event = (self.session.query(Event)
                 .filter(Event.id == ValueStorage.event_id)
                 .first())

        assert event is None
