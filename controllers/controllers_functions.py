from views.view_functions import (console,
                                  MC_ADMINISTRATION,
                                  MC_USER_DETAILS,
                                  MC_USER_UPDATE,
                                  MC_USER_CREATE,
                                  MC_CLIENT_DETAILS,
                                  MC_CLIENT_LIST,
                                  MC_CLIENT_UPDATE,
                                  MC_CLIENT_CREATE,
                                  MC_CONTRACT_DETAILS,
                                  MC_CONTRACT_LIST,
                                  MC_CONTRACT_UPDATE,
                                  MC_CONTRACT_CREATE,
                                  MC_EVENT_DETAILS,
                                  MC_EVENT_LIST,
                                  MC_EVENT_UPDATE,
                                  MC_EVENT_CREATE,
                                  MC_EXIT)
from models.user_dal_functions import get_client_list_for_user


def application_exit():
    console.print("Au revoir")


def navigation_handler(controller, choice, connected_user_id, connected_user_role):
    if choice[0] == MC_EXIT:
        application_exit()

    elif choice[0] == MC_CLIENT_LIST:
        controller.control_client_list(connected_user_id, connected_user_role)
    elif choice[0] == MC_CLIENT_DETAILS:
        controller.control_client_details(choice[1], connected_user_id, connected_user_role)
    elif choice[0] == MC_CLIENT_UPDATE:
        controller.control_client_update(choice[1], choice[2], choice[3], connected_user_id, connected_user_role)
    elif choice[0] == MC_CLIENT_CREATE:
        controller.control_client_create(connected_user_id, connected_user_role)

    elif choice[0] == MC_CONTRACT_LIST:
        controller.control_contract_list(connected_user_id, connected_user_role)
    elif choice[0] == MC_CONTRACT_DETAILS:
        controller.control_contract_details(choice[1], connected_user_id, connected_user_role)
    elif choice[0] == MC_CONTRACT_UPDATE:
        controller.control_contract_update(choice[1], choice[2], choice[3], connected_user_id, connected_user_role)
    elif choice[0] == MC_CONTRACT_CREATE:
        controller.control_contract_create(connected_user_id, connected_user_role)

    elif choice[0] == MC_EVENT_LIST:
        controller.control_event_list(connected_user_id, connected_user_role)
    elif choice[0] == MC_EVENT_DETAILS:
        controller.control_event_details(choice[1], connected_user_id, connected_user_role)
    elif choice[0] == MC_EVENT_UPDATE:
        controller.control_event_update(choice[1], choice[2], choice[3], connected_user_id, connected_user_role)
    elif choice[0] == MC_EVENT_CREATE:
        controller.control_event_create(connected_user_id, connected_user_role)

    elif choice[0] == MC_ADMINISTRATION:
        controller.control_user_administration(connected_user_id, connected_user_role)
    elif choice[0] == MC_USER_DETAILS:
        controller.control_user_details(choice[1], connected_user_id, connected_user_role)
    elif choice[0] == MC_USER_UPDATE:
        controller.control_user_update(choice[1], choice[2], choice[3], connected_user_id, connected_user_role)
    elif choice[0] == MC_USER_CREATE:
        controller.control_user_create(connected_user_id, connected_user_role)


def client_list(user_id):

    result = get_client_list_for_user(user_id)
    if result['status'] == 'ok':
        data = result['data']
    return data
