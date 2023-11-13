# define Data Layer Access functions for the Client class
# created in the client_models package

from sqlalchemy import exc
from sqlalchemy.orm import subqueryload

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                )
from models.client_models import Client
from models.contract_dal_functions import delete_contract


def create_client(client_dict):
    """ create client in database
    parameters :
    client_dict : dictionnary with data for client to be created,
                one key for each needed column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'client_id': id from created client (if status == ok)
    'error': error details (if status == ko)
    """
    client = Client(first_name=client_dict['first_name'],
                    last_name=client_dict['last_name'],
                    email=client_dict['email'],
                    telephone=client_dict['telephone'],
                    enterprise=client_dict['enterprise'],
                    commercial_contact_id=client_dict['commercial_contact_id'],
                    active=client_dict['active'],
                    )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(client)
            session.commit()
            result['client_id'] = client.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_client(client_dict):
    """ update client in database
    parameters :
    client_dict : dictionnary with
        'id' : client to be updated id
        one key for each updated in base
        for active column use activate/deactivate functions
    returns result dictionnary with keys :
    'status': ok or ko
    'client_id': id from updated client (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            client = (session.query(Client)
                      .filter(Client.id == client_dict['id'])
                      .first())

            if client is not None:
                if 'first_name' in client_dict:
                    client.first_name = client_dict['first_name']
                if 'last_name' in client_dict:
                    client.last_name = client_dict['last_name']
                if 'email' in client_dict:
                    client.email = client_dict['email']
                if 'telephone' in client_dict:
                    client.telephone = client_dict['telephone']
                if 'enterprise' in client_dict:
                    client.enterprise = client_dict['enterprise']
                if 'commercial_contact_id' in client_dict:
                    client.commercial_contact_id = client_dict[
                        'commercial_contact_id']

                session.commit()

                result['client_id'] = client.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_client(client_id):
    """ deactivate client in database (set active to False)
    parameters :
    client_id
    returns :
    'status': ok or ko
    'client_id': id from updated client (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            client = (session.query(Client)
                      .filter(Client.id == client_id)
                      .first())
            if client is not None:
                client.deactivate()
                session.commit()
                result['client_id'] = client.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_client(client_id):
    """ activate client in database (set active to False)
    parameters :
    client_id
    returns :
    'status': ok or ko
    'client_id': id from updated client (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            client = (session.query(Client)
                      .filter(Client.id == client_id)
                      .first())
            if client is not None:
                client.activate()
                session.commit()
                result['client_id'] = client.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_client_by_id(client_id):
    """ retrieve a client in database by id
    parameters :
    client_id
    returns result dictionnary with keys :
    'status': ok or ko
    'client': client object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            client = (session.query(Client)
                      .options(subqueryload(Client.contracts))
                      .filter(Client.id == client_id)
                      .first())
            if client is not None:
                result['client'] = client
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_all_clients():
    """ retrieve all clients in database
    parameters :

    returns result dictionnary with keys :
    'status': ok or ko
    'clients': clients objects (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            clients = (session.query(Client)
                       .all())
            if clients is not None:
                result['clients'] = clients
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_client(client_id):
    """ delete client in database and all linked contract
    parameters :
    client_id
    returns :
    'status': ok or ko
    'client_id': id from deleted client (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            client = (session.query(Client)
                      .filter(Client.id == client_id)
                      .first())
            if client:
                if client.contracts:
                    for contract in client.contracts:
                        result_del_co = delete_contract(contract.id)
                        if result_del_co['status'] == 'ko':
                            result['status'] = 'ko'
                            result['error'] = result_del_co['error']
                            return result

                rows_affected = (session.query(Client)
                                 .filter(Client.id == client_id)
                                 .delete())
                session.commit()

                if rows_affected == 0:
                    result['status'] = "ko"
                    result['error'] = DB_RECORD_NOT_FOUND
                else:
                    result['client_id'] = client_id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result
