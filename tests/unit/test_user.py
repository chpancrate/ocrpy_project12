from models.user_models import User


class TestUser():

    def test_is_password_correct_ok(self, user_fix):
        user = User(employee_number=user_fix['employee_number'],
                    first_name=user_fix['first_name'],
                    last_name=user_fix['last_name'],
                    email=user_fix['email'],
                    password=user_fix['password'],
                    active=user_fix['active'],
                    team_id=user_fix['team_id']
                    )

        password = user_fix['password']
        assert user.is_password_correct(password)

    def test_is_password_correct_ko(self, user_fix):
        user = User(employee_number=user_fix['employee_number'],
                    first_name=user_fix['first_name'],
                    last_name=user_fix['last_name'],
                    email=user_fix['email'],
                    password=user_fix['password'],
                    active=user_fix['active'],
                    team_id=user_fix['team_id']
                    )

        password = 'wrong_password'
        assert not user.is_password_correct(password)
