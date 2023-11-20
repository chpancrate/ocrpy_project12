from sqlalchemy.orm import sessionmaker

from models.user_models import User
from models.client_models import Client, Contract, Event
import models.event_dal_functions as dal
import models.client_dal_functions as dalc
import models.contract_dal_functions as dalo

from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


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

        result = dalc.create_client(client_fix)
        ValueStorage.client_id = result['client_id']
        self.session.commit()

        contract_fix['client_id'] = ValueStorage.client_id

        result = dalo.create_contract(contract_fix)
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


