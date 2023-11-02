# define Data Layer Access functions for the Client, Contract and Event classes
# created in the client_models package

from sqlalchemy import exc

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                )
from models.client_models import Client, Contract, Event


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
                    client.team_id = client_dict['team_id']
                if 'enterprise' in client_dict:
                    client.team_id = client_dict['team_id']
                if 'commercial_contact_id' in client_dict:
                    client.team_id = client_dict['team_id']

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


def create_event(event_dict):
    """ create event in database
    parameters :
    event_dict : dictionnary with data for event to be created,
                one key for each needed column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'event_id': id from created event (if status == ok)
    'error': error details (if status == ko)
    """
    event = Event(title=event_dict['title'],
                  contract_id=event_dict['contract_id'],
                  start_date=event_dict['start_date'],
                  end_date=event_dict['end_date'],
                  support_contact_id=event_dict['support_contact_id'],
                  location=event_dict['location'],
                  attendees=event_dict['attendees'],
                  notes=event_dict['notes'],
                  active=event_dict['active']
                  )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(event)
            session.commit()
            result['event_id'] = event.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_event(event_dict):
    """ update event in database
    parameters :
    event_dict : dictionnary with
        'id' : event to be updated id
        one key for each updated in base
        for active column use activate/deactivate functions
    returns result dictionnary with keys :
    'status': ok or ko
    'event_id': id from updated event (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            event = (session.query(Event)
                     .filter(Event.id == event_dict['id'])
                     .first())

            if event is not None:
                if 'title' in event_dict:
                    event.title = event_dict['title']
                if 'contract_id' in event_dict:
                    event.contract_id = event_dict['contract_id']
                if 'start_date' in event_dict:
                    event.start_date = event_dict['start_date']
                if 'end_date' in event_dict:
                    event.end_date = event_dict['end_date']
                if 'support_contact_id' in event_dict:
                    event.support_contact_id = event_dict['support_contact_id']
                if 'location' in event_dict:
                    event.location = event_dict['location']
                if 'attendees' in event_dict:
                    event.attendees = event_dict['attendees']
                if 'notes' in event_dict:
                    event.notes = event_dict['notes']

                session.commit()

                result['event_id'] = event.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_event(event_id):
    """ deactivate event in database (set active to False)
    parameters :
    event_id
    returns :
    'status': ok or ko
    'event_id': id from updated event (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            event = (session.query(Event)
                     .filter(Event.id == event_id)
                     .first())
            if event is not None:
                event.deactivate()
                session.commit()
                result['event_id'] = event.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_event(event_id):
    """ activate event in database (set active to False)
    parameters :
    event_id
    returns :
    'status': ok or ko
    'event_id': id from updated event (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            event = (session.query(Event)
                     .filter(Event.id == event_id)
                     .first())
            if event is not None:
                event.activate()
                session.commit()
                result['event_id'] = event.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_event_by_id(event_id):
    """ retrieve a event in database by id
    parameters :
    event_id
    returns result dictionnary with keys :
    'status': ok or ko
    'event': event object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            event = (session.query(Event)
                     .filter(Event.id == event_id)
                     .first())
            if event is not None:
                result['event'] = event
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_event(event_id):
    """ delete event in database
    parameters :
    event_id
    returns :
    'status': ok or ko
    'event_id': id from deleted event (if status == ok)
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            rows_affected = (session.query(Event)
                             .filter(Event.id == event_id)
                             .delete())
            session.commit()

            if rows_affected == 0:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
            else:
                result['event_id'] = event_id
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
