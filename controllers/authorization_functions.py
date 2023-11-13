from models.user_dal_functions import get_user_by_id
from models.contract_dal_functions import get_contract_by_id
from models.event_dal_functions import get_event_by_id

MANAGEMENT_ROLE = 'gestion'
COMMERCIAL_ROLE = 'commercial'
SUPPORT_ROLE = 'support'


def owns_client(user_id, client_id):
    result = get_user_by_id(user_id)
    if result['status'] == 'ok':
        user = result['user']
        client_found = False
        for client in user.clients:
            if client_id == client.id:
                client_found = True
                break

        if client_found:
            return True
        else:
            return False
    else:
        return False


def owns_event(user_id, event_id):
    result = get_user_by_id(user_id)
    if result['status'] == 'ok':
        user = result['user']
        event_found = False
        for event in user.events:
            if event_id == event.id:
                event_found = True
                break

        if event_found:
            return True
        else:
            return False
    else:
        return False


def is_client_create_authorized(user_id, user_role):
    # Rules :
    # user in commercial team
    if user_role == COMMERCIAL_ROLE:
        return True
    else:
        return False


def is_client_update_authorized(user_id, user_role, client_id):
    # Rules :
    # user in commercial team
    # AND
    # user owns client
    if user_role == COMMERCIAL_ROLE:
        if owns_client(user_id, client_id):
            return True
        else:
            return False
    else:
        return False


def is_contract_create_authorized(user_id, user_role):
    # Rules :
    # user in management team
    if user_role == MANAGEMENT_ROLE:
        return True
    else:
        return False


def is_contract_update_authorized(user_id, user_role, contract_id):
    # Rules :
    # user in management team
    # OR
    #   user in commercial team
    #   AND
    #   user owns client
    if user_role == MANAGEMENT_ROLE:
        return True
    elif user_role == COMMERCIAL_ROLE:
        result = get_contract_by_id(contract_id)
        if result['status'] == 'ok':
            client_id = result['contract'].client_id
            if owns_client(user_id, client_id):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def is_event_create_authorized(user_id, user_role):
    # Rules :
    # user commercial team
    # AND
    # user own client (checked at creation prompt)
    if user_role == COMMERCIAL_ROLE:
        return True
    else:
        return False


def is_event_upd_authorized(user_id, user_role, event_id):
    # Rules :
    # user in management team
    # OR
    #   user in commercial team
    #   AND
    #   user owns client
    # OR
    #   user in support team
    #   AND
    #   user owns client
    if user_role == MANAGEMENT_ROLE:
        return True
    elif user_role == COMMERCIAL_ROLE:
        result_event = get_event_by_id(event_id)

        result_contract = get_contract_by_id(result_event['event'].contract_id)
        client_id = result_contract['contract'].client_id

        if owns_client(user_id, client_id):
            return True
        else:
            return False
    elif user_role == SUPPORT_ROLE:
        if owns_event(user_id, event_id):
            return True
        else:
            return False
    else:
        return False


def is_user_read_authorized(user_id, user_role):
    # Rules :
    # user in management team
    if user_role == MANAGEMENT_ROLE:
        return True
    else:
        return False


def is_user_create_authorized(user_id, user_role):
    # Rules :
    # user in management team
    if user_role == MANAGEMENT_ROLE:
        return True
    else:
        return False


def is_user_update_authorized(user_id, user_role):
    # Rules :
    # user in management team
    if user_role == MANAGEMENT_ROLE:
        return True
    else:
        return False
