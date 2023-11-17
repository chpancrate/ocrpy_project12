# define Data Layer Access functions for the User class
# created in the user_models package

from argon2 import PasswordHasher
from sqlalchemy import exc
from sqlalchemy.orm import subqueryload

from db import (session_maker,
                DB_RECORD_NOT_FOUND
                )
from models.user_models import User


def create_user(user_dict):
    """ create user in database
    parameters :
    user_dict : dictionnary with data for user to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'user_id': id from created user (if status == ok)
    'error': error details (if status == ko)
    """

    user = User(employee_number=user_dict['employee_number'],
                first_name=user_dict['first_name'],
                last_name=user_dict['last_name'],
                email=user_dict['email'],
                password=user_dict['password'],
                active=user_dict['active'],
                team_id=user_dict['team_id']
                )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(user)
            session.commit()
            result['user_id'] = user.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_user(user_dict):
    """ update user in database
    not to be used for the "active" or "password" fields
    parameters :
    user_dict : dictionnary with data to be updated for the user
                mandatory key 'id'
                one key for each modified column in base
    returns :
    'status': ok or ko
    'user_id': id from updated user (if status == ok)
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            user = (session.query(User)
                    .filter(User.id == user_dict['id'])
                    .first())

            if user is not None:
                if 'employee_number' in user_dict:
                    user.employee_number = user_dict['employee_number']
                if 'first_name' in user_dict:
                    user.first_name = user_dict['first_name']
                if 'last_name' in user_dict:
                    user.last_name = user_dict['last_name']
                if 'email' in user_dict:
                    user.email = user_dict['email']
                if 'team_id' in user_dict:
                    user.team_id = user_dict['team_id']

                session.commit()

                result['user_id'] = user.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_user(user_id):
    """ deactivate user in database (set active to False)
    parameters :
    user_id
    returns :
    'status': ok or ko
    'user_id': id from updated user (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            user = (session.query(User)
                    .filter(User.id == user_id)
                    .first())
            if user is not None:
                user.deactivate()
                session.commit()
                result['user_id'] = user.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_user(user_id):
    """ activate user in database (set active to True)
    parameters :
    user_id
    returns :
    'status': ok or ko
    'user_id': id from updated user (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            user = (session.query(User)
                    .filter(User.id == user_id)
                    .first())
            if user is not None:
                user.activate()
                session.commit()
                result['user_id'] = user.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_user_password(user_dict):
    """ update user password with hashing
    parameters :
    dictionnary dict mandatory keys 'id' and 'password'
    returns :
    'status': ok or ko
    'user_id': id from updated user (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            user = (session.query(User)
                    .filter(User.id == user_dict['id'])
                    .first())

            if user is not None:
                ph = PasswordHasher()
                hash_password = ph.hash(user_dict['password'])
                user.password = hash_password
                session.commit()

                result['user_id'] = user.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_user_by_email(email):
    """ retrieve a user in database by email
    parameters :
    user_id
    returns result dictionnary with keys :
    'status': ok or ko
    'user': user object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            user = (session.query(User)
                    .filter(User.email == email)
                    .first())
            if user is not None:
                result['user'] = user
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_user_by_id(user_id):
    """ retrieve a user in database by id
    parameters :
    user_id
    returns result dictionnary with keys :
    'status': ok or ko
    'user': user object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            user = (session.query(User)
                    .filter(User.id == user_id)
                    .first())
            if user is not None:
                result['user'] = user
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_user_by_employee_id(employee_number):
    """ retrieve a user in database by employee number
    parameters :
    user_id
    returns result dictionnary with keys :
    'status': ok or ko
    'user': user object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            user = (session.query(User)
                    .filter(User.employee_number == employee_number)
                    .first())
            if user is not None:
                result['user'] = user
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_all_users():
    """ retrieve all user in database
    parameters :
    returns result dictionnary with keys :
    'status': ok or ko
    'users': list of users object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            users = session.query(User).all()
            if users is not None:
                result['users'] = users
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_user(user_id):
    """ delete user in database
    parameters :
    user_id
    returns :
    'status': ok or ko
    'user_id': id from deleted user (if status == ok)
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            rows_affected = (session.query(User)
                             .filter(User.id == user_id)
                             .delete())
            session.commit()

            if rows_affected == 0:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
            else:
                result['user_id'] = user_id
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_client_list_for_user(user_id):
    """ get clients data linked to the user
    parameters :
    user_id
    returns :
    'status': ok or ko
    'data': data from the clients linked to the user
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            user = (session.query(User)
                    .filter(User.id == user_id)
                    .first())
            session.commit()

            if user is None:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
            else:
                if user.clients is None:
                    result['data'] = []
                else:
                    result['data'] = user.clients.all()
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result
