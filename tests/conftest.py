import pytest
from datetime import datetime


class ValueStorage():
    user_id = None
    team_id = None
    role_id = None

    client_id = None
    contract_id = None
    event_id = None


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
    return {'name': "role name 2",
            'active': True,
            }


@pytest.fixture
def client_fix():
    return {'first_name': 'client first name',
            'last_name': 'client last name',
            'email': 'client@email.com',
            'telephone': '0612345678',
            'enterprise': 'client enterprise',
            'active': True,
            'commercial_contact_id': None
            }


@pytest.fixture
def contract_fix():
    return {'client_id': None,
            'total_amount': 10000.00,
            'amount_unpaid': 9000.00,
            'status': 'unsigned',
            'active': True,
            }


@pytest.fixture
def event_fix():
    return {'title': 'test event',
            'contract_id': None,
            'start_date': datetime.strptime('24/12/2024', '%d/%m/%Y'),
            'end_date': datetime.strptime('24/12/2024', '%d/%m/%Y'),
            'support_contact_id': None,
            'location': 'somewhere',
            'attendees': 10,
            'notes': 'events notes',
            'active': True,
            }
