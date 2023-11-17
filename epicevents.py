# Epic events CRM launching script
from dotenv import load_dotenv
import os
import sentry_sdk

from controllers.general_cont import MainController
from views.general_view import Screen
from authentication.auth_models import AuthenticationManager


def main():

    load_dotenv()

    sentry_dsn = os.getenv("SENTRY_DSN")
    
    sentry_sdk.init(
        dsn=sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
    )
    authentication = AuthenticationManager()
    screen = Screen(authentication)

    epic_events_crm = MainController(screen, authentication)
    epic_events_crm.run()


if __name__ == "__main__":
    main()
