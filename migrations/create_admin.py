# admin user creation script
from db import (session_maker)
from models.user_models import User
from models.client_models import Client, Event


user = User(
    employee_number=999999999,
    first_name='admin',
    last_name='admin',
    email='admin@crm.net',
    password='password',  # TO BE MODIFIED BEFORE RUNNING THE SCRIPT
    active=True,
    )
with session_maker() as session:
    session.add(user)
    session.commit()
