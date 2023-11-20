from sqlalchemy.orm import sessionmaker

from models.user_models import User
from models.client_models import Client, Contract, Event
import models.event_dal_functions as dale
import models.client_dal_functions as dalc
import models.contract_dal_functions as dalo

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

        result = dalc.create_client(client_fix)
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dalo.create_contract(contract_fix)
        self.session.commit()
        ValueStorage.contract_id = result['contract_id']

        event_fix['contract_id'] = ValueStorage.contract_id

        result = dale.create_event(event_fix)

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

        result = dale.delete_event(ValueStorage.event_id)

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

        result = dale.delete_event(event_id)

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

        result = dalo.delete_contract(ValueStorage.contract_id)

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

        result = dalo.delete_contract(contract_id)

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

        result = dalc.delete_client(ValueStorage.client_id)

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

        result = dalc.delete_client(client_id)

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

        result = dalc.create_client(client_fix)
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dalo.create_contract(contract_fix)
        self.session.commit()
        ValueStorage.contract_id = result['contract_id']

        event_fix['contract_id'] = ValueStorage.contract_id

        result = dale.create_event(event_fix)

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

        result = dalc.delete_client(ValueStorage.client_id)

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
