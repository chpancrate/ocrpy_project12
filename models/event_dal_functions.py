# define Data Layer Access functions for the Contract class
# created in the client_models package

from sqlalchemy import exc

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                )
from models.client_models import Event


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


def get_all_events():
    """ retrieve all events in database
    parameters :

    returns result dictionnary with keys :
    'status': ok or ko
    'events': events objects (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            events = (session.query(Event).all())
            if events is not None:
                result['events'] = events
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
