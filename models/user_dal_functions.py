# define Data Layer Access functions for the User, Team and Role classes
# created in the user_models package

from argon2 import PasswordHasher
from sqlalchemy import exc

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                DB_TEAM_NOT_EMPTY,
                )
from models.user_models import User, Team, Role


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
            user = session.query(User).filter(User.email == email).first()
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
            user = session.query(User).filter(User.id == user_id).first()
            if user is not None:
                result['user'] = user
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


def create_team(team_dict):
    """ create team in database
    parameters :
    team_dict : dictionnary with data for team to be created,
                one key for each column in base, id excepted
    returns result dictionnary with keys :
    'status': ok or ko
    'team_id': id from created team (if status == ok)
    'error': error details (if status == ko)
    """
    team = Team(name=team_dict['name'],
                active=team_dict['active'],
                role_id=team_dict['role_id']
                )

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            session.add(team)
            session.commit()
            result['team_id'] = team.id

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def update_team(team_dict):
    """ update team in database
    parameters :
    team_dict : dictionnary with mandatory 'id' key
                and one key for each column to be modified
                active field cannot be updated with this function
                use activate_team / deactivate_team instead
    returns result dictionnary with keys :
    'status': ok or ko
    'team_id': updated team id (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            team = (session.query(Team)
                    .filter(Team.id == team_dict['id'])
                    .first())

            if team is not None:
                if 'name' in team_dict:
                    team.name = team_dict['name']
                if 'role_id' in team_dict:
                    team.role_id = team_dict['role_id']

                session.commit()

                result['team_id'] = team.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def activate_team(team_id):
    """ set team active field to True
    parameters :
    team_id
    returns result dictionnary with keys :
    'status': ok or ko
    'team_id': updated team id (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            team = (session.query(Team)
                    .filter(Team.id == team_id)
                    .first())
            if team is not None:
                team.activate()
                session.commit()
                result['team_id'] = team.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def deactivate_team(team_id):
    """ set team active field to False
    parameters :
    team_id
    returns result dictionnary with keys :
    'status': ok or ko
    'team_id': updated team id (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            team = (session.query(Team)
                    .filter(Team.id == team_id)
                    .first())
            if team is not None:
                team.deactivate()
                session.commit()
                result['team_id'] = team.id
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def get_team_by_id(team_id):
    """
    parameters :
    team_id
    returns result dictionnary with keys :
    'status': ok or ko
    'team': team object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            team = (session.query(Team)
                    .filter(Team.id == team_id)
                    .first())
            if team is not None:
                result['team'] = team
            else:
                result['status'] = "ko"
                result['error'] = DB_RECORD_NOT_FOUND
    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


def delete_team(team_id):
    """ delete team in database
    no user must be using the team
    parameters :
    team_id
    returns :
    'status': ok or ko
    'team_id': id from deleted team (if status == ok)
    'error': error details (if status == ko)
    """

    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:

            team = (session.query(Team)
                    .filter(Team.id == team_id)
                    .first())

            if not team.users:
                rows_affected = (session.query(Team)
                                 .filter(Team.id == team_id)
                                 .delete())
                session.commit()

                if rows_affected == 0:
                    result['status'] = "ko"
                    result['error'] = DB_RECORD_NOT_FOUND
                else:
                    result['team_id'] = team_id
            else:
                result['status'] = "ko"
                result['error'] = DB_TEAM_NOT_EMPTY

    except exc.SQLAlchemyError as e:
        result['status'] = "ko"
        result['error'] = e

    return result


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
