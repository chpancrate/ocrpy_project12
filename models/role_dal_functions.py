# define Data Layer Access functions for the Role class
# created in the user_models package

from sqlalchemy import exc

from db import (session_maker,
                DB_RECORD_NOT_FOUND
                )
from models.user_models import Role


def create_role(role_dict):
    """ create role in database
    parameters :
    user_dict : dictionnary with data for role to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'role_id': id from created role object (if status == ok)
    'error': error details (if status == ko)
    """
    role = Role(name=role_dict['name'],
                active=role_dict['active']
                )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(role)
            session.commit()
            result['role_id'] = role.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_role(role_dict):
    """ create user in database
    parameters :
    user_dict : dictionnary with data fot user to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'role_id': id from updated role (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            role = (session.query(Role)
                    .filter(Role.id == role_dict['id'])
                    .first())

            if role is not None:
                if 'name' in role_dict:
                    role.name = role_dict['name']

                session.commit()

                result['role_id'] = role.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_role(role_id):
    """ create user in database
    parameters :
    user_dict : dictionnary with data fot user to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'role_id': updated role id (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            role = (session.query(Role)
                    .filter(Role.id == role_id)
                    .first())
            if role is not None:
                role.activate()
                session.commit()
                result['role_id'] = role.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_role(role_id):
    """ create user in database
    parameters :
    user_dict : dictionnary with data fot user to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'role_id': updated role id (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            role = (session.query(Role)
                    .filter(Role.id == role_id)
                    .first())
            if role is not None:
                role.deactivate()
                session.commit()
                result['role_id'] = role.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_role_by_id(role_id):
    """
    parameters :
    role_id
    returns result dictionnary with keys :
    'status': ok or ko
    'role': role object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            role = (session.query(Role)
                    .filter(Role.id == role_id)
                    .first())
            if role is not None:
                result['role'] = role
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_role(role_id):
    """ delete role in database
    parameters :
    role_id
    returns :
    'status': ok or ko
    'role_id': id from deleted role (if status == ok)
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            rows_affected = (session.query(Role)
                             .filter(Role.id == role_id)
                             .delete())
            session.commit()

            if rows_affected == 0:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
            else:
                result['role_id'] = role_id
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result
