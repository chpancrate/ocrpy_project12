import datetime

from views.view_functions import (console,
                                  MC_RETURN,
                                  MC_ABORT,
                                  MSG_ERROR,
                                  MSG_CLIENT_NOT_FOUND,
                                  MSG_ERROR_LOGIN,
                                  MSG_WRONG_AUTHORIZATION,
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
                                  MENU_EVENTS_LIST_KEYS,
                                  MENU_EVENTS_LIST_LABEL,
                                  MENU_EVENTS_DETAILS_KEYS,
                                  MENU_EVENTS_DETAILS_LABEL,
                                  MENU_EVENT_UPDATE_KEYS,
                                  MENU_EVENT_UPDATE_LABEL,
                                  MENU_EVENT_CREATE_KEYS,
                                  MENU_EVENT_CREATE_LABEL,
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
                                  DATE_FORMAT
                                  )
from .controllers_functions import (navigation_handler,
                                    client_list)

from models.client_dal_functions import (get_client_by_id,
                                         get_all_clients,
                                         update_client,
                                         create_client
                                         )
from models.contract_dal_functions import (get_contract_by_id,
                                           get_all_contracts,
                                           update_contract,
                                           create_contract
                                           )
from models.event_dal_functions import (get_event_by_id,
                                        get_all_events,
                                        update_event,
                                        create_event
                                        )
from models.client_models import Client
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
                                      is_event_upd_authorized,
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

    def control_start(self,
                      connected_user_id,
                      connected_user_role,
                      access_token,
                      refresh_token):
        """start menu of the aplication"""
        body_data = {}

        clients_data = client_list(connected_user_id)
        body_data['clients'] = clients_data
        body_data['clients_title'] = 'Vos clients'

        contracts_data = []
        for client in clients_data:
            result = get_client_by_id(client.id)
            for contract in result['client'].contracts:
                contracts_data.append(contract)
        body_data['contracts'] = contracts_data
        body_data['contracts_title'] = 'Vos contrats'

        events_data = []
        for contract in contracts_data:
            result = get_contract_by_id(contract.id)
            for event in result['contract'].events:
                events_data.append(event)
        body_data['events'] = events_data
        body_data['events_title'] = 'Vos évènements'

        # actions menu creation, taking role into account
        actions = []
        actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
        actions.append((MENU_CONTRACTS_LIST_KEYS, MENU_CONTRACTS_LIST_LABEL))
        actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
        if is_user_read_authorized(connected_user_id,
                                   connected_user_role):
            actions.append((MENU_ADMINISTRATION_KEYS,
                            MENU_ADMINISTRATION_LABEL))
        actions.append((MENU_CLIENTS_DETAILS_KEYS, MENU_CLIENTS_DETAILS_LABEL))
        actions.append((MENU_CONTRACTS_DETAILS_KEYS,
                        MENU_CONTRACTS_DETAILS_LABEL))
        actions.append((MENU_EVENTS_DETAILS_KEYS, MENU_EVENTS_DETAILS_LABEL))
        actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

        view_setup = {
            'body': {
                'data': body_data},
            'footer': {
                'title': FOOTER_TITLE,
                'actions': actions
                }
            }

        choice = self.screen.general(view_setup)

        navigation_handler(self, choice, connected_user_id, connected_user_role)

    #############################
    # clients screens controllers
    #############################

    def control_client_list(self,
                            connected_user_id,
                            connected_user_role):
        """ client list control"""

        body_data = {}

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
            body_data['clients_title'] = 'Liste des clients'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CLIENTS_DETAILS_KEYS,
                            MENU_CLIENTS_DETAILS_LABEL))
            if is_client_create_authorized(connected_user_id,
                                           connected_user_role):
                actions.append((MENU_CLIENT_CREATE_KEYS,
                                MENU_CLIENT_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))
            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.general(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_client_details(self,
                               client_id,
                               connected_user_id,
                               connected_user_role):
        """ client detail control"""

        body_data = {}

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
            body_data['client_title'] = 'Détails du client'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS,
                            MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CLIENTS_DETAILS_KEYS,
                            MENU_CLIENTS_DETAILS_LABEL))
            if is_client_update_authorized(connected_user_id,
                                           connected_user_role):
                actions.append((MENU_CLIENT_UPDATE_KEYS,
                                MENU_CLIENT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.details(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                choice.append(client_id)
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_client_update(self,
                              data_id,
                              data_value,
                              client_id,
                              connected_user_id,
                              connected_user_role):
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

        if data_id == '1':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['first_name'] = data_value
            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '2':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['last_name'] = data_value
            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '3':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['email'] = data_value
            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '4':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['telephone'] = data_value
            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '5':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['entreprise'] = data_value
            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '6':
            client_dict = {}
            client_dict['id'] = client_id
            client_dict['commercial_contact_id'] = data_value

            result = update_client(client_dict)
            if result['status'] == 'ok':
                self.control_client_details(client_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

    def control_client_create(self,
                              connected_user_id,
                              connected_user_role):
        """ client create control
        parameter :
        return : dictionnary with
        'status'
        'client_id' : created client id if status ok
        'error' : if status ko
        """
        body_data = {}
        view_setup = {
            'type': 'client_creation',
            'body': {
                'data': body_data},
            'footer': {
                'title': FOOTER_TITLE,
                'actions': []
                }
            }

        result_screen = self.screen.creation(view_setup)

        if result_screen == MC_ABORT:
            self.control_client_list(connected_user_id, connected_user_role)
        else:
            client_dict = result_screen
            result = create_client(client_dict)

            if result['status'] == 'ok':
                self.control_client_details(result['client_id'], connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

    ###############################
    # contracts screens controllers
    ###############################

    def control_contract_list(self,
                              connected_user_id,
                              connected_user_role):
        """ contract list control"""

        body_data = {}

        result = get_all_contracts()

        process_ok = False

        if result['status'] == 'ok':
            body_data['contracts'] = result['contracts']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['contracts'] = []
            process_ok = True

        if process_ok:
            body_data['contracts_title'] = 'Liste des contrats'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_CONTRACTS_DETAILS_KEYS,
                            MENU_CONTRACTS_DETAILS_LABEL))
            if is_contract_create_authorized(connected_user_id,
                                             connected_user_role):
                actions.append((MENU_CONTRACT_CREATE_KEYS,
                                MENU_CONTRACT_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.general(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_contract_details(self,
                                 contract_id,
                                 connected_user_id,
                                 connected_user_role):
        """ client detail control"""

        body_data = {}

        result = get_contract_by_id(contract_id)

        if result['status'] == 'ok':
            contract = result['contract']
            body_data['contract'] = contract

            result_client = get_client_by_id(contract.client_id)
            if result_client['status'] == 'ok':
                client = result_client['client']
                body_data['contract_client'] = client
            else:
                console.print(MSG_ERROR)

            result_commercial_contact = get_user_by_id(
                client.commercial_contact_id)
            if result_commercial_contact['status'] == 'ok':
                user = result_commercial_contact['user']
                body_data['contract_commercial_contact'] = user
            else:
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
                        console.print(MSG_ERROR)
                else:
                    console.print(MSG_ERROR)

            body_data['contract_title'] = 'Détails du contrat'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_contract_update_authorized(connected_user_id,
                                             connected_user_role,
                                             contract_id):
                actions.append((MENU_CONTRACT_UPDATE_KEYS,
                                MENU_CONTRACT_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.details(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                choice.append(contract_id)
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_contract_update(self,
                                data_id,
                                data_value,
                                contract_id,
                                connected_user_id,
                                connected_user_role):
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

        if data_id == '1':
            contract_dict = {}
            contract_dict['id'] = contract_id
            contract_dict['client_id'] = data_value
            result = update_contract(contract_dict)
            if result['status'] == 'ok':
                self.control_contract_details(contract_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '2':
            contract_dict = {}
            contract_dict['id'] = contract_id
            contract_dict['total_amount'] = data_value
            result = update_contract(contract_dict)
            if result['status'] == 'ok':
                self.control_contract_details(contract_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '3':
            contract_dict = {}
            contract_dict['id'] = contract_id
            contract_dict['amount_unpaid'] = data_value
            result = update_contract(contract_dict)
            if result['status'] == 'ok':
                self.control_contract_details(contract_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '4':
            contract_dict = {}
            contract_dict['id'] = contract_id
            contract_dict['status'] = data_value
            result = update_contract(contract_dict)
            if result['status'] == 'ok':
                self.control_contract_details(contract_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

    def control_contract_create(self,
                                connected_user_id,
                                connected_user_role):
        """ control contract creation
        parameter :
        return : dictionnary with
        'status'
        'contract_id' : created contract id if status ok
        'error' : if status ko
        """
        body_data = {}
        view_setup = {
            'type': 'contract_creation',
            'body': {
                'data': body_data},
            'footer': {
                'title': 'Actions possibles',
                'actions': []
                }
            }

        result_screen = self.screen.creation(view_setup)

        if result_screen == MC_ABORT:
            self.control_contract_list(connected_user_id, connected_user_role)
        else:
            contract_dict = result_screen
            result = create_contract(contract_dict)

            if result['status'] == 'ok':
                self.control_contract_details(result['contract_id'], connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

    ############################
    # events screens controllers
    ############################
    def control_event_list(self,
                           connected_user_id,
                           connected_user_role):
        """ event list control"""

        body_data = {}

        result = get_all_events()

        process_ok = False

        if result['status'] == 'ok':
            body_data['events'] = result['events']
            process_ok = True
        elif (result['status'] == 'ko'
              and result['error'] == DB_RECORD_NOT_FOUND):
            body_data['events'] = []
            process_ok = True

        if process_ok:
            body_data['events_title'] = 'Liste des évènements'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS,
                            MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            actions.append((MENU_EVENTS_DETAILS_KEYS,
                            MENU_EVENTS_DETAILS_LABEL))
            if is_event_create_authorized(connected_user_id,
                                          connected_user_role):
                actions.append((MENU_EVENT_CREATE_KEYS,
                                MENU_EVENT_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.general(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_event_details(self,
                              event_id,
                              connected_user_id,
                              connected_user_role):
        """ control event details screen """

        body_data = {}

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
                console.print(MSG_ERROR)

            body_data['event_title'] = "Détails de l'évènement"

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_event_upd_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_EVENT_UPDATE_KEYS,
                                MENU_EVENT_UPDATE_LABEL))
            actions.append((MENU_EVENTS_DETAILS_KEYS,
                            MENU_EVENTS_DETAILS_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.details(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                choice.append(event_id)
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_event_update(self,
                             data_id,
                             data_value,
                             event_id,
                             connected_user_id,
                             connected_user_role):
        """ event data update control
        parameter :
        data_id : id of the updated value (from screen layout)
        data_value : new value
        event_id : id of the event to be updated
        return : dictionnary with
        'status'
        'data_id' : if status ok
        'error' : if status ko
        """

        if data_id == '1':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['title'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '2':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['contract_id'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)
        elif data_id == '3':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['start_date'] = datetime.datetime.strptime(data_value,
                                                                  DATE_FORMAT)
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '4':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['end_date'] = datetime.datetime.strptime(data_value,
                                                                DATE_FORMAT)
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '5':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['location'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '6':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['attendees'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '7':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['notes'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

        elif data_id == '8':
            event_dict = {}
            event_dict['id'] = event_id
            event_dict['support_contact_id'] = data_value
            result = update_event(event_dict)
            if result['status'] == 'ok':
                self.control_event_details(event_id, connected_user_id, connected_user_role)
            else:
                console.print(MSG_ERROR)

    def control_event_create(self,
                             connected_user_id,
                             connected_user_role):
        """ control event creation
        parameter :
        return : dictionnary with
        'status'
        'event_id' : created event if status ok
        'error' : if status ko
        """
        body_data = {}
        view_setup = {
            'type': 'event_creation',
            'body': {
                'data': body_data},
            'footer': {
                'title': 'Actions possibles',
                'actions': []
                }
            }

        result_screen = self.screen.creation(view_setup)

        if result_screen == MC_ABORT:
            self.control_event_list(connected_user_id, connected_user_role)
        else:
            event_dict = result_screen
            event_dict['start_date'] = datetime.datetime.strptime(
                event_dict['start_date'], DATE_FORMAT)
            event_dict['end_date'] = datetime.datetime.strptime(
                event_dict['end_date'], DATE_FORMAT)
            if connected_user_role == COMMERCIAL_ROLE:
                result = create_event(event_dict)
                if result['status'] == 'ok':
                    self.control_event_details(result['event_id'], connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)
            else:
                console.print(MSG_WRONG_AUTHORIZATION)

    ################################################
    # user administration events screens controllers
    ################################################
    def control_user_administration(self,
                                    connected_user_id,
                                    connected_user_role):
        """ user administration homepage """

        body_data = {}

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
            body_data['users_title'] = 'Liste des utilisateurs'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
                actions.append((MENU_USER_DETAILS_KEYS,
                                MENU_USER_DETAILS_LABEL))
            if is_user_create_authorized(connected_user_id,
                                         connected_user_role):
                actions.append((MENU_USER_CREATE_KEYS,
                                MENU_USER_CREATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.user_administration(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_user_details(self,
                             user_id,
                             connected_user_id,
                             connected_user_role):
        """ user update page """

        body_data = {}

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

            body_data['user_title'] = 'Détails utilisateur'

            # actions menu creation, taking role into account
            actions = []
            actions.append((MENU_CLIENTS_LIST_KEYS, MENU_CLIENTS_LIST_LABEL))
            actions.append((MENU_CONTRACTS_LIST_KEYS,
                            MENU_CONTRACTS_LIST_LABEL))
            actions.append((MENU_EVENTS_LIST_KEYS, MENU_EVENTS_LIST_LABEL))
            if is_user_read_authorized(connected_user_id,
                                       connected_user_role):
                actions.append((MENU_ADMINISTRATION_KEYS,
                                MENU_ADMINISTRATION_LABEL))
            if is_user_update_authorized(connected_user_id,
                                         connected_user_role):
                actions.append((MENU_USER_UPDATE_KEYS,
                                MENU_USER_UPDATE_LABEL))
            actions.append((MENU_RETURN_KEYS, MENU_RETURN_LABEL))
            actions.append((MENU_EXIT_KEYS, MENU_EXIT_LABEL))

            view_setup = {
                'body': {
                    'data': body_data},
                'footer': {
                    'title': FOOTER_TITLE,
                    'actions': actions
                    }
                }

            choice = self.screen.user_details(view_setup)
            if choice[0] == MC_RETURN:
                console.print('retour')
                pass
            else:
                choice.append(user_id)
                navigation_handler(self, choice, connected_user_id, connected_user_role)
        else:
            console.print(MSG_ERROR)

    def control_user_update(self,
                            data_id,
                            data_value,
                            user_id,
                            connected_user_id,
                            connected_user_role):
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

        if connected_user_role == MANAGEMENT_ROLE:
            if data_id == '1':
                user_dict = {}
                user_dict['id'] = user_id
                user_dict['employee_number'] = data_value
                result = update_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(user_id, connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)

            elif data_id == '2':
                user_dict = {}
                user_dict['id'] = user_id
                user_dict['first_name'] = data_value
                result = update_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(user_id, connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)

            elif data_id == '3':
                user_dict = {}
                user_dict['id'] = user_id
                user_dict['last_name'] = data_value
                result = update_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(user_id, connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)

            elif data_id == '4':
                user_dict = {}
                user_dict['id'] = user_id
                user_dict['email'] = data_value
                result = update_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(user_id, connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)

            elif data_id == '5':
                user_dict = {}
                user_dict['id'] = user_id
                user_dict['team_id'] = data_value
                result = update_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(user_id, connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)
        else:
            console.print(MSG_WRONG_AUTHORIZATION)

    def control_user_create(self,
                            connected_user_id,
                            connected_user_role):
        """ control user creation
        parameter :
        return : dictionnary with
        'status'
        'user_id' : created user if status ok
        'error' : if status ko
        """
        body_data = {}
        view_setup = {
            'type': 'user_creation',
            'body': {
                'data': body_data},
            'footer': {
                'title': 'Actions possibles',
                'actions': []
                }
            }

        result_screen = self.screen.user_creation(view_setup)

        if result_screen == MC_ABORT:
            self.control_user_administration(connected_user_id, connected_user_role)
        else:
            user_dict = result_screen
            if connected_user_role == MANAGEMENT_ROLE:
                result = create_user(user_dict)
                if result['status'] == 'ok':
                    self.control_user_details(result['user_id'], connected_user_id, connected_user_role)
                else:
                    console.print(MSG_ERROR)
            else:
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
            user_id = result_user['user'].id

            result_role = get_user_role(user_id)
            if result_role['status'] == 'ok':
                user_role = result_role['user_role']
                self.control_start(user_id,
                                   user_role,
                                   access_token,
                                   refresh_token)
            else:
                console.print(MSG_ERROR)
        else:
            console.print(MSG_ERROR_LOGIN)
            self.login()

    ##################
    # controller start
    ##################
    def run(self):
        self.login()
