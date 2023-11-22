import os
from dotenv import load_dotenv

from rich.console import Console
from rich.layout import Layout
from rich.text import Text
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

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
                                               )
from controllers.constants import (MENU_CLIENTS_LIST_KEYS,
                                   MENU_CLIENTS_DETAILS_KEYS,
                                   MENU_CLIENT_UPDATE_KEYS,
                                   MENU_CLIENT_CREATE_KEYS,
                                   MENU_CONTRACTS_LIST_KEYS,
                                   MENU_CONTRACTS_DETAILS_KEYS,
                                   MENU_CONTRACT_UPDATE_KEYS,
                                   MENU_CONTRACT_CREATE_KEYS,
                                   MENU_CONTRACT_FILTER_UNSIGNED_KEYS,
                                   MENU_CONTRACT_FILTER_UNPAID_KEYS,
                                   MENU_EVENTS_LIST_KEYS,
                                   MENU_EVENTS_DETAILS_KEYS,
                                   MENU_EVENT_UPDATE_KEYS,
                                   MENU_EVENT_CREATE_KEYS,
                                   MENU_EVENT_FILTER_OWNED_KEYS,
                                   MENU_EVENT_FILTER_UNASSIGNED_KEYS,
                                   MENU_ADMINISTRATION_KEYS,
                                   MENU_USER_DETAILS_KEYS,
                                   MENU_USER_UPDATE_KEYS,
                                   MENU_USER_CREATE_KEYS,
                                   DATE_FORMAT,
                                   PRPT_NEW_DATA
                                   )

load_dotenv()

clear_screen_setup = os.getenv("CLEAR_SCREEN")

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
    """ create general screen layout :
    header
        logo main_menu
    body
        clients
        contracts
        events
    footer
    """

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
    """ create user administration screen layout :
    header
        logo main_menu
    body
    footer
    """
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
    """ create screen header """
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
    """ create login screen header """

    logo_str = ("EPIC EVENTS - CRM")
    logo_disp = Padding(logo_str, (1, 1), style="on blue", expand=False)

    header_str = "Customer Relationship Management System"
    centered_header_str = Align.center(header_str)
    header_disp = Padding(centered_header_str, (1, 1))

    work_layout['logo'].update(logo_disp)
    work_layout['main_menu'].update(header_disp)
    return work_layout


def sub_menu_display_create(sub_menu_setup, title):
    """ create submenu displyed in the footer """
    sub_menu_str = Text()
    for item in sub_menu_setup:
        sub_menu_str.append_text(menu_item(item[0], item[1]))
    sub_menu_disp = Panel(Padding(sub_menu_str, (1, 1)),
                          style='blue',
                          title=title)
    return sub_menu_disp


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
    """ format date for display purpose"""

    if date is None:
        return ' '
    else:
        return date.strftime(DATE_FORMAT)


def clear_screen():
    """ clear screen
    used before screen display, can be disabled in .env file
    """

    if clear_screen_setup == 'true':
        os.system("cls")
    else:
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
