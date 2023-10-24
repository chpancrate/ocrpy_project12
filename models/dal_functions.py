from epicevents import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from models.models import User


session_maker = sessionmaker(bind=engine)


def get_user_by_email(email):
    try:
        with session_maker() as session:
            user = session.query(User).filter(User.email == email).first()
    except exc.SQLAlchemyError:
        user = None

    return user


def get_user_by_id(user_id):
    try:
        with session_maker() as session:
            user = session.query(User).filter(User.id == user_id).first()
    except exc.SQLAlchemyError:
        user = None

    return user


def create_user(user_dict):
    user = User(employee_number=user_dict['employee_number'],
                first_name=user_dict['first_name'],
                last_name=user_dict['last_name'],
                email=user_dict['email'],
                password=user_dict['password'],
                active=user_dict['active'],
                team_id=user_dict['team_id']
                )

    status = "ok"
    try:
        with session_maker() as session:
            session.add(user)
            session.commit()
    except exc.SQLAlchemyError as e:
        print("xxxx", e)
        status = "error"

    return status


def update_user(user_dict):

    status = "ok"
    try:
        with session_maker() as session:
            user = (session.query(User)
                    .filter(User.id == user_dict['id'])
                    .first())

            user.employee_number = user_dict['employee_number'],
            user.first_name = user_dict['first_name'],
            user.last_name = user_dict['last_name'],
            user.email = user_dict['email'],
            user.password = user_dict['password'],
            user.active = user_dict['active'],
            user.team_id = user_dict['team_id']

            session.commit()
    except exc.SQLAlchemyError:
        status = "error"

    return status


def deactivate_user():
    pass


def reactivate_user():
    pass
