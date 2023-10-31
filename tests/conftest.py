import pytest


class ValueStorage():
    user_id = None
    team_id = None
    role_id = None


@pytest.fixture
def user_fix():
    return {'employee_number': 1,
            'first_name': "firstname 1",
            'last_name': "lastname 1",
            'email': "test1@email.com",
            'password': "password1",
            'active': True,
            'team_id': None
            }


@pytest.fixture
def team_fix():
    return {'name': "team name",
            'active': True,
            'role_id': None
            }


@pytest.fixture
def role_fix():
    return {'name': "role name",
            'active': True,
            }


"""
@pytest.fixture
def user2_fix():
    return {'employee_number': 2,
            'first_name': "firstname 2",
            'last_name': "lastname 2",
            'email': "test2@email.com",
            'password': "password2",
            'active': True,
            'team_id': None
            }


@pytest.fixture
def user3_fix():
    return {'employee_number': 3,
            'first_name': "firstname 3",
            'last_name': "lastname 3",
            'email': "test3@email.com",
            'password': "password3",
            'active': False,
            'team_id': None
            }


@pytest.fixture
def user4_fix():
    return {'employee_number': 4,
            'first_name': "firstname 4",
            'last_name': "lastname 4",
            'email': "test4@email.com",
            'password': "password4",
            'active': True,
            'team_id': None
            }
"""
