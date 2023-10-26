from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from argon2 import PasswordHasher
from db import Base

# Base = declarative_base()


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

        if ph.verify(self.password, input_password):
            self.is_authenticated = True
            return True
        else:
            self.is_authenticated = False
            return False

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    users = relationship("User", backref="users")

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    teams = relationship("Team", backref="teams")

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
