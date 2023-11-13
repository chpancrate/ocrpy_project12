# define Data Layer Access functions for the Contract class
# created in the client_models package

from sqlalchemy import exc
from sqlalchemy.orm import subqueryload

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                )
from models.client_models import Contract
from models.event_dal_functions import delete_event


def create_contract(contract_dict):
    """ create contract in database
    parameters :
    contract_dict : dictionnary with data for contract to be created,
                one key for each needed column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'contract_id': id from created contract (if status == ok)
    'error': error details (if status == ko)
    """
    contract = Contract(client_id=contract_dict['client_id'],
                        total_amount=contract_dict['total_amount'],
                        amount_unpaid=contract_dict['amount_unpaid'],
                        status=contract_dict['status'],
                        active=contract_dict['active']
                        )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(contract)
            session.commit()
            result['contract_id'] = contract.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_contract(contract_dict):
    """ update contract in database
    parameters :
    contract_dict : dictionnary with
        'id' : contract to be updated id
        one key for each updated in base
        for active column use activate/deactivate functions
    returns result dictionnary with keys :
    'status': ok or ko
    'contract_id': id from updated contract (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            contract = (session.query(Contract)
                        .filter(Contract.id == contract_dict['id'])
                        .first())

            if contract is not None:
                if 'client_id' in contract_dict:
                    contract.client_id = contract_dict['client_id']
                if 'total_amount' in contract_dict:
                    contract.total_amount = contract_dict['total_amount']
                if 'amount_unpaid' in contract_dict:
                    contract.amount_unpaid = contract_dict['amount_unpaid']
                if 'status' in contract_dict:
                    contract.status = contract_dict['status']

                session.commit()

                result['contract_id'] = contract.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_contract(contract_id):
    """ deactivate contract in database (set active to False)
    parameters :
    contract_id
    returns :
    'status': ok or ko
    'contract_id': id from updated contract (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            contract = (session.query(Contract)
                        .filter(Contract.id == contract_id)
                        .first())
            if contract is not None:
                contract.deactivate()
                session.commit()
                result['contract_id'] = contract.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_contract(contract_id):
    """ activate contract in database (set active to False)
    parameters :
    contract_id
    returns :
    'status': ok or ko
    'contract_id': id from updated contract (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            contract = (session.query(Contract)
                        .filter(Contract.id == contract_id)
                        .first())
            if contract is not None:
                contract.activate()
                session.commit()
                result['contract_id'] = contract.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_contract_by_id(contract_id):
    """ retrieve a contract in database by id
    parameters :
    contract_id
    returns result dictionnary with keys :
    'status': ok or ko
    'contract': contract object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            contract = (session.query(Contract)
                        .options(subqueryload(Contract.events))
                        .filter(Contract.id == contract_id)
                        .first())
            if contract is not None:
                result['contract'] = contract
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_all_contracts():
    """ retrieve all contracts in database
    parameters :

    returns result dictionnary with keys :
    'status': ok or ko
    'contracts': contracts objects (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            contracts = (session.query(Contract).all())
            if contracts is not None:
                result['contracts'] = contracts
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_contract(contract_id):
    """ delete contract in database and all linked event
    parameters :
    contract_id
    returns :
    'status': ok or ko
    'contract_id': id from deleted contract (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            contract = (session.query(Contract)
                        .filter(Contract.id == contract_id)
                        .first())
            if contract:
                if contract.events:
                    for event in contract.events:
                        result_del_ev = delete_event(event.id)
                        if result_del_ev['status'] == 'ko':
                            result['status'] = 'ko'
                            result['error'] = result_del_ev['error']
                            return result

                rows_affected = (session.query(Contract)
                                 .filter(Contract.id == contract_id)
                                 .delete())
                session.commit()

                if rows_affected == 0:
                    result['status'] = "ko"
                    result['error'] = DB_RECORD_NOT_FOUND
                else:
                    result['contract_id'] = contract_id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result
