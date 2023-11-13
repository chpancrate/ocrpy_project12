# Epic events CRM launching script
from controllers.general_cont import MainController
from views.general_view import Screen
from authentication.auth_models import AuthenticationManager


def main():
    screen = Screen()
    authentication = AuthenticationManager()

    epic_events_crm = MainController(screen, authentication)
    epic_events_crm.run()


if __name__ == "__main__":
    main()
