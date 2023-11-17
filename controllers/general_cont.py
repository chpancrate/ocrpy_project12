import datetime
import time
from sentry_sdk import capture_exception, capture_message, set_user


from controllers.constants import (MSG_ERROR,
                                   MSG_CLIENT_NOT_FOUND,
                                   MSG_ERROR_LOGIN,
                                   MSG_WRONG_AUTHORIZATION,
                                   MSG_WRONG_EMAIL_FORMAT,
                                   MSG_WRONG_CLIENT,
                                   MSG_WRONG_NUMBER_FORMAT,
                                   MSG_WRONG_STATUS,
                                   MSG_CONTRACT_NOT_FOUND,
                                   MSG_WRONG_DATE_FORMAT,
                                   MSG_WRONG_COMMERCIAL_USER,
                                   MSG_WRONG_SUPPORT_USER,
                                   MSG_WRONG_TEAM,
                                   MSG_WRONG_EMPLOYEE_NUMBER,
                                   MSG_EXPIRED_SESSION,
                                   MENU_CLIENTS_LIST_KEYS,
                                   MENU_CLIENTS_LIST_LABEL,
                                   MENU_CLIENTS_DETAILS_KEYS,
                                   MENU_CLIENTS_DETAILS_LABEL,
                                   MENU_CLIENT_UPDATE_KEYS,
                                   MENU_CLIENT_UPDATE_LABEL,
                                   MENU_CLIENT_CREATE_KEYS,
                                   MENU_CLIENT_CREATE_LABEL,
                                   MENU_CONTRACTS_LIST_KEYS,
                                   MENU_CONTRACTS_LIST_LABEL,
                                   MENU_CONTRACTS_DETAILS_KEYS,
                                   MENU_CONTRACTS_DETAILS_LABEL,
                                   MENU_CONTRACT_UPDATE_KEYS,
                                   MENU_CONTRACT_UPDATE_LABEL,
                                   MENU_CONTRACT_CREATE_KEYS,
                                   MENU_CONTRACT_CREATE_LABEL,
                                   MENU_CONTRACT_FILTER_UNPAID_KEYS,
                                   MENU_CONTRACT_FILTER_UNPAID_LABEL,
                                   MENU_CONTRACT_FILTER_UNSIGNED_KEYS,
                                   MENU_CONTRACT_FILTER_UNSIGNED_LABEL,
                                   MENU_EVENTS_LIST_KEYS,
                                   MENU_EVENTS_LIST_LABEL,
                                   MENU_EVENTS_DETAILS_KEYS,
                                   MENU_EVENTS_DETAILS_LABEL,
                                   MENU_EVENT_UPDATE_KEYS,
                                   MENU_EVENT_UPDATE_LABEL,
                                   MENU_EVENT_CREATE_KEYS,
                                   MENU_EVENT_CREATE_LABEL,
                                   MENU_EVENT_FILTER_OWNED_KEYS,
                                   MENU_EVENT_FILTER_OWNED_LABEL,
                                   MENU_EVENT_FILTER_UNASSIGNED_KEYS,
                                   MENU_EVENT_FILTER_UNASSIGNED_LABEL,
                                   MENU_ADMINISTRATION_KEYS,
                                   MENU_ADMINISTRATION_LABEL,
                                   MENU_USER_DETAILS_KEYS,
                                   MENU_USER_DETAILS_LABEL,
                                   MENU_USER_UPDATE_KEYS,
                                   MENU_USER_UPDATE_LABEL,
                                   MENU_USER_CREATE_KEYS,
                                   MENU_USER_CREATE_LABEL,
                                   MENU_EXIT_KEYS,
                                   MENU_EXIT_LABEL,
                                   MENU_RETURN_KEYS,
                                   MENU_RETURN_LABEL,
                                   FOOTER_TITLE,
                                   DATE_FORMAT,
                                   PRPT_CLIENT_LASTNAME,
                                   PRPT_CLIENT_FIRSTNAME,
                                   PRPT_CLIENT_EMAIL,
                                   PRPT_CLIENT_TELEPHONE,
                                   PRPT_CLIENT_ENTERPRISE,
                                   PRPT_CLIENT_COMMERCIAL_ID,
                                   PRPT_CLIENT_CREATION,
                                   PRPT_CLIENT_ID,
                                   PRPT_CONTRACT_TOTAL_AMOUNT,
                                   PRPT_CONTRACT_UNPAID_AMOUNT,
                                   PRPT_CONTRACT_STATUS,
                                   PRPT_CONTRACT_CREATION,
                                   PRPT_EVENT_TITLE,
                                   PRPT_CONTRACT_ID,
                                   PRPT_EVENT_START_DATE,
                                   PRPT_EVENT_END_DATE,
                                   PRPT_EVENT_LOCATION,
                                   PRPT_EVENT_ATTENDEES,
                                   PRPT_EVENT_NOTES,
                                   PRPT_EVENT_SUPPORT_ID,
                                   PRPT_EVENT_CREATION,
                                   PRPT_USER_EMPLOYEE_ID,
                                   PRPT_USER_FIRST_NAME,
                                   PRPT_USER_LAST_NAME,
                                   PRPT_USER_EMAIL,
                                   PRPT_USER_TEAM_ID,
                                   PRPT_USER_PASSWORD,
                                   PRPT_USER_CREATION,
                                   PRPT_ACTIONS,
                                   PRPT_NEW_DATA,
                                   YES_NO_CHOICE,
                                   TITLE_CLIENT_DETAILS,
                                   TITLE_CLIENTS_LISTS,
                                   TITLE_CLIENTS_HOME,
                                   TITLE_CONTRACT_DETAILS,
                                   TITLE_CONTRACTS_LISTS,
                                   TITLE_CONTRACTS_HOME,
                                   TITLE_EVENT_DETAILS,
                                   TITLE_EVENTS_LISTS,
                                   TITLE_EVENTS_HOME,
                                   TITLE_USER_DETAILS,
                                   TITLE_USER_LISTS
                                   )

from views.view_functions import (console)
from .controllers_functions import (navigation_handler,
                                    client_list,
                                    validate_email,
                                    validate_contract,
                                    validate_client,
                                    validate_commercial_user,
                                    validate_employee_number,
                                    validate_support_user,
                                    validate_team,
                                    is_date,
                                    is_float,
                                    prompt_choices_creation,
                                    create_view_setup,
                                    MC_CLIENT_LIST,
                                    MC_CLIENT_DETAILS,
                                    MC_CLIENT_UPDATE,
                                    MC_CLIENT_CREATE,
                                    MC_CONTRACT_LIST,
                                    MC_CONTRACT_DETAILS,
                                    MC_CONTRACT_UPDATE,
                                    MC_CONTRACT_CREATE,
                                    MC_CONTRACT_UNPAID_FILTER,
                                    MC_CONTRACT_UNSIGNED_FILTER,
                                    MC_EVENT_LIST,
                                    MC_EVENT_DETAILS,
                                    MC_EVENT_UPDATE,
                                    MC_EVENT_CREATE,
                                    MC_EVENT_OWNED_FILTER,
                                    MC_EVENT_UNASSIGNED_FILTER,
                                    MC_ADMINISTRATION,
                                    MC_USER_DETAILS,
                                    MC_USER_UPDATE,
                                    MC_USER_CREATE,
                                    MC_EXIT,
                                    MC_RETURN,
                                    MC_INVALID,
                                    MC_ABORT
                                    )

from models.client_dal_functions import (get_client_by_id,
                                         get_all_clients,
                                         update_client,
                                         create_client
                                         )
from models.contract_dal_functions import (get_contract_by_id,
                                           get_all_contracts,
                                           update_contract,
                                           create_contract,
                                           get_unsigned_contracts,
                                           get_unpaid_contracts
                                           )
from models.event_dal_functions import (get_event_by_id,
                                        get_all_events,
                                        update_event,
                                        create_event,
                                        get_event_unassigned,
                                        get_supported_event
                                        )
from models.client_models import Client, CONTRACT_STATUS
from models.user_dal_functions import (get_user_by_id,
                                       get_user_by_email,
                                       get_all_users,
                                       update_user,
                                       create_user,
                                       )
from models.team_dal_functions import (get_team_by_id)
from models.general_dal_functions import get_user_role

from .authorization_functions import (is_client_create_authorized,
                                      is_client_update_authorized,
                                      is_contract_create_authorized,
                                      is_contract_update_authorized,
                                      is_event_create_authorized,
                                      is_event_update_authorized,
                                      is_user_create_authorized,
                                      is_user_read_authorized,
                                      is_user_update_authorized,
                                      MANAGEMENT_ROLE,
                                      COMMERCIAL_ROLE,
                                      SUPPORT_ROLE)

from db import DB_RECORD_NOT_FOUND


class MainController:

    def __init__(self, view, authentication):
        self.screen = view
        self.auth = authentication
        self.no_tokens = {'access': None, 'refresh': None}

    def control_start(self,
                      connected_user,
                      connected_user_role,
                      access_token=None,
                      refresh_token=None):
        """start menu of the aplication"""
        body_data = {}
        actions = []
        prompt = {}
        tokens = {'access': access_token,
                  'refresh': refresh_token
                  }
        view_setup = create_view_setup(None,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       None,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt,
                                       tokens
                                       )

        clients_data = client_list(connected_user.id)
        body_data['clients'] = clients_data
        body_data['clients_title'] = TITLE_CLIENTS_HOME

        contracts_data = []
        for client in clients_data:
            result = get_client_by_id(client.id)
            for contract in result['client'].contracts:
                contracts_data.append(contract)
        body_data['contracts'] = contracts_data
        body_data['contracts_title'] = TITLE_CONTRACTS_HOME

        events_data = []
        for contract in contracts_data:
            result = get_contract_by_id(contract.id)
            for event in result['contract'].events:
                events_data.append(event)
        body_data['events'] = events_data
        body_data['events_title'] = TITLE_EVENTS_HOME

        # actions menu creation, taking role into account
        actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
        actions.append((MENU_CONTRACTS_LIST_KEYS, MENU_CONTRACTS_LIST_LABEL))
        actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
        if is_user_read_authorized(connected_user.id,
                                   connected_user_role):
            actions.append((MENU_ADMINISTRATION_KEYS,
                            MENU_ADMINISTRATION_LABEL))
        actions.append((MENU_CLIENTS_DETAILS_KEYS, MENU_CLIENTS_DETAILS_LABEL))
        actions.append((MENU_CONTRACTS_DETAILS_KEYS,
                        MENU_CONTRACTS_DETAILS_LABEL))
        actions.append((MENU_EVENTS_DETAILS_KEYS, MENU_EVENTS_DETAILS_LABEL))
        actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

        # prompt definition
        prompt['choices'] = prompt_choices_creation(actions)
        prompt['label'] = PRPT_ACTIONS

        choice, token = self.screen.general(view_setup, tokens)

        check_token = self.auth.check_token(token)

        if check_token['status'] == 'ko':
            console.print(MSG_EXPIRED_SESSION)
            time.sleep(2)
            self.login()
        else:

            navigation_handler(self,
                               choice,
                               connected_user,
                               connected_user_role,
                               token)

    #############################
    # clients screens controllers
    #############################

    def control_client_list(self,
                            connected_user,
                            connected_user_role):
        """ client list control"""

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CLIENT_LIST,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CLIENTS_LISTS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_all_clients()

        process_ok = False

        if result['status'] == 'ok':
            body_data['clients'] = result['clients']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['clients'] = []
            process_ok = True

        if process_ok:
            body_data['clients_title'] = TITLE_CLIENTS_LISTS

            # actions menu creation, taking role into account
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CLIENTS_DETAILS_KEYS,
                            MENU_CLIENTS_DETAILS_LABEL))
            if is_client_create_authorized(connected_user.id,
                                           connected_user_role):
                actions.append((MENU_CLIENT_CREATE_KEYS,
                                MENU_CLIENT_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.general(view_setup, self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_client_details(self,
                               client_id,
                               connected_user,
                               connected_user_role):
        """ client detail control"""

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CLIENT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CLIENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_client_by_id(client_id)

        process_ok = False

        if result['status'] == 'ok':
            client = result['client']
            body_data['client'] = client
            result_user = get_user_by_id(client.commercial_contact_id)
            if result_user['status'] == 'ok':
                process_ok = True
                body_data['client_commercial_contact'] = result_user['user']
            else:
                capture_exception(result_user['error'])
                console.print(MSG_ERROR)
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            console.print(MSG_CLIENT_NOT_FOUND)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

        if process_ok:
            body_data['client_title'] = 'Détails du client'

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS,
                            MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CLIENTS_DETAILS_KEYS,
                            MENU_CLIENTS_DETAILS_LABEL))
            if is_client_update_authorized(connected_user.id,
                                           connected_user_role,
                                           client_id):
                actions.append((MENU_CLIENT_UPDATE_KEYS,
                                MENU_CLIENT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.details(view_setup, self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                choice.append(client_id)
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)

    def control_client_update(self,
                              data_id,
                              data_value,
                              client_id,
                              connected_user,
                              connected_user_role,
                              token):
        """ client data update control
        parameter :
        data_id : id of the updated value (from screen layout)
        data_value : new value
        client_id : id of the client to be updated
        return : dictionnary with
        'status'
        'data_id' : if status ok
        'error' : if status ko
        """

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CLIENT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CLIENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_client_by_id(client_id)

        process_ok = False

        if result['status'] == 'ok':
            body_data['client'] = result['client']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            console.print(MSG_CLIENT_NOT_FOUND)
            return

        if process_ok:
            body_data['client_title'] = TITLE_CLIENT_DETAILS

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS,
                            MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CLIENTS_DETAILS_KEYS,
                            MENU_CLIENTS_DETAILS_LABEL))
            if is_client_update_authorized(connected_user.id,
                                           connected_user_role,
                                           client_id):
                actions.append((MENU_CLIENT_UPDATE_KEYS,
                                MENU_CLIENT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            if data_id == '1':
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['first_name'] = data_value

                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '2':
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['last_name'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '3':
                while not validate_email(data_value):
                    prompt['error'] = MSG_WRONG_EMAIL_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['email'] = data_value

                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '4':
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['telephone'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '5':
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['entreprise'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '6':
                while not validate_commercial_user(data_value):
                    prompt['error'] = MSG_WRONG_COMMERCIAL_USER
                    prompt['label'] = PRPT_NEW_DATA
                    data_value = self.screen.details(view_setup,
                                                     self.no_tokens)
                client_dict = {}
                client_dict['id'] = client_id
                client_dict['commercial_contact_id'] = data_value

                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_client(client_dict)
                    if result['status'] == 'ok':
                        self.control_client_details(client_id,
                                                    connected_user,
                                                    connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

    def control_client_create(self,
                              connected_user,
                              connected_user_role):
        """ client create control
        parameter :
        return : dictionnary with
        'status'
        'client_id' : created client id if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}
        client_dict = {}

        view_setup = create_view_setup(MC_CLIENT_CREATE,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CLIENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        prompt['label'] = PRPT_CLIENT_FIRSTNAME
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        client_dict['first_name'] = input_data
        body_data['first_name'] = input_data

        prompt['label'] = PRPT_CLIENT_LASTNAME
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        client_dict['last_name'] = input_data
        body_data['last_name'] = input_data

        prompt['label'] = PRPT_CLIENT_EMAIL
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        while not validate_email(input_data):
            prompt['error'] = MSG_WRONG_EMAIL_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        client_dict['email'] = input_data
        body_data['email'] = input_data

        prompt['label'] = PRPT_CLIENT_TELEPHONE
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        client_dict['telephone'] = input_data
        body_data['telephone'] = input_data

        prompt['label'] = PRPT_CLIENT_ENTERPRISE
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        client_dict['enterprise'] = input_data
        body_data['enterprise'] = input_data

        prompt['label'] = PRPT_CLIENT_CREATION
        prompt['choices'] = YES_NO_CHOICE
        input_data, token = self.screen.creation(view_setup, self.no_tokens)

        # token handling
        check_token = self.auth.check_token(token)

        if check_token['status'] == 'ko':
            console.print(MSG_EXPIRED_SESSION)
            time.sleep(2)
            self.login()
        else:
            if input_data == YES_NO_CHOICE[1]:
                self.control_client_list(connected_user, connected_user_role)
            else:
                client_dict['commercial_contact_id'] = connected_user.id
                client_dict['active'] = True
                result = create_client(client_dict)

                if result['status'] == 'ok':
                    self.control_client_details(result['client_id'],
                                                connected_user,
                                                connected_user_role)
                else:
                    capture_exception(result['error'])
                    console.print(MSG_ERROR)

    ###############################
    # contracts screens controllers
    ###############################

    def control_contract_list(self,
                              connected_user,
                              connected_user_role,
                              type):
        """ contract list control"""

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CONTRACT_LIST,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CONTRACTS_LISTS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )
        if type == MC_CONTRACT_LIST:
            result = get_all_contracts()
        elif type == MC_CONTRACT_UNPAID_FILTER:
            result = get_unpaid_contracts()
        elif type == MC_CONTRACT_UNSIGNED_FILTER:
            result = get_unsigned_contracts()

        process_ok = False

        if result['status'] == 'ok':
            body_data['contracts'] = result['contracts']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['contracts'] = []
            process_ok = True

        if process_ok:
            body_data['contracts_title'] = TITLE_CONTRACTS_LISTS

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CONTRACTS_DETAILS_KEYS,
                            MENU_CONTRACTS_DETAILS_LABEL))
            if is_contract_create_authorized(connected_user.id,
                                             connected_user_role):
                actions.append((MENU_CONTRACT_CREATE_KEYS,
                                MENU_CONTRACT_CREATE_LABEL))
            actions.append((MENU_CONTRACT_FILTER_UNPAID_KEYS,
                            MENU_CONTRACT_FILTER_UNPAID_LABEL))
            actions.append((MENU_CONTRACT_FILTER_UNSIGNED_KEYS,
                            MENU_CONTRACT_FILTER_UNSIGNED_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.general(view_setup, self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_contract_details(self,
                                 contract_id,
                                 connected_user,
                                 connected_user_role):
        """ client detail control"""

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CONTRACT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CONTRACT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_contract_by_id(contract_id)

        if result['status'] == 'ok':
            body_data['contract_title'] = TITLE_CONTRACT_DETAILS

            contract = result['contract']
            body_data['contract'] = contract

            result_client = get_client_by_id(contract.client_id)
            if result_client['status'] == 'ok':
                client = result_client['client']
                body_data['contract_client'] = client
            else:
                capture_exception(result_client['error'])
                console.print(MSG_ERROR)

            result_commercial_contact = get_user_by_id(
                client.commercial_contact_id)
            if result_commercial_contact['status'] == 'ok':
                user = result_commercial_contact['user']
                body_data['contract_commercial_contact'] = user
            else:
                capture_exception(result_commercial_contact['error'])
                console.print(MSG_ERROR)

            if contract.events:
                result_event = get_event_by_id(contract.events[0].id)
                if result_event['status'] == 'ok':
                    event = result_event['event']
                    body_data['contract_event'] = event

                    result_support_contact = get_user_by_id(
                        event.support_contact_id)
                    if result_support_contact['status'] == 'ok':
                        user = result_support_contact['user']
                        body_data['contract_event_support'] = user
                    else:
                        capture_exception(result_support_contact['error'])
                        console.print(MSG_ERROR)
                else:
                    capture_exception(result_event['error'])
                    console.print(MSG_ERROR)

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_contract_update_authorized(connected_user.id,
                                             connected_user_role,
                                             contract_id):
                actions.append((MENU_CONTRACT_UPDATE_KEYS,
                                MENU_CONTRACT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.details(view_setup, self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                choice.append(contract_id)
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_contract_update(self,
                                data_id,
                                data_value,
                                contract_id,
                                connected_user,
                                connected_user_role,
                                token):
        """ contract data update control
        parameter :
        data_id : id of the updated value (from screen layout)
        data_value : new value
        contract_id : id of the contract to be updated
        return : dictionnary with
        'status'
        'data_id' : if status ok
        'error' : if status ko
        """

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_CONTRACT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CONTRACT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_contract_by_id(contract_id)

        if result['status'] == 'ok':
            contract = result['contract']
            body_data['contract'] = contract

            result_client = get_client_by_id(contract.client_id)
            if result_client['status'] == 'ok':
                client = result_client['client']
                body_data['contract_client'] = client
            else:
                capture_exception(result_client['error'])
                console.print(MSG_ERROR)

            result_commercial_contact = get_user_by_id(
                client.commercial_contact_id)
            if result_commercial_contact['status'] == 'ok':
                user = result_commercial_contact['user']
                body_data['contract_commercial_contact'] = user
            else:
                capture_exception(result_commercial_contact['error'])
                console.print(MSG_ERROR)

            if contract.events:
                result_event = get_event_by_id(contract.events[0].id)
                if result_event['status'] == 'ok':
                    event = result_event['event']
                    body_data['contract_event'] = event

                    result_support_contact = get_user_by_id(
                        event.support_contact_id)
                    if result_support_contact['status'] == 'ok':
                        user = result_support_contact['user']
                        body_data['contract_event_support'] = user
                    else:
                        capture_exception(result_support_contact['error'])
                        console.print(MSG_ERROR)
                else:
                    capture_exception(result_event['error'])
                    console.print(MSG_ERROR)

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_contract_update_authorized(connected_user.id,
                                             connected_user_role,
                                             contract_id):
                actions.append((MENU_CONTRACT_UPDATE_KEYS,
                                MENU_CONTRACT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            if data_id == '1':
                while not validate_client(data_value):
                    prompt['error'] = MSG_WRONG_CLIENT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                contract_dict = {}
                contract_dict['id'] = contract_id
                contract_dict['client_id'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_contract(contract_dict)
                    if result['status'] == 'ok':
                        self.control_contract_details(contract_id,
                                                      connected_user,
                                                      connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '2':
                while not is_float(data_value):
                    prompt['error'] = MSG_WRONG_NUMBER_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                contract_dict = {}
                contract_dict['id'] = contract_id
                contract_dict['total_amount'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_contract(contract_dict)
                    if result['status'] == 'ok':
                        self.control_contract_details(contract_id,
                                                      connected_user,
                                                      connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '3':
                while not is_float(data_value):
                    prompt['error'] = MSG_WRONG_NUMBER_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                contract_dict = {}
                contract_dict['id'] = contract_id
                contract_dict['amount_unpaid'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_contract(contract_dict)
                    if result['status'] == 'ok':
                        self.control_contract_details(contract_id,
                                                      connected_user,
                                                      connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '4':
                while not (data_value in CONTRACT_STATUS):
                    prompt['error'] = MSG_WRONG_STATUS
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                contract_dict = {}
                contract_dict['id'] = contract_id
                contract_dict['status'] = data_value
                # token handling
                check_token = self.auth.check_token(token)

                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_contract(contract_dict)
                    if result['status'] == 'ok':
                        message = ("Contract Id: {} status update to : {}"
                                   .format(contract_dict['id'],
                                           contract_dict['status']))
                        capture_message(message)
                        self.control_contract_details(contract_id,
                                                      connected_user,
                                                      connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

    def control_contract_create(self,
                                connected_user,
                                connected_user_role):
        """ control contract creation
        parameter :
        return : dictionnary with
        'status'
        'contract_id' : created contract id if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}
        contract_dict = {}

        view_setup = create_view_setup(MC_CONTRACT_CREATE,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_CONTRACT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        prompt['label'] = PRPT_CLIENT_ID
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        while not validate_client(input_data):
            prompt['error'] = MSG_WRONG_CLIENT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        contract_dict['client_id'] = input_data
        body_data['client_id'] = input_data

        prompt['label'] = PRPT_CONTRACT_TOTAL_AMOUNT
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        while not is_float(input_data):
            prompt['error'] = MSG_WRONG_NUMBER_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        contract_dict['total_amount'] = input_data
        body_data['total_amount'] = input_data

        prompt['label'] = PRPT_CONTRACT_UNPAID_AMOUNT
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        while not is_float(input_data):
            prompt['error'] = MSG_WRONG_NUMBER_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        contract_dict['amount_unpaid'] = input_data
        body_data['amount_unpaid'] = input_data

        prompt['label'] = PRPT_CONTRACT_STATUS
        input_data, token = self.screen.creation(view_setup, self.no_tokens)
        while not (input_data in CONTRACT_STATUS):
            prompt['error'] = MSG_WRONG_STATUS
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        contract_dict['status'] = input_data
        body_data['status'] = input_data

        prompt['label'] = PRPT_CONTRACT_CREATION
        prompt['choices'] = YES_NO_CHOICE
        input_data, token = self.screen.creation(view_setup, self.no_tokens)

        # token handling
        check_token = self.auth.check_token(token)

        if check_token['status'] == 'ko':
            console.print(MSG_EXPIRED_SESSION)
            time.sleep(2)
            self.login()
        else:
            if input_data == YES_NO_CHOICE[1]:
                self.control_contract_list(connected_user, connected_user_role)
            else:
                contract_dict['active'] = True
                result = create_contract(contract_dict)

                if result['status'] == 'ok':
                    self.control_contract_details(result['contract_id'],
                                                  connected_user,
                                                  connected_user_role)
                else:
                    capture_exception(result['error'])
                    console.print(MSG_ERROR)

    ############################
    # events screens controllers
    ############################
    def control_event_list(self,
                           connected_user,
                           connected_user_role,
                           type):
        """ event list control"""

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_EVENT_LIST,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_EVENTS_LISTS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )
        if type == MC_EVENT_LIST:
            result = get_all_events()
        elif type == MC_EVENT_OWNED_FILTER:
            result = get_supported_event(connected_user.id)
        elif type == MC_EVENT_UNASSIGNED_FILTER:
            result = get_event_unassigned()
        process_ok = False

        if result['status'] == 'ok':
            body_data['events'] = result['events']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['events'] = []
            process_ok = True

        if process_ok:
            body_data['events_title'] = TITLE_EVENTS_LISTS

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS,
                            MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_EVENTS_DETAILS_KEYS,
                            MENU_EVENTS_DETAILS_LABEL))
            if is_event_create_authorized(connected_user.id,
                                          connected_user_role):
                actions.append((MENU_EVENT_CREATE_KEYS,
                                MENU_EVENT_CREATE_LABEL))
            if connected_user_role == SUPPORT_ROLE:
                actions.append((MENU_EVENT_FILTER_OWNED_KEYS,
                                MENU_EVENT_FILTER_OWNED_LABEL))
            actions.append((MENU_EVENT_FILTER_UNASSIGNED_KEYS,
                            MENU_EVENT_FILTER_UNASSIGNED_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.general(view_setup,
                                                self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_event_details(self,
                              event_id,
                              connected_user,
                              connected_user_role):
        """ control event details screen """

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_EVENT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_EVENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_event_by_id(event_id)

        if result['status'] == 'ok':
            body_data['event_title'] = TITLE_EVENT_DETAILS

            event = result['event']
            body_data['event'] = event

            result_support_contact = get_user_by_id(
                event.support_contact_id)
            if result_support_contact['status'] == 'ok':
                user = result_support_contact['user']
                body_data['event_support'] = user

            result_contract = get_contract_by_id(event.contract_id)
            contract = result_contract['contract']

            result_client = get_client_by_id(contract.client_id)
            body_data['event_client'] = result_client['client']

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_event_update_authorized(connected_user.id,
                                          connected_user_role,
                                          event_id):
                actions.append((MENU_EVENT_UPDATE_KEYS,
                                MENU_EVENT_UPDATE_LABEL))
            actions.append((MENU_EVENTS_DETAILS_KEYS,
                            MENU_EVENTS_DETAILS_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.details(view_setup, self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                choice.append(event_id)
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_event_update(self,
                             data_id,
                             data_value,
                             event_id,
                             connected_user,
                             connected_user_role,
                             token):
        """ event data update control
        parameter :
        data_id : id of the updated value (from screen layout)
        data_value : new value
        event_id : id of the event to be updated
        token : to validate if update ok
        return : dictionnary with
        'status'
        'data_id' : if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_EVENT_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_EVENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_event_by_id(event_id)

        if result['status'] == 'ok':
            event = result['event']
            body_data['event'] = event

            result_support_contact = get_user_by_id(
                event.support_contact_id)
            if result_support_contact['status'] == 'ok':
                user = result_support_contact['user']
                body_data['event_support'] = user
            else:
                capture_exception(result_support_contact['error'])
                console.print(MSG_ERROR)

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_event_update_authorized(connected_user.id,
                                          connected_user_role,
                                          event_id):
                actions.append((MENU_EVENT_UPDATE_KEYS,
                                MENU_EVENT_UPDATE_LABEL))
            actions.append((MENU_EVENTS_DETAILS_KEYS,
                            MENU_EVENTS_DETAILS_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            if data_id == '1':
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['title'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '2':
                while not validate_contract(data_value):
                    prompt['error'] = MSG_CONTRACT_NOT_FOUND
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['contract_id'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '3':
                while not is_date(data_value):
                    prompt['error'] = MSG_WRONG_DATE_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['start_date'] = datetime.datetime.strptime(
                    data_value, DATE_FORMAT)
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '4':
                while not is_date(data_value):
                    prompt['error'] = MSG_WRONG_DATE_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['end_date'] = datetime.datetime.strptime(
                    data_value, DATE_FORMAT)
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '5':
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['location'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '6':
                while not is_float(data_value):
                    prompt['error'] = MSG_WRONG_NUMBER_FORMAT
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['attendees'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '7':
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['notes'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

            elif data_id == '8':
                while not validate_support_user(data_value):
                    prompt['error'] = MSG_WRONG_SUPPORT_USER
                    prompt['label'] = PRPT_NEW_DATA
                    data_value, token = self.screen.details(view_setup,
                                                            self.no_tokens)
                event_dict = {}
                event_dict['id'] = event_id
                event_dict['support_contact_id'] = data_value
                # token handling
                check_token = self.auth.check_token(token)
                if check_token['status'] == 'ko':
                    console.print(MSG_EXPIRED_SESSION)
                    time.sleep(2)
                    self.login()
                else:
                    result = update_event(event_dict)
                    if result['status'] == 'ok':
                        self.control_event_details(event_id,
                                                   connected_user.id,
                                                   connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)

    def control_event_create(self,
                             connected_user,
                             connected_user_role):
        """ control event creation
        parameter :
        return : dictionnary with
        'status'
        'event_id' : created event if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}
        event_dict = {}

        view_setup = create_view_setup(MC_EVENT_CREATE,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_EVENT_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        prompt['label'] = PRPT_EVENT_TITLE
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        event_dict['title'] = input_data
        body_data['title'] = input_data

        prompt['label'] = PRPT_CONTRACT_ID
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        while not validate_contract(input_data, connected_user.id):
            prompt['error'] = MSG_CONTRACT_NOT_FOUND
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        event_dict['contract_id'] = input_data
        body_data['contract_id'] = input_data

        prompt['label'] = PRPT_EVENT_START_DATE
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        while not is_date(input_data):
            prompt['error'] = MSG_WRONG_DATE_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        event_dict['start_date'] = datetime.datetime.strptime(
            input_data, DATE_FORMAT)
        body_data['start_date'] = input_data

        prompt['label'] = PRPT_EVENT_END_DATE
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        while not is_date(input_data):
            prompt['error'] = MSG_WRONG_DATE_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        event_dict['end_date'] = datetime.datetime.strptime(
            input_data, DATE_FORMAT)
        body_data['end_date'] = input_data

        prompt['label'] = PRPT_EVENT_LOCATION
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        event_dict['location'] = input_data
        body_data['location'] = input_data

        prompt['label'] = PRPT_EVENT_ATTENDEES
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        while not is_float(input_data):
            prompt['error'] = MSG_WRONG_NUMBER_FORMAT
            input_data, token = self.screen.creation(view_setup,
                                                     self.no_tokens)
        prompt.pop('error', None)
        event_dict['attendees'] = input_data
        body_data['attendees'] = input_data

        prompt['label'] = PRPT_EVENT_NOTES
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)
        event_dict['notes'] = input_data
        body_data['notes'] = input_data

        prompt['label'] = PRPT_EVENT_CREATION
        prompt['choices'] = YES_NO_CHOICE
        input_data, token = self.screen.creation(view_setup,
                                                 self.no_tokens)

        # token handling
        check_token = self.auth.check_token(token)

        if check_token['status'] == 'ko':
            console.print(MSG_EXPIRED_SESSION)
            time.sleep(2)
            self.login()
        else:
            if input_data == YES_NO_CHOICE[1]:
                self.control_event_list(connected_user, connected_user_role)
            else:
                event_dict['active'] = True
                event_dict['support_contact_id'] = None
                result = create_event(event_dict)
                if result['status'] == 'ok':
                    self.control_event_details(result['event_id'],
                                               connected_user,
                                               connected_user_role)
                else:
                    capture_exception(result['error'])
                    console.print(MSG_ERROR)

    ################################################
    # user administration events screens controllers
    ################################################
    def control_user_administration(self,
                                    connected_user,
                                    connected_user_role):
        """ user administration homepage """

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_ADMINISTRATION,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_USER_LISTS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_all_users()

        process_ok = False

        if result['status'] == 'ok':
            list_of_users = []
            for user in result['users']:
                result = get_team_by_id(user.team_id)
                team = result['team']
                user_data = [user, team.name]
                list_of_users.append(user_data)
            body_data['users'] = list_of_users
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['users'] = []
            process_ok = True

        if process_ok:
            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
                actions.append((MENU_USER_DETAILS_KEYS,
                                MENU_USER_DETAILS_LABEL))
            if is_user_create_authorized(connected_user.id,
                                         connected_user_role):
                actions.append((MENU_USER_CREATE_KEYS,
                                MENU_USER_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.user_administration(view_setup,
                                                            self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_user_details(self,
                             user_id,
                             connected_user,
                             connected_user_role):
        """ user details display page """

        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_USER_DETAILS,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_USER_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_user_by_id(user_id)

        if result['status'] == 'ok':
            user = result['user']
            body_data['user'] = user

            if user.team_id:
                result_team = get_team_by_id(user.team_id)
                team = result_team['team']
                body_data['user_team'] = team.name
            else:
                body_data['user_team'] = ' '

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_user_update_authorized(connected_user.id,
                                         connected_user_role):
                actions.append((MENU_USER_UPDATE_KEYS,
                                MENU_USER_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            # prompt definition
            prompt['choices'] = prompt_choices_creation(actions)
            prompt['label'] = PRPT_ACTIONS

            choice, token = self.screen.user_details(view_setup,
                                                     self.no_tokens)

            # token handling
            check_token = self.auth.check_token(token)

            if check_token['status'] == 'ko':
                console.print(MSG_EXPIRED_SESSION)
                time.sleep(2)
                self.login()
            else:
                choice.append(user_id)
                navigation_handler(self,
                                   choice,
                                   connected_user,
                                   connected_user_role,
                                   token)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_user_update(self,
                            data_id,
                            data_value,
                            user_id,
                            connected_user,
                            connected_user_role,
                            token):
        """ user data update control
        parameter :
        data_id : id of the updated value (from screen layout)
        data_value : new value
        user_id : id of the user to be updated
        return : dictionnary with
        'status'
        'data_id' : if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}

        view_setup = create_view_setup(MC_USER_UPDATE,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_USER_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        result = get_user_by_id(user_id)

        if result['status'] == 'ok':
            user = result['user']
            body_data['user'] = user

            if user.team_id:
                result_team = get_team_by_id(user.team_id)
                team = result_team['team']
                body_data['user_team'] = team.name
            else:
                body_data['user_team'] = ' '

            # actions menu creation, taking role into account
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user.id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_user_update_authorized(connected_user.id,
                                         connected_user_role):
                actions.append((MENU_USER_UPDATE_KEYS,
                                MENU_USER_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            if is_user_update_authorized(connected_user.id,
                                         connected_user_role):
                if data_id == '1':
                    while not validate_employee_number(data_value):
                        prompt['error'] = MSG_WRONG_EMPLOYEE_NUMBER
                        prompt['label'] = PRPT_NEW_DATA
                        data_value, token = self.screen.user_details(
                            view_setup, self.no_tokens)
                    user_dict = {}
                    user_dict['id'] = user_id
                    user_dict['employee_number'] = data_value
                    # token handling
                    check_token = self.auth.check_token(token)

                    if check_token['status'] == 'ko':
                        console.print(MSG_EXPIRED_SESSION)
                        time.sleep(2)
                        self.login()
                    else:
                        result = update_user(user_dict)
                        if result['status'] == 'ok':
                            message = ("User Id: {} employee_number: {} update"
                                       .format(user_dict['id'],
                                               user_dict['employee_number']))
                            capture_message(message)

                            self.control_user_details(user_id,
                                                      connected_user,
                                                      connected_user_role)
                        else:
                            capture_exception(result['error'])
                            console.print(MSG_ERROR)

                elif data_id == '2':
                    user_dict = {}
                    user_dict['id'] = user_id
                    user_dict['first_name'] = data_value
                    # token handling
                    check_token = self.auth.check_token(token)

                    if check_token['status'] == 'ko':
                        console.print(MSG_EXPIRED_SESSION)
                        time.sleep(2)
                        self.login()
                    else:
                        result = update_user(user_dict)
                        if result['status'] == 'ok':
                            message = ("User Id: {} first_name: {} update"
                                       .format(user_dict['id'],
                                               user_dict['first_name']))
                            capture_message(message)

                            self.control_user_details(user_id,
                                                      connected_user,
                                                      connected_user_role)
                        else:
                            capture_exception(result['error'])
                            console.print(MSG_ERROR)

                elif data_id == '3':
                    user_dict = {}
                    user_dict['id'] = user_id
                    user_dict['last_name'] = data_value
                    # token handling
                    check_token = self.auth.check_token(token)

                    if check_token['status'] == 'ko':
                        console.print(MSG_EXPIRED_SESSION)
                        time.sleep(2)
                        self.login()
                    else:
                        result = update_user(user_dict)
                        if result['status'] == 'ok':
                            message = ("User Id: {} last_name: {} update"
                                       .format(user_dict['id'],
                                               user_dict['last_name']))
                            capture_message(message)

                            self.control_user_details(user_id,
                                                      connected_user,
                                                      connected_user_role)
                        else:
                            capture_exception(result['error'])
                            console.print(MSG_ERROR)

                elif data_id == '4':
                    while not validate_email(data_value):
                        prompt['error'] = MSG_WRONG_EMAIL_FORMAT
                        prompt['label'] = PRPT_NEW_DATA
                        data_value, token = self.screen.user_details(
                            view_setup, self.no_tokens)
                    user_dict = {}
                    user_dict['id'] = user_id
                    user_dict['email'] = data_value
                    # token handling
                    check_token = self.auth.check_token(token)

                    if check_token['status'] == 'ko':
                        console.print(MSG_EXPIRED_SESSION)
                        time.sleep(2)
                        self.login()
                    else:
                        result = update_user(user_dict)
                        if result['status'] == 'ok':
                            message = ("User Id: {} email: {} update"
                                       .format(user_dict['id'],
                                               user_dict['email']))
                            capture_message(message)

                            self.control_user_details(user_id,
                                                      connected_user,
                                                      connected_user_role)
                        else:
                            capture_exception(result['error'])
                            console.print(MSG_ERROR)

                elif data_id == '5':
                    while not validate_team(data_value):
                        prompt['error'] = MSG_WRONG_TEAM
                        prompt['label'] = PRPT_NEW_DATA
                        data_value, token = self.screen.user_details(
                            view_setup, self.no_tokens)
                    user_dict = {}
                    user_dict['id'] = user_id
                    user_dict['team_id'] = data_value
                    # token handling
                    check_token = self.auth.check_token(token)

                    if check_token['status'] == 'ko':
                        console.print(MSG_EXPIRED_SESSION)
                        time.sleep(2)
                        self.login()
                    else:
                        result = update_user(user_dict)
                        if result['status'] == 'ok':
                            message = ("User Id: {} team_id: {} update"
                                       .format(user_dict['id'],
                                               user_dict['team_id']))
                            capture_message(message)

                            self.control_user_details(user_id,
                                                      connected_user,
                                                      connected_user_role)
                        else:
                            capture_exception(result['error'])
                            console.print(MSG_ERROR)
            else:
                capture_message(MSG_WRONG_AUTHORIZATION)
                console.print(MSG_WRONG_AUTHORIZATION)
        else:
            capture_exception(result['error'])
            console.print(MSG_ERROR)

    def control_user_create(self,
                            connected_user,
                            connected_user_role):
        """ control user creation
        parameter :
        return : dictionnary with
        'status'
        'user_id' : created user if status ok
        'error' : if status ko
        """
        set_user({"email": connected_user.email})

        body_data = {}
        actions = []
        prompt = {}
        user_dict = {}

        view_setup = create_view_setup(MC_USER_CREATE,
                                       connected_user.first_name,
                                       connected_user.last_name,
                                       connected_user_role,
                                       TITLE_USER_DETAILS,
                                       body_data,
                                       FOOTER_TITLE,
                                       actions,
                                       prompt
                                       )

        prompt['label'] = PRPT_USER_EMPLOYEE_ID
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        while not validate_employee_number(input_data):
            prompt['error'] = MSG_WRONG_EMPLOYEE_NUMBER
            input_data = self.screen.user_creation(view_setup,
                                                   self.no_tokens)
        prompt.pop('error', None)
        user_dict['employee_number'] = input_data
        body_data['employee_number'] = input_data

        prompt['label'] = PRPT_USER_FIRST_NAME
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        user_dict['first_name'] = input_data
        body_data['first_name'] = input_data

        prompt['label'] = PRPT_USER_LAST_NAME
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        user_dict['last_name'] = input_data
        body_data['last_name'] = input_data

        prompt['label'] = PRPT_USER_EMAIL
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        while not validate_email(input_data):
            prompt['error'] = MSG_WRONG_EMAIL_FORMAT
            input_data = self.screen.user_creation(view_setup,
                                                   self.no_tokens)
        prompt.pop('error', None)
        user_dict['email'] = input_data
        body_data['email'] = input_data

        prompt['label'] = PRPT_USER_TEAM_ID
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        while not validate_team(input_data):
            prompt['error'] = MSG_WRONG_TEAM
            input_data = self.screen.user_creation(view_setup,
                                                   self.no_tokens)
        user_dict['team_id'] = input_data
        body_data['team_id'] = input_data

        prompt['label'] = PRPT_USER_PASSWORD
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)
        user_dict['password'] = input_data
        body_data['password'] = input_data

        prompt['label'] = PRPT_USER_CREATION
        prompt['choices'] = YES_NO_CHOICE
        input_data, token = self.screen.user_creation(view_setup,
                                                      self.no_tokens)

        # token handling
        check_token = self.auth.check_token(token)

        if check_token['status'] == 'ko':
            console.print(MSG_EXPIRED_SESSION)
            time.sleep(2)
            self.login()
        else:
            if input_data == YES_NO_CHOICE[1]:
                self.control_user_administration(connected_user,
                                                 connected_user_role)
            else:
                user_dict['active'] = True
                if is_user_create_authorized(connected_user.id,
                                             connected_user_role):
                    result = create_user(user_dict)
                    if result['status'] == 'ok':
                        message = ("User Id: {} Lastname: {} creation"
                                   .format(result['user_id'],
                                           user_dict['last_name']))
                        capture_message(message)
                        self.control_user_details(result['user_id'],
                                                  connected_user,
                                                  connected_user_role)
                    else:
                        capture_exception(result['error'])
                        console.print(MSG_ERROR)
                else:
                    capture_message(MSG_WRONG_AUTHORIZATION)
                    console.print(MSG_WRONG_AUTHORIZATION)

    ##################
    # controller login
    ##################
    def login(self):

        body_data = {}
        view_setup = {
            'type': 'user_login',
            'body': {
                'data': body_data},
            'footer': {
                'title': 'Actions possibles',
                'actions': []
                }
            }

        result_screen = self.screen.login(view_setup)

        email = result_screen['email']
        password = result_screen['password']
        result = self.auth.password_authentication(email, password)
        if result['status'] == 'ok':
            access_token = result['access']
            refresh_token = result['refresh']

            result_user = get_user_by_email(email)
            user = result_user['user']

            result_role = get_user_role(user.id)
            if result_role['status'] == 'ok':
                user_role = result_role['user_role']
                self.control_start(user,
                                   user_role,
                                   access_token,
                                   refresh_token)
            else:
                capture_exception(result_role['error'])
                console.print(MSG_ERROR)
        else:
            console.print(MSG_ERROR_LOGIN)
            time.sleep(2)
            self.login()

    def exit(self):
        self.screen.exit()

    ##################
    # controller start
    ##################
    def run(self):
        self.login()
