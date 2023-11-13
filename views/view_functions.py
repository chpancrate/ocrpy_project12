import os
import re
import datetime

from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from models.user_dal_functions import get_user_by_id, get_user_by_employee_id
from models.team_dal_functions import get_team_by_id
from models.client_dal_functions import get_client_by_id
from models.contract_dal_functions import get_contract_by_id
from models.client_models import CONTRACT_STATUS

from controllers.authorization_functions import owns_client, owns_event

DATE_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT_DISP = 'JJ/MM/AAAA HH:MM'

# menu choices
MC_CLIENT_LIST = 'client_list'
MC_CLIENT_DETAILS = 'client_details'
MC_CLIENT_UPDATE = 'client_update'
MC_CLIENT_CREATE = 'client_create'

MC_CONTRACT_LIST = 'contracts_list'
MC_CONTRACT_DETAILS = 'contract_details'
MC_CONTRACT_UPDATE = 'contrat_update'
MC_CONTRACT_CREATE = 'contrat_create'

MC_EVENT_LIST = 'events_list'
MC_EVENT_DETAILS = 'event_details'
MC_EVENT_UPDATE = 'event_update'
MC_EVENT_CREATE = 'event_create'

MC_ADMINISTRATION = 'administration'
MC_USER_DETAILS = 'user_details'
MC_USER_UPDATE = 'user_update'
MC_USER_CREATE = 'user_create'

MC_EXIT = 'exit'
MC_RETURN = 'return'
MC_INVALID = 'invalid'
MC_ABORT = 'abort'

# messages
MSG_ERROR = ("une erreur s'est produite veuillez réessayer,\n"
             "si l'erreur persiste contactez votre administrateur")
MSG_CLIENT_NOT_FOUND = 'Le client est inexistant'
MSG_CONTRACT_NOT_FOUND = ('Le contrat est inexistant ou '
                          'est déjà lié à un évènement')
MSG_WRONG_EMAIL_FORMAT = "Le format de l'email est incorrect"
MSG_WRONG_NUMBER_FORMAT = "La donnée doit être nombre"
MSG_WRONG_COMMERCIAL_USER = ("L'utilisateur doit faire partie"
                             " de l'équipe commerciale")
MSG_WRONG_SUPPORT_USER = ("L'utilisateur doit faire partie"
                          " de l'équipe support")
MSG_WRONG_STATUS = 'Le status doit être dans ' + str(CONTRACT_STATUS)
MSG_WRONG_DATE_FORMAT = 'La date doit être dans le format ' + DATE_FORMAT_DISP
MSG_WRONG_TEAM = "L'équipe n'existe pas"
MSG_WRONG_EMPLOYEE_NUMBER = "Matricule déja utilisé"
MSG_ERROR_LOGIN = "email ou mot de passe érronés"
MSG_WRONG_AUTHORIZATION = ("Vous n'avez pas l'autorisation d'effectuer"
                           "cette action")
MSG_WRONG_CLIENT = "Le client est inexistant ou ne vous appartient pas"

# menu items
MENU_CLIENTS_LIST_KEYS = 'c'
MENU_CLIENTS_LIST_LABEL = 'Liste Clients'
MENU_CLIENTS_DETAILS_KEYS = 'dc'
MENU_CLIENTS_DETAILS_LABEL = 'Détails Client'
MENU_CLIENT_UPDATE_KEYS = 'mc'
MENU_CLIENT_UPDATE_LABEL = 'Modifier Client'
MENU_CLIENT_CREATE_KEYS = 'cc'
MENU_CLIENT_CREATE_LABEL = 'Créer Client'

MENU_CONTRACTS_LIST_KEYS = 'o'
MENU_CONTRACTS_LIST_LABEL = 'Liste Contrats'
MENU_CONTRACTS_DETAILS_KEYS = 'do'
MENU_CONTRACTS_DETAILS_LABEL = 'Détails Contrat'
MENU_CONTRACT_UPDATE_KEYS = 'mo'
MENU_CONTRACT_UPDATE_LABEL = 'Modifier Contrat'
MENU_CONTRACT_CREATE_KEYS = 'co'
MENU_CONTRACT_CREATE_LABEL = 'Créer Contrat'

MENU_EVENTS_LIST_KEYS = 'e'
MENU_EVENTS_LIST_LABEL = 'Liste Evènement'
MENU_EVENTS_DETAILS_KEYS = 'de'
MENU_EVENTS_DETAILS_LABEL = 'Détails Evènement'
MENU_EVENT_UPDATE_KEYS = 'me'
MENU_EVENT_UPDATE_LABEL = 'Modifier Evènement'
MENU_EVENT_CREATE_KEYS = 'ce'
MENU_EVENT_CREATE_LABEL = 'Créer Evènement'

MENU_ADMINISTRATION_KEYS = 'a'
MENU_ADMINISTRATION_LABEL = 'Administration'
MENU_USER_DETAILS_KEYS = 'du'
MENU_USER_DETAILS_LABEL = 'Détails utilisateur'
MENU_USER_UPDATE_KEYS = 'mu'
MENU_USER_UPDATE_LABEL = 'Modifier utilisateur'
MENU_USER_CREATE_KEYS = 'cu'
MENU_USER_CREATE_LABEL = 'Créer utilisateur'

MENU_EXIT_KEYS = 's'
MENU_EXIT_LABEL = 'Sortir'
MENU_RETURN_KEYS = 'r'
MENU_RETURN_LABEL = 'Retour'

# footer
FOOTER_TITLE = 'Actions possibles'


def menu_item(code, description):
    """Format string for menu display"""
    item = Text()
    item.append(code, style="bold bright_blue")
    item.append("/", style="bold white")
    item.append(description, style="bold white")
    item.append("  ", style="bold white")
    return item


def screen_layout():
    layout = Layout()
    header_height = 3
    footer_height = 6

    layout.split_column(Layout(name='header'),
                        Layout(name='body'),
                        Layout(name='footer'))

    layout['header'].split_row(Layout(name='logo'),
                               Layout(name='main_menu'))
    layout["main_menu"].size = None
    layout["main_menu"].ratio = 3
    layout['header'].size = header_height

    layout['body'].split_column(Layout(name='clients'),
                                Layout(name='contracts'),
                                Layout(name='events'))

    layout['footer'].size = footer_height
    return layout


def administration_screen_layout():
    layout = Layout()
    header_height = 3
    footer_height = 6

    layout.split_column(Layout(name='header'),
                        Layout(name='body'),
                        Layout(name='footer'))

    layout['header'].split_row(Layout(name='logo'),
                               Layout(name='main_menu'))
    layout["main_menu"].size = None
    layout["main_menu"].ratio = 3
    layout['header'].size = header_height

    layout['footer'].size = footer_height
    return layout


def main_menu_display_create(work_layout):

    logo_str = ("EPIC EVENTS - CRM")
    logo_disp = Padding(logo_str, (1, 1), style="on blue", expand=False)

    main_menu_str = Text()
    main_menu_str.append_text(menu_item(MENU_CLIENTS_LIST_KEYS,
                                        MENU_CLIENTS_LIST_LABEL))
    main_menu_str.append_text(menu_item(MENU_CONTRACTS_LIST_KEYS,
                                        MENU_CONTRACTS_LIST_LABEL))
    main_menu_str.append_text(menu_item(MENU_EVENTS_LIST_KEYS,
                                        MENU_EVENTS_LIST_LABEL))
    main_menu_str.append_text(menu_item(MENU_ADMINISTRATION_KEYS,
                                        MENU_ADMINISTRATION_LABEL))
    main_menu_disp = Padding(main_menu_str, (1, 1))

    work_layout['logo'].update(logo_disp)
    work_layout['main_menu'].update(main_menu_disp)
    return work_layout


def sub_menu_display_create(sub_menu_setup, title):
    sub_menu_str = Text()
    for item in sub_menu_setup:
        sub_menu_str.append_text(menu_item(item[0], item[1]))
    sub_menu_disp = Panel(Padding(sub_menu_str, (1, 1)),
                          style='blue',
                          title=title)
    return sub_menu_disp


def prompt_display_create(prompt_setup):
    choices = []
    for item in prompt_setup['footer']['actions']:
        choices.append(item[0])
    choice = Prompt.ask("Quel est votre choix ?", choices=choices)

    return choice


def prompt_choice_decode(choice1):
    """ decode prompt choice and ask for more information when needed
    """
    if choice1 == MENU_CLIENTS_LIST_KEYS:
        return [MC_CLIENT_LIST]
    elif choice1 == MENU_CLIENTS_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel client désirez vous ?")
        return [MC_CLIENT_DETAILS, choice2]
    elif choice1 == MENU_CLIENT_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(
            "Quelle est la nouvelle valeur?")
        if choice2 == '3':
            while not validate_email(choice3):
                console.print(MSG_WRONG_EMAIL_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '6':
            while not validate_commercial_user(choice3):
                console.print(MSG_WRONG_COMMERCIAL_USER)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        return [MC_CLIENT_UPDATE, choice2, choice3]
    elif choice1 == MENU_CLIENT_CREATE_KEYS:
        return [MC_CLIENT_CREATE]

    elif choice1 == MENU_CONTRACTS_LIST_KEYS:
        return [MC_CONTRACT_LIST]
    elif choice1 == MENU_CONTRACTS_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel contrat désirez vous ")
        return [MC_CONTRACT_DETAILS, choice2]
    elif choice1 == MENU_CONTRACT_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(
            "Quelle est la nouvelle valeur?")
        if choice2 == '1':
            while not validate_client(choice3):
                console.print(MSG_WRONG_CLIENT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '2':
            while not is_float(choice3):
                console.print(MSG_WRONG_NUMBER_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '3':
            while not is_float(choice3):
                console.print(MSG_WRONG_NUMBER_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '4':
            while not (choice3 in CONTRACT_STATUS):
                console.print(MSG_WRONG_STATUS)
                choice3 = Prompt.ask('la valeur doit être dans',
                                     CONTRACT_STATUS)
        return [MC_CONTRACT_UPDATE, choice2, choice3]
    elif choice1 == MENU_CONTRACT_CREATE_KEYS:
        return [MC_CONTRACT_CREATE]

    elif choice1 == MENU_EVENTS_LIST_KEYS:
        return [MC_EVENT_LIST]
    elif choice1 == MENU_EVENTS_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel évènements désirez vous ?")
        return [MC_EVENT_DETAILS, choice2]
    elif choice1 == MENU_EVENT_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(
            "Quelle est la nouvelle valeur?")
        if choice2 == '2':
            while not validate_contract(choice3):
                console.print(MSG_CONTRACT_NOT_FOUND)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '3':
            while not is_date(choice3):
                console.print(MSG_WRONG_DATE_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '4':
            while not is_date(choice3):
                console.print(MSG_WRONG_DATE_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '6':
            while not is_float(choice3):
                console.print(MSG_WRONG_NUMBER_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '8':
            while not validate_support_user(choice3):
                console.print(MSG_WRONG_SUPPORT_USER)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        return [MC_EVENT_UPDATE, choice2, choice3]
    elif choice1 == MENU_EVENT_CREATE_KEYS:
        return [MC_EVENT_CREATE]

    elif choice1 == MENU_ADMINISTRATION_KEYS:
        return [MC_ADMINISTRATION]
    elif choice1 == MENU_USER_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel utilisateur désirez vous ?")
        return [MC_USER_DETAILS, choice2]
    elif choice1 == MENU_USER_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(
            "Quelle est la nouvelle valeur?")
        if choice2 == '1':
            while not validate_employee_number(choice3):
                console.print(MSG_WRONG_EMPLOYEE_NUMBER)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        if choice2 == '4':
            while not validate_email(choice3):
                console.print(MSG_WRONG_EMAIL_FORMAT)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        elif choice2 == '5':
            while not validate_team(choice3):
                console.print(MSG_WRONG_TEAM)
                choice3 = Prompt.ask("Quelle est la nouvelle valeur?")
        return [MC_USER_UPDATE, choice2, choice3]
    elif choice1 == MENU_USER_CREATE_KEYS:
        return [MC_USER_CREATE]

    elif choice1 == "r":
        return [MC_RETURN]
    elif choice1 == "s":
        return [MC_EXIT]


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


def validate_contract(contract_id):
    """
    validate that a contract exist and has no event linked
    parameter :
    contract id
    return :
    boolean
    """
    result = get_contract_by_id(contract_id)
    contract = result['contract']
    if (result['status'] == 'ok' and
       contract.events == []):
        return True
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


def client_creation_prompt_display():
    """
    Prompt for data for client creation
    return :
    dictionnary with client data if user confirms creation
    MC_ABORT if not
    """
    client_data = {}

    data = Prompt.ask("Entrer le nom du client")
    client_data['last_name'] = data

    data = Prompt.ask("Entrer le prénom du client")
    client_data['first_name'] = data

    data = Prompt.ask("Entrer l'email")
    while not validate_email(data):
        console.print(MSG_WRONG_EMAIL_FORMAT)
        data = Prompt.ask("Entrer l'email")
    client_data['email'] = data

    data = Prompt.ask("Entrer le numéro de téléphone")
    client_data['telephone'] = data

    data = Prompt.ask("Entrer le nom de l'entreprise")
    client_data['enterprise'] = data

    data = Prompt.ask("Entrer le numero du contact commercial")
    while not validate_commercial_user(data):
        console.print(MSG_WRONG_COMMERCIAL_USER)
        data = Prompt.ask("Entrer le numero du contact commercial")
    client_data['commercial_contact_id'] = data

    confirmation = Confirm.ask("Voulez-vous créer le client ?",
                               choices=['o', 'n'])

    if confirmation:
        client_data['active'] = True
        return client_data
    else:
        return MC_ABORT


def contract_creation_prompt_display(connected_user_id):
    """
    Prompt for data for contract creation
    return :
    dictionnary with contract data if user confirms creation
    MC_ABORT if not
    """
    contract_data = {}

    client_id = Prompt.ask("Entrer le No du client")
    while not (validate_client(client_id)
               and owns_client(connected_user_id,
                               client_id)):
        console.print(MSG_WRONG_CLIENT)
        client_id = Prompt.ask("Entrer le No du client")
    contract_data['client_id'] = client_id

    total_amount = Prompt.ask("Entrer le montant total du contrat")
    while not is_float(total_amount):
        console.print(MSG_WRONG_NUMBER_FORMAT)
        total_amount = Prompt.ask("Entrer le montant total du contrat")
    contract_data['total_amount'] = total_amount

    amount_unpaid = Prompt.ask("Entrer le montant non payé du contrat")
    while not is_float(amount_unpaid):
        console.print(MSG_WRONG_NUMBER_FORMAT)
        amount_unpaid = Prompt.ask("Entrer le montant non payé du contrat")
    contract_data['amount_unpaid'] = amount_unpaid

    status = Prompt.ask("Entrer le status du contrat")
    while not (status in CONTRACT_STATUS):
        console.print(MSG_WRONG_STATUS)
        status = Prompt.ask("Entrer le status du contrat")
    contract_data['status'] = status

    confirmation = Confirm.ask("Voulez-vous créer le contrat ?",
                               choices=['o', 'n'])

    if confirmation:
        contract_data['active'] = True
        return contract_data
    else:
        return MC_ABORT


def event_creation_prompt_display():
    """
    Prompt for data for event creation
    return :
    dictionnary with event data if user confirms creation
    MC_ABORT if not
    """
    event_data = {}

    title = Prompt.ask("Entrer le titre")
    event_data['title'] = title

    contract_id = Prompt.ask("Entrer le No de contrat")
    while not validate_contract(contract_id):
        console.print(MSG_CONTRACT_NOT_FOUND)
        contract_id = Prompt.ask("Entrer le No de contrat")
    event_data['contract_id'] = contract_id

    start_date = Prompt.ask("Entrer la date et l'heure de début")
    while not is_date(start_date):
        console.print(MSG_WRONG_DATE_FORMAT)
        start_date = Prompt.ask("Entrer la date et l'heure de début")
    event_data['start_date'] = start_date

    end_date = Prompt.ask("Entrer la date et l'heure de fin")
    while not is_date(end_date):
        console.print(MSG_WRONG_DATE_FORMAT)
        end_date = Prompt.ask("Entrer la date et l'heure de fin")
    event_data['end_date'] = end_date

    location = Prompt.ask("Entrer le lieu de l'évènement")
    event_data['location'] = location

    attendees = Prompt.ask("Entrer le nombre de personnes")
    while not is_float(attendees):
        console.print(MSG_WRONG_NUMBER_FORMAT)
        attendees = Prompt.ask("Entrer le nombre de personnes")
    event_data['attendees'] = attendees

    notes = Prompt.ask("Entrer les notes concernant l'évènement")
    event_data['notes'] = notes

    support_contact_id = Prompt.ask("Entrer l'Id de la personne support")
    while not validate_support_user(support_contact_id):
        console.print(MSG_WRONG_SUPPORT_USER)
        support_contact_id = Prompt.ask("Entrer l'Id de la personne support")
    event_data['support_contact_id'] = support_contact_id

    confirmation = Confirm.ask("Voulez-vous créer le contrat ?",
                               choices=['o', 'n'])

    if confirmation:
        event_data['active'] = True
        return event_data
    else:
        return MC_ABORT


def user_creation_prompt_display():
    """
    Prompt for data for user creation
    return :
    dictionnary with user data if user confirms creation
    MC_ABORT if not
    """
    user_data = {}

    employee_number = Prompt.ask("Entrer le Matricule")
    while not validate_employee_number(employee_number):
        console.print(MSG_WRONG_EMPLOYEE_NUMBER)
        employee_number = Prompt.ask("Entrer le Matricule")
    user_data['employee_number'] = employee_number

    first_name = Prompt.ask("Entrer le prénom")
    user_data['first_name'] = first_name

    last_name = Prompt.ask("Entrer le nom")
    user_data['last_name'] = last_name

    email = Prompt.ask("Entrer l'email")
    while not validate_email(email):
        console.print(MSG_WRONG_EMAIL_FORMAT)
        email = Prompt.ask("Entrer l'email")
    user_data['email'] = email

    team_id = Prompt.ask("Entrer le numéro d'équipe")
    while not validate_team(team_id):
        console.print(MSG_WRONG_TEAM)
        team_id = Prompt.ask("Entrer le numéro d'équipe")
    user_data['team_id'] = team_id

    password = Prompt.ask("Entrer le mot de passe")
    user_data['password'] = password

    confirmation = Confirm.ask("Voulez-vous créer le contrat ?",
                               choices=['o', 'n'])

    if confirmation:
        user_data['active'] = True
        return user_data
    else:
        return MC_ABORT


def display_date(date):
    if date is None:
        return ' '
    else:
        return date.strftime(DATE_FORMAT)


def clear_screen():
    os.system("cls")
    pass


console = Console()
