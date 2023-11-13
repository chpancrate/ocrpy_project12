from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db import Base
from .client_models import Client


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_number = Column(Integer, nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), default=None)
    clients = relationship('Client',
                           backref='followed_clients',
                           lazy='dynamic')
    events = relationship('Event',
                          backref='supported_events',
                          lazy='dynamic')

    def __init__(self,
                 employee_number,
                 first_name,
                 last_name,
                 email,
                 password,
                 team_id=None,
                 active=True):

        ph = PasswordHasher()

        self.employee_number = employee_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = ph.hash(password)
        self.team_id = team_id
        self.active = active

        self.is_authenticated = False

    def is_password_correct(self, input_password):

        ph = PasswordHasher()
        result = False

        try:
            result_verify = ph.verify(self.password, input_password)
            if result_verify:
                self.is_authenticated = True
                result = True
            else:
                self.is_authenticated = False
                result = False
        except VerifyMismatchError:
            self.is_authenticated = False
            result = False

        return result

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def full_name(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    users = relationship('User',
                         backref='users',
                         lazy='dynamic')

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True, nullable=False)
    teams = relationship('Team',
                         backref='teams',
                         lazy='dynamic')

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
