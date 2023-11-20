from sqlalchemy.orm import sessionmaker

from models.user_models import User
from models.client_models import Client, Contract, Event
import models.contract_dal_functions as dal
import models.client_dal_functions as dalc
from db import (engine,
                Base,
                DB_RECORD_NOT_FOUND
                )
from ..conftest import ValueStorage


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

        result = dalc.create_client(client_fix)
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
