from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models.models import Base, User
import models.dal_functions as dal


class TestDal():
    def setup_class(self):
        db_url = "sqlite:///unit_test.db"
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        user_dict = {
                     'employee_number': 2,
                     'first_name': "first name test",
                     'last_name': "last_name_test",
                     'email': "test@email.com",
                     'password': "password",
                     'active': True,
                     'team_id': None
        }

        status = dal.create_user(user_dict)

        assert status == "ok"

        user = (self.session.query(User)
                    .filter(User.first_name == "first name test")
                    .first())
        
        assert user.email == "test@email.com"