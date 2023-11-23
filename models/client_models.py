from sqlalchemy import (Column,
                        ForeignKey,
                        CheckConstraint,
                        Integer,
                        String,
                        Boolean,
                        DateTime,
                        Float,
                        Text
                        )
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base

CONTRACT_STATUS = ['signé', 'non signé']


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    telephone = Column(String(50), nullable=False)
    enterprise = Column(String(50), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)
    commercial_contact_id = Column(Integer,
                                   ForeignKey('users.id'),
                                   nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    contracts = relationship('Contract',
                             cascade='save-update, merge, delete',
                             passive_deletes=True,
                             backref='contracts')

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def full_name(self):
        full_name = self.first_name + ' ' + self.last_name
        return full_name


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer,
                       ForeignKey('clients.id', ondelete='CASCADE'),
                       nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_unpaid = Column(Float, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)
    status = Column(String(10), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    events = relationship('Event',
                          cascade='save-update, merge, delete',
                          passive_deletes=True,
                          backref="events")

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    contract_id = Column(Integer,
                         ForeignKey('contracts.id', ondelete='CASCADE'),
                         nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    support_contact_id = Column(Integer, ForeignKey('users.id'))
    location = Column(String(100), nullable=False)
    attendees = Column(Integer, CheckConstraint('attendees >= 0'), default=0)
    notes = Column(Text)
    creation_date = Column(DateTime, nullable=False, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)
    active = Column(Boolean, default=True, nullable=False)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True
