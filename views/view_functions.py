import os
import re
import datetime

from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align

from models.user_dal_functions import get_user_by_id, get_user_by_employee_id
from models.team_dal_functions import get_team_by_id
from models.client_dal_functions import get_client_by_id
from models.contract_dal_functions import get_contract_by_id
from models.client_models import CONTRACT_STATUS

from controllers.authorization_functions import owns_client, owns_event
from controllers.controllers_functions import (MC_CLIENT_LIST,
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
from controllers.constants import (MSG_ERROR,
                                   MSG_CLIENT_NOT_FOUND,
                                   MSG_ERROR_LOGIN,
                                   MSG_WRONG_AUTHORIZATION,
                                   MSG_CONTRACT_NOT_FOUND,
                                   MSG_WRONG_CLIENT,
                                   MSG_WRONG_COMMERCIAL_USER,
                                   MSG_WRONG_DATE_FORMAT,
                                   MSG_WRONG_EMAIL_FORMAT,
                                   MSG_WRONG_EMPLOYEE_NUMBER,
                                   MSG_WRONG_NUMBER_FORMAT,
                                   MSG_WRONG_STATUS,
                                   MSG_WRONG_SUPPORT_USER,
                                   MSG_WRONG_TEAM,
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
                                   MENU_CONTRACT_FILTER_UNSIGNED_KEYS,
                                   MENU_CONTRACT_FILTER_UNPAID_KEYS,
                                   MENU_EVENTS_LIST_KEYS,
                                   MENU_EVENTS_LIST_LABEL,
                                   MENU_EVENTS_DETAILS_KEYS,
                                   MENU_EVENTS_DETAILS_LABEL,
                                   MENU_EVENT_UPDATE_KEYS,
                                   MENU_EVENT_UPDATE_LABEL,
                                   MENU_EVENT_CREATE_KEYS,
                                   MENU_EVENT_CREATE_LABEL,
                                   MENU_EVENT_FILTER_OWNED_KEYS,
                                   MENU_EVENT_FILTER_UNASSIGNED_KEYS,
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
                                   PRPT_NEW_DATA
                                   )

CLIENT_COLOR = 'green'
CONTRACT_COLOR = 'yellow'
EVENT_COLOR = 'cyan'
USER_COLOR = 'red'

console = Console()


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


def header_display_create(work_layout,
                          user_first_name,
                          user_last_name,
                          user_role):

    logo_str = ("EPIC EVENTS - CRM")
    logo_disp = Padding(logo_str, (1, 1), style="on blue", expand=False)

    header_str = (user_first_name
                  + ' '
                  + user_last_name
                  + ', role: '
                  + user_role)
    centered_header_str = Align.center(header_str)
    header_disp = Padding(centered_header_str, (1, 1))

    work_layout['logo'].update(logo_disp)
    work_layout['main_menu'].update(header_disp)
    return work_layout


def login_header_display_create(work_layout):

    logo_str = ("EPIC EVENTS - CRM")
    logo_disp = Padding(logo_str, (1, 1), style="on blue", expand=False)

    header_str = "Customer Relationship Management System"
    centered_header_str = Align.center(header_str)
    header_disp = Padding(centered_header_str, (1, 1))

    work_layout['logo'].update(logo_disp)
    work_layout['main_menu'].update(header_disp)
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
        choice3 = Prompt.ask(PRPT_NEW_DATA)
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
        choice3 = Prompt.ask(PRPT_NEW_DATA)
        return [MC_CONTRACT_UPDATE, choice2, choice3]
    elif choice1 == MENU_CONTRACT_CREATE_KEYS:
        return [MC_CONTRACT_CREATE]
    elif choice1 == MENU_CONTRACT_FILTER_UNPAID_KEYS:
        return [MC_CONTRACT_UNPAID_FILTER]
    elif choice1 == MENU_CONTRACT_FILTER_UNSIGNED_KEYS:
        return [MC_CONTRACT_UNSIGNED_FILTER]

    elif choice1 == MENU_EVENTS_LIST_KEYS:
        return [MC_EVENT_LIST]
    elif choice1 == MENU_EVENTS_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel évènements désirez vous ?")
        return [MC_EVENT_DETAILS, choice2]
    elif choice1 == MENU_EVENT_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(PRPT_NEW_DATA)
        return [MC_EVENT_UPDATE, choice2, choice3]
    elif choice1 == MENU_EVENT_CREATE_KEYS:
        return [MC_EVENT_CREATE]
    elif choice1 == MENU_EVENT_FILTER_OWNED_KEYS:
        return [MC_EVENT_OWNED_FILTER]
    elif choice1 == MENU_EVENT_FILTER_UNASSIGNED_KEYS:
        return [MC_EVENT_UNASSIGNED_FILTER]

    elif choice1 == MENU_ADMINISTRATION_KEYS:
        return [MC_ADMINISTRATION]
    elif choice1 == MENU_USER_DETAILS_KEYS:
        choice2 = Prompt.ask("Quel utilisateur désirez vous ?")
        return [MC_USER_DETAILS, choice2]
    elif choice1 == MENU_USER_UPDATE_KEYS:
        choice2 = Prompt.ask(
            "Quelle donnée voulez vous modifier (No situé devant)?")
        choice3 = Prompt.ask(PRPT_NEW_DATA)
        return [MC_USER_UPDATE, choice2, choice3]
    elif choice1 == MENU_USER_CREATE_KEYS:
        return [MC_USER_CREATE]

    elif choice1 == "r":
        return [MC_RETURN]
    elif choice1 == "s":
        return [MC_EXIT]


def display_date(date):
    if date is None:
        return ' '
    else:
        return date.strftime(DATE_FORMAT)


def clear_screen():
    # os.system("cls")
    pass


def display_prompt(prompt):

    if 'error' in prompt:
        console.print(prompt['error'])

    if 'choices' in prompt:
        choice = Prompt.ask(prompt['label'],
                            choices=prompt['choices'])
    else:
        choice = Prompt.ask(prompt['label'])

    return choice
