# define Data Layer Access functions for the Team class
# created in the user_models package

from sqlalchemy import exc

from db import (session_maker,
                DB_RECORD_NOT_FOUND,
                DB_TEAM_NOT_EMPTY,
                )
from models.user_models import Team


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


def get_all_teams():
    """ retrieve all teams in database
    parameters :
    returns result dictionnary with keys :
    'status': ok or ko
    'teams': list of teams object (if status == ok)
    'error': error details (if status == ko)
    """
    result = {}
    result['status'] = "ok"
    try:
        with session_maker() as session:
            teams = session.query(Team).all()
            if teams is not None:
                result['teams'] = teams
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

            if team.users.all() == []:
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
