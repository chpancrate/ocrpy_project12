import datetime
import re

from models.user_dal_functions import (get_client_list_for_user,
                                       get_user_by_id,
                                       get_user_by_employee_id
                                       )
from models.client_models import CONTRACT_STATUS
from models.client_dal_functions import get_client_by_id
from models.contract_dal_functions import get_contract_by_id
from models.team_dal_functions import get_team_by_id

from controllers.constants import DATE_FORMAT

# menu choices
MC_CLIENT_LIST = 'client_list'
MC_CLIENT_DETAILS = 'client_details'
MC_CLIENT_UPDATE = 'client_update'
MC_CLIENT_CREATE = 'client_create'

MC_CONTRACT_LIST = 'contracts_list'
MC_CONTRACT_DETAILS = 'contract_details'
MC_CONTRACT_UPDATE = 'contrat_update'
MC_CONTRACT_CREATE = 'contrat_create'
MC_CONTRACT_UNPAID_FILTER = 'contrat_unpaid_filter'
MC_CONTRACT_UNSIGNED_FILTER = 'contrat_unsigned_filter'

MC_EVENT_LIST = 'events_list'
MC_EVENT_DETAILS = 'event_details'
MC_EVENT_UPDATE = 'event_update'
MC_EVENT_CREATE = 'event_create'
MC_EVENT_OWNED_FILTER = 'event_owned_filter'
MC_EVENT_UNASSIGNED_FILTER = 'event_unassigned_filter'

MC_ADMINISTRATION = 'administration'
MC_USER_DETAILS = 'user_details'
MC_USER_UPDATE = 'user_update'
MC_USER_CREATE = 'user_create'

MC_EXIT = 'exit'
MC_RETURN = 'return'
MC_INVALID = 'invalid'
MC_ABORT = 'abort'


def navigation_handler(controller,
                       choice,
                       connected_user,
                       connected_user_role,
                       token):
    if choice[0] == MC_EXIT:
        controller.exit()

    if choice[0] == MC_RETURN:
        controller.control_start(connected_user, connected_user_role)

    elif choice[0] == MC_CLIENT_LIST:
        controller.control_client_list(connected_user,
                                       connected_user_role)
    elif choice[0] == MC_CLIENT_DETAILS:
        controller.control_client_details(choice[1],
                                          connected_user,
                                          connected_user_role)
    elif choice[0] == MC_CLIENT_UPDATE:
        controller.control_client_update(choice[1],
                                         choice[2],
                                         choice[3],
                                         connected_user,
                                         connected_user_role,
                                         token)
    elif choice[0] == MC_CLIENT_CREATE:
        controller.control_client_create(connected_user,
                                         connected_user_role)

    elif choice[0] == MC_CONTRACT_LIST:
        controller.control_contract_list(connected_user,
                                         connected_user_role,
                                         MC_CONTRACT_LIST)
    elif choice[0] == MC_CONTRACT_DETAILS:
        controller.control_contract_details(choice[1],
                                            connected_user,
                                            connected_user_role)
    elif choice[0] == MC_CONTRACT_UPDATE:
        controller.control_contract_update(choice[1],
                                           choice[2],
                                           choice[3],
                                           connected_user,
                                           connected_user_role,
                                           token)
    elif choice[0] == MC_CONTRACT_CREATE:
        controller.control_contract_create(connected_user,
                                           connected_user_role)
    elif choice[0] == MC_CONTRACT_UNPAID_FILTER:
        controller.control_contract_list(connected_user,
                                         connected_user_role,
                                         MC_CONTRACT_UNPAID_FILTER)
    elif choice[0] == MC_CONTRACT_UNSIGNED_FILTER:
        controller.control_contract_list(connected_user,
                                         connected_user_role,
                                         MC_CONTRACT_UNSIGNED_FILTER)

    elif choice[0] == MC_EVENT_LIST:
        controller.control_event_list(connected_user,
                                      connected_user_role,
                                      MC_EVENT_LIST)
    elif choice[0] == MC_EVENT_DETAILS:
        controller.control_event_details(choice[1],
                                         connected_user,
                                         connected_user_role)
    elif choice[0] == MC_EVENT_UPDATE:
        controller.control_event_update(choice[1],
                                        choice[2],
                                        choice[3],
                                        connected_user,
                                        connected_user_role,
                                        token)
    elif choice[0] == MC_EVENT_CREATE:
        controller.control_event_create(connected_user, connected_user_role)
    elif choice[0] == MC_EVENT_OWNED_FILTER:
        controller.control_event_list(connected_user,
                                      connected_user_role,
                                      MC_EVENT_OWNED_FILTER)
    elif choice[0] == MC_EVENT_UNASSIGNED_FILTER:
        controller.control_event_list(connected_user,
                                      connected_user_role,
                                      MC_EVENT_UNASSIGNED_FILTER)

    elif choice[0] == MC_ADMINISTRATION:
        controller.control_user_administration(connected_user,
                                               connected_user_role)
    elif choice[0] == MC_USER_DETAILS:
        controller.control_user_details(choice[1],
                                        connected_user,
                                        connected_user_role)
    elif choice[0] == MC_USER_UPDATE:
        controller.control_user_update(choice[1],
                                       choice[2],
                                       choice[3],
                                       connected_user,
                                       connected_user_role,
                                       token)
    elif choice[0] == MC_USER_CREATE:
        controller.control_user_create(connected_user,
                                       connected_user_role)


def client_list(user_id):

    result = get_client_list_for_user(user_id)
    if result['status'] == 'ok':
        data = result['data']
    return data


def validate_email(email):
    """
    validate email format
    parameter :
    email to be validated
    return
    boolean
    """
    email_regex = r'[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}'
    if re.fullmatch(email_regex, email) is None:
        return False
    else:
        return True


def validate_commercial_user(user_id):
    """
    validate that a user is in the commercial team
    parameter :
    user id
    return :
    boolean
    """
    result = get_user_by_id(user_id)
    if (result['status'] == 'ok'
       and result['user'].team_id == 2):
        return True
    else:
        return False


def validate_support_user(user_id):
    """
    validate that a user is in the support team
    parameter :
    user id
    return :
    boolean
    """
    result = get_user_by_id(user_id)
    if (result['status'] == 'ok'
       and result['user'].team_id == 3):
        return True
    else:
        return False


def validate_employee_number(employee_number):
    """
    validate that an employee number is not already used
    parameter :
    user id
    return :
    True if nummber not in database False if it is
    """
    result = get_user_by_employee_id(employee_number)
    if result['status'] == 'ok':
        return False
    else:
        return True


def validate_client(client_id):
    """
    validate that a client exist
    parameter :
    client id
    return :
    boolean
    """
    result = get_client_by_id(client_id)
    if result['status'] == 'ok':
        return True
    else:
        return False


def validate_contract(contract_id, user_id):
    """
    validate that a contract:
     - exist 
     - has no event linked
     - is for a client of the user
     - is signed
    contract id
    return :
    boolean
    """
    result_contract = get_contract_by_id(contract_id)

    if (result_contract['status'] == 'ok' and
       result_contract['contract'].events == [] and
       result_contract['contract'].status == CONTRACT_STATUS[0]):

        result_client = get_client_by_id(result_contract['contract'].client_id)

        if (result_client['status'] == 'ok' and
           result_client['client'].commercial_contact_id == user_id):

            return True
        else:
            return False
    else:
        return False


def validate_team(team_id):
    """
    validate that a team exist
    parameter :
    client id
    return :
    boolean
    """
    result = get_team_by_id(team_id)
    if result['status'] == 'ok':
        return True
    else:
        return False


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_date(date):
    try:
        datetime.datetime.strptime(date, DATE_FORMAT)
        return True
    except ValueError:
        return False


def prompt_choices_creation(menu_list):
    choices = []
    for menu_item in menu_list:
        choices.append(menu_item[0])

    return choices


def create_view_setup(type,
                      user_first_name,
                      user_last_name,
                      user_role,
                      body_title,
                      body_data,
                      footer_title,
                      actions,
                      prompt,
                      tokens=None):
    view_setup = {
        'type': type,
        'header': {
            'user_first_name': user_first_name,
            'user_last_name': user_last_name,
            'user_role': user_role
        },
        'body': {
            'title': body_title,
            'data': body_data},
        'footer': {
            'title': footer_title,
            'actions': actions
            },
        'prompt': prompt,
        'tokens': tokens
        }

    return view_setup
