# script to create needed dat for the use of epicevnts crm
# THE ADMIN PASSWORD MUST BE CHANGED BEFORE RUNNING
from db import (session_maker)
from models.user_models import User, Team, Role


try:
    with session_maker() as session:
        # 'management' role creation

        role_management = Role(
            name='gestion',
            active=True
        )
        session.add(role_management)
        session.commit()

        # 'commercial' role creation

        role_commercial = Role(
            name='commercial',
            active=True
        )
        session.add(role_commercial)
        session.commit()

        # 'support' role creation

        role_support = Role(
            name='support',
            active=True
        )
        session.add(role_support)
        session.commit()

        # 'management' team creation

        team_management = Team(
            name='gestion',
            role_id=role_management.id,
            active=True
        )
        session.add(team_management)
        session.commit()

        # 'commercial' team creation

        team_commercial = Team(
            name='commercial',
            role_id=role_commercial.id,
            active=True
        )
        session.add(team_commercial)
        session.commit()

        # 'support' team creation

        team_support = Team(
            name='support',
            role_id=role_support.id,
            active=True
        )
        session.add(team_support)
        session.commit()

        # admin user creation

        user = User(
            employee_number=999999999,
            first_name='admin',
            last_name='admin',
            email='admin@crm.net',
            password='password',  # TO BE MODIFIED BEFORE RUNNING THE SCRIPT
            team_id='1',
            active=True,
            )
        session.add(user)
        session.commit()

except Exception as e:
    print(f"DB initialization failed with error : {str(e)}")
    session.rollback()
