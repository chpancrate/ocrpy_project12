import os

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from .view_functions import (
    console,
    header_display_create,
    login_header_display_create,
    sub_menu_display_create,
    prompt_display_create,
    prompt_choice_decode,
    screen_layout,
    administration_screen_layout,
    clear_screen,
    display_date,
    display_prompt,
    CLIENT_COLOR,
    CONTRACT_COLOR,
    EVENT_COLOR,
    USER_COLOR
)

from controllers.controllers_functions import (MC_CLIENT_CREATE,
                                               MC_CLIENT_DETAILS,
                                               MC_CLIENT_UPDATE,
                                               MC_CONTRACT_CREATE,
                                               MC_CONTRACT_DETAILS,
                                               MC_CONTRACT_UPDATE,
                                               MC_EVENT_CREATE,
                                               MC_EVENT_DETAILS,
                                               MC_EVENT_UPDATE,
                                               MC_USER_UPDATE,
                                               MC_USER_DETAILS)
# reduce console size to allow prompt
OFFSET_HEIGHT = 2
CONSOLE_SIZE = console.height - OFFSET_HEIGHT
console.height = CONSOLE_SIZE


class Screen:
    def __init__(self, authentication):
        self.auth = authentication

    def token_process(func):
        """ decorator
        processes token before calling the function
        if token received from controller (when login) store them
        else
        retrieve stored access token
        if access token valid send it with the result of the functions
        if not, refresh it and send the new token with the fucntion result
        if refresh impossible send the old token
        (will force a login from the controller)
        """

        def wrapper(self, *args, **kwargs):

            tokens = args[1]
            if tokens['access'] is not None:
                self.auth.save_tokens_to_file(tokens)

            result = func(self, args[0])

            stored_tokens = self.auth.get_tokens_from_file()

            check_access = self.auth.check_token(stored_tokens['access'])
            if check_access['status'] == 'ok':
                # print('XXX-TokP: check_access ok')
                token = stored_tokens['access']
            else:
                # print('XXX-TokP: check_access ko')
                check_refresh = self.auth.check_token(stored_tokens['refresh'])
                if check_refresh['status'] == 'ok':
                    # print('XXX-TokP: check_refresh ok')
                    get_refresh = self.auth.request_token_with_refresh(
                        stored_tokens['refresh'])
                    if get_refresh['status'] == 'ok':
                        # print('XXX-TokP: get_refresh_ok')
                        token = get_refresh['access']
                    else:
                        # print('XXX-TokP: get_refresh_ko')
                        token = stored_tokens['access']
                else:
                    # print('XXX-TokP: check_refresh ko')
                    token = stored_tokens['access']

            return result, token

        return wrapper

    @token_process
    def general(self, view_setup):
        """display the start screen"""

        clear_screen()

        layout = screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        # clients list
        if "clients" in view_setup["body"]["data"]:
            clients_data = view_setup["body"]["data"]["clients"]

            table = Table(box=None)

            table.add_column("No",
                             justify="center",
                             no_wrap=True,
                             style="white")
            table.add_column("Prénom",
                             justify="left",
                             no_wrap=True,
                             style="white")
            table.add_column("Nom",
                             justify="left",
                             no_wrap=True,
                             style="white")
            table.add_column("Entreprise",
                             justify="left",
                             no_wrap=True,
                             style="white")

            for client in clients_data:
                table.add_row(
                    str(client.id),
                    client.first_name,
                    client.last_name,
                    client.enterprise,
                )
            centered_table = Align.center(table)
            list_disp = Panel(
                centered_table,
                style=CLIENT_COLOR,
                title=view_setup["body"]["data"]["clients_title"],
            )
            disp_layout["clients"].update(list_disp)
        else:
            disp_layout["clients"].visible = False

        # contracts list
        if "contracts" in view_setup["body"]["data"]:
            contracts_data = view_setup["body"]["data"]["contracts"]
            table = Table(box=None)

            table.add_column("No",
                             justify="center",
                             no_wrap=True,
                             style="white")
            table.add_column("Client No",
                             justify="left",
                             no_wrap=True,
                             style="white")
            table.add_column("Montant total",
                             justify="left",
                             no_wrap=True,
                             style="white")
            table.add_column("Montant non payé",
                             justify="left",
                             no_wrap=True,
                             style="white")
            table.add_column("status",
                             justify="left",
                             no_wrap=True,
                             style="white")

            for contract in contracts_data:
                table.add_row(
                    str(contract.id),
                    str(contract.client_id),
                    str(contract.total_amount),
                    str(contract.amount_unpaid),
                    contract.status,
                )
            centered_table = Align.center(table)
            list_disp = Panel(
                centered_table,
                style=CONTRACT_COLOR,
                title=view_setup["body"]["data"]["contracts_title"],
            )
            disp_layout["contracts"].update(list_disp)
        else:
            disp_layout["contracts"].visible = False

        # event lists
        if "events" in view_setup["body"]["data"]:
            events_data = view_setup["body"]["data"]["events"]
            table = Table(box=None)

            table.add_column(
                "No", justify="center", no_wrap=True, style="white")
            table.add_column(
                "Titre", justify="left", no_wrap=True, style="white")
            table.add_column(
                "No contrat", justify="left", no_wrap=True, style="white")
            table.add_column(
                "Date début", justify="left", no_wrap=True, style="white")
            table.add_column(
                "Date fin", justify="left", no_wrap=True, style="white")
            table.add_column(
                "Lieu", justify="left", no_wrap=True, style="white")
            table.add_column(
                "Nb de personnes", justify="left", no_wrap=True, style="white"
            )

            for event in events_data:
                table.add_row(
                    str(event.id),
                    event.title,
                    str(event.contract_id),
                    display_date(event.start_date),
                    display_date(event.end_date),
                    event.location,
                    str(event.attendees),
                )

            centered_table = Align.center(table)
            list_disp = Panel(
                centered_table,
                style=EVENT_COLOR,
                title=view_setup["body"]["data"]["events_title"],
            )

            disp_layout["events"].update(list_disp)
        else:
            disp_layout["events"].visible = False

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        choice = display_prompt(view_setup['prompt'])

        return prompt_choice_decode(choice)

    @token_process
    def details(self, view_setup):
        """display the details screen"""

        clear_screen()

        layout = screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        # client display
        if "client" in view_setup["body"]["data"]:
            client = view_setup["body"]["data"]["client"]
            commercial_contact = (view_setup["body"]
                                  ["data"]['client_commercial_contact'])

            # client details
            table_client = Table(box=None, show_header=False, title="Client")

            table_client.add_column(
                "Item", justify="left", no_wrap=True, style=CLIENT_COLOR)
            table_client.add_column(
                "Separator", justify="left", no_wrap=True, style=CLIENT_COLOR)
            table_client.add_column(
                "Value", justify="left", no_wrap=True, style="white")

            table_client.add_row("    No", ":", str(client.id))
            table_client.add_row("(1) Prénom", ":", client.first_name)
            table_client.add_row("(2) Nom", ":", client.last_name)
            table_client.add_row("(3) Email", ":", client.email)
            table_client.add_row("(4) Telephone", ":", client.telephone)
            table_client.add_row("(5) Entreprise", ":", client.enterprise)
            table_client.add_row("(6) Id Contact", ":",
                                 str(client.commercial_contact_id))
            table_client.add_row("    Nom Contact", ":",
                                 commercial_contact.full_name())
            table_client.add_row("    Date de Création",
                                 ":",
                                 display_date(client.creation_date))
            table_client.add_row("    Date de mise à jour",
                                 ":",
                                 display_date(client.last_update))

            centered_table_client = Align.center(table_client)

            # contracts list
            contracts_data = client.contracts
            table_contracts = Table(
                box=None, show_header=True, title="Contrats")

            table_contracts.add_column("No",
                                       justify="center",
                                       no_wrap=True,
                                       style="white")
            table_contracts.add_column("Client No",
                                       justify="left",
                                       no_wrap=True,
                                       style="white")
            table_contracts.add_column("Montant total",
                                       justify="left",
                                       no_wrap=True,
                                       style="white")
            table_contracts.add_column("Montant non payé",
                                       justify="left",
                                       no_wrap=True,
                                       style="white")
            table_contracts.add_column("status",
                                       justify="left",
                                       no_wrap=True,
                                       style="white")

            for contract in contracts_data:
                table_contracts.add_row(
                    str(contract.id),
                    str(contract.client_id),
                    str(contract.total_amount),
                    str(contract.amount_unpaid),
                    contract.status,
                )
            centered_table_contracts = Align.center(table_contracts)

            # screen display
            table_group = Group(
                centered_table_client, " ", " ", centered_table_contracts
            )
            client_disp = Panel(table_group,
                                style=CLIENT_COLOR,
                                title=(view_setup['body']
                                       ['data']['client_title'])
                                )
            disp_layout["clients"].update(client_disp)
        else:
            disp_layout["clients"].visible = False

        # contract display
        if "contract" in view_setup["body"]["data"]:
            contract = view_setup["body"]["data"]["contract"]
            client = view_setup["body"]["data"]["contract_client"]
            commercial_contact = (view_setup["body"]
                                  ["data"]["contract_commercial_contact"])
            if 'contract_event' in view_setup["body"]["data"]:
                event = view_setup["body"]["data"]["contract_event"]
            if 'contract_event_support' in view_setup["body"]["data"]:
                event_support = (view_setup["body"]
                                 ["data"]["contract_event_support"])

            # contract details
            table_contract = Table(box=None,
                                   show_header=False,
                                   title="Contrat")

            table_contract.add_column("Item",
                                      justify="left",
                                      no_wrap=True,
                                      style=CONTRACT_COLOR)
            table_contract.add_column("Separator",
                                      justify="left",
                                      no_wrap=True,
                                      style=CONTRACT_COLOR)
            table_contract.add_column("Value",
                                      justify="left",
                                      no_wrap=True,
                                      style="white")

            table_contract.add_row(
                "    No", ":", str(contract.id))
            table_contract.add_row(
                "(1) No Client", ":", str(contract.client_id))
            table_contract.add_row(
                "    Nom Complet", ":", client.full_name())
            table_contract.add_row(
                "    Telephone", ":", client.telephone)
            table_contract.add_row(
                "    Email", ":", client.email)
            table_contract.add_row(
                "    Contact Commercial", ":", commercial_contact.full_name())
            table_contract.add_row(
                "(2) Montant total", ":", str(contract.total_amount))
            table_contract.add_row(
                "(3) Montant non payé", ":", str(contract.amount_unpaid))
            table_contract.add_row(
                "(4) status", ":", contract.status)
            table_contract.add_row("    Date de Création",
                                   ":",
                                   display_date(contract.creation_date))
            table_contract.add_row("    Date de mise à jour",
                                   ":",
                                   display_date(contract.last_update))

            centered_table_contract = Align.center(table_contract)

            # contract event details
            table_event = Table(box=None, show_header=False, title="Evènement")

            table_event.add_column("Item",
                                   justify="left",
                                   no_wrap=True,
                                   style=CONTRACT_COLOR)
            table_event.add_column("Separator",
                                   justify="left",
                                   no_wrap=True,
                                   style=CONTRACT_COLOR)
            table_event.add_column("Value",
                                   justify="left",
                                   no_wrap=True,
                                   style="white")
            
            if "contract_event" in view_setup["body"]["data"]:
                table_event.add_row(
                    "Titre", ":", event.title)
                table_event.add_row(
                    "Débute le", ":", display_date(event.start_date))
                table_event.add_row(
                    "Se termine le", ":", display_date(event.end_date))
                table_event.add_row(
                    "Lieu", ":", event.location)
                table_event.add_row(
                    "Nombre de personnes", ":", str(event.attendees))
                table_event.add_row(
                    "Notes", ":", str(event.notes))

                centered_table_event = Align.center(table_event)

                # Event Support contact
                support_contact_disp = Text()
                support_contact_disp.append('Contact support: ')
                if 'contract_event_support' in view_setup["body"]["data"]:
                    support_contact_disp.append(event_support.full_name(),
                                                style='white')

                centered_support_contact_disp = Align.center(
                    support_contact_disp)
            else:
                # display is empty
                table_event.add_row(
                    "Titre", ":", "")
                table_event.add_row(
                    "Débute le", ":", "")
                table_event.add_row(
                    "Se termine le", ":", "")
                table_event.add_row(
                    "Lieu", ":", "")
                table_event.add_row(
                    "Nombre de personnes", ":", "")
                table_event.add_row(
                    "Notes", ":", "")

                centered_table_event = Align.center(table_event)

                # Event Support contact
                support_contact_disp = Text()
                support_contact_disp.append('Contact support: ')

                centered_support_contact_disp = Align.center(
                    support_contact_disp)

            # screen display
            table_group = Group(
                centered_table_contract,
                " ",
                " ",
                centered_table_event,
                " ",
                centered_support_contact_disp
            )
            contract_disp = Panel(table_group,
                                  style=CONTRACT_COLOR,
                                  title=(view_setup['body']
                                         ['data']['contract_title'])
                                  )
            disp_layout["contracts"].update(contract_disp)
        else:
            disp_layout["contracts"].visible = False

        # event display
        if "event" in view_setup["body"]["data"]:
            event = view_setup["body"]["data"]['event']
            event_client = view_setup["body"]["data"]['event_client']

            table_event = Table(box=None, show_header=False, title="Evènement")

            table_event.add_column(
                "Item", justify="left", no_wrap=True, style=EVENT_COLOR)
            table_event.add_column(
                "Separator", justify="left", no_wrap=True, style=EVENT_COLOR)
            table_event.add_column(
                "Value", justify="left", no_wrap=True, style="white")

            table_event.add_row(
                "(1) Titre", ":", event.title)
            table_event.add_row(
                "    Id", ":", str(event.id))
            table_event.add_row(
                "(2) No Contrat", ":", str(event.contract_id))
            table_event.add_row(
                "    Client", ":", event_client.full_name())
            table_event.add_row(
                "    Telephone", ":", event_client.telephone)
            table_event.add_row(
                "    Email", ":", event_client.email)
            table_event.add_row(
                "(3) Débute le", ":", display_date(event.start_date))
            table_event.add_row(
                "(4) Se termine le", ":", display_date(event.end_date))
            table_event.add_row(
                "(5) Lieu", ":", event.location)
            table_event.add_row(
                "(6) Nombre de personnes", ":", str(event.attendees))
            table_event.add_row(
                "(7) Notes", ":", event.notes)
            if event.support_contact_id is not None:
                table_event.add_row(
                    "(8) No Contact Support",
                    ":",
                    str(event.support_contact_id))
                event_support = view_setup["body"]["data"]['event_support']
                table_event.add_row(
                    "    Nom Contact Support",
                    ":",
                    event_support.full_name())
            else:
                table_event.add_row(
                    "(8) No Contact Support",
                    ":",
                    " ")
                table_event.add_row(
                    "    Nom Contact Support",
                    ":",
                    " ")

            centered_table_event = Align.center(table_event)

            # screen display
            event_disp = Panel(centered_table_event,
                               style=EVENT_COLOR,
                               title=(view_setup['body']
                                      ['data']['event_title'])
                               )
            disp_layout["events"].update(event_disp)

        else:
            disp_layout["events"].visible = False

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        if view_setup['type'] in [MC_CLIENT_DETAILS,
                                  MC_CONTRACT_DETAILS,
                                  MC_EVENT_DETAILS]:
            choice = display_prompt(view_setup['prompt'])
            return prompt_choice_decode(choice)
        elif view_setup['type'] == [MC_CLIENT_UPDATE,
                                    MC_CONTRACT_UPDATE,
                                    MC_EVENT_UPDATE]:
            input_data = display_prompt(view_setup['prompt'])
            return input_data

    @token_process
    def creation(self, view_setup):
        """display the creation screen"""

        clear_screen()

        console.height = 20
        layout = screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        body_data = view_setup['body']['data']

        if view_setup['type'] == MC_CLIENT_CREATE:
            table_client = Table(box=None,
                                 show_header=False,
                                 )

            table_client.add_column("Item",
                                    justify="left",
                                    no_wrap=True,
                                    style=CLIENT_COLOR)
            table_client.add_column("Separator",
                                    justify="left",
                                    no_wrap=True,
                                    style=CLIENT_COLOR)
            table_client.add_column("Value",
                                    justify="left",
                                    no_wrap=True,
                                    style="white")

            if 'first_name' in body_data:
                first_name = body_data['first_name']
            else:
                first_name = ' '
            table_client.add_row("Prénom",
                                 ":",
                                 first_name)

            if 'last_name' in body_data:
                last_name = body_data['last_name']
            else:
                last_name = ' '
            table_client.add_row("Nom",
                                 ":",
                                 last_name)

            if 'email' in body_data:
                email = body_data['email']
            else:
                email = ' '
            table_client.add_row("Email",
                                 ":",
                                 email)

            if 'telephone' in body_data:
                telephone = body_data['telephone']
            else:
                telephone = ' '
            table_client.add_row("Telephone",
                                 ":",
                                 telephone)

            if 'entreprise' in body_data:
                entreprise = body_data['entreprise']
            else:
                entreprise = ' '
            table_client.add_row("Entreprise",
                                 ":",
                                 entreprise)

            centered_table_client = Align.center(table_client)
            client_disp = Panel(centered_table_client,
                                style=CLIENT_COLOR,
                                title=view_setup['body']['title']
                                )
            disp_layout["clients"].update(client_disp)
        else:
            disp_layout['clients'].visible = False

        if view_setup['type'] == MC_CONTRACT_CREATE:
            table_contract = Table(box=None,
                                   show_header=False,
                                   )

            table_contract.add_column("Item",
                                      justify="left",
                                      no_wrap=True,
                                      style=CONTRACT_COLOR)
            table_contract.add_column("Separator",
                                      justify="left",
                                      no_wrap=True,
                                      style=CONTRACT_COLOR)
            table_contract.add_column("Value",
                                      justify="left",
                                      no_wrap=True,
                                      style="white")

            if 'client_id' in body_data:
                client_id = body_data['client_id']
            else:
                client_id = ' '
            table_contract.add_row("Id Client",
                                   ":",
                                   client_id)

            if 'total_amount' in body_data:
                total_amount = body_data['total_amount']
            else:
                total_amount = ' '
            table_contract.add_row("Montant total",
                                   ":",
                                   total_amount)

            if 'amount_unpaid' in body_data:
                amount_unpaid = body_data['amount_unpaid']
            else:
                amount_unpaid = ' '
            table_contract.add_row("Reste à payer",
                                   ":",
                                   amount_unpaid)

            if 'status' in body_data:
                status = body_data['status']
            else:
                status = ' '
            table_contract.add_row("Status",
                                   ":",
                                   status)

            centered_table_contract = Align.center(table_contract)
            contract_disp = Panel(centered_table_contract,
                                  style=CONTRACT_COLOR,
                                  title=view_setup['body']['title']
                                  )
            disp_layout["contracts"].update(contract_disp)

        else:
            disp_layout["contracts"].visible = False

        if view_setup['type'] == MC_EVENT_CREATE:
            table_event = Table(box=None,
                                show_header=False,
                                )

            table_event.add_column("Item",
                                   justify="left",
                                   no_wrap=True,
                                   style=EVENT_COLOR)
            table_event.add_column("Separator",
                                   justify="left",
                                   no_wrap=True,
                                   style=EVENT_COLOR)
            table_event.add_column("Value",
                                   justify="left",
                                   no_wrap=True,
                                   style="white")

            if 'title' in body_data:
                title = body_data['title']
            else:
                title = ' '
            table_event.add_row("Titre",
                                ":",
                                title)

            if 'contract_id' in body_data:
                contract_id = body_data['contract_id']
            else:
                contract_id = ' '
            table_event.add_row("No de Contrat",
                                ":",
                                contract_id)

            if 'start_date' in body_data:
                start_date = body_data['start_date']
            else:
                start_date = ' '
            table_event.add_row("date de début",
                                ":",
                                start_date)

            if 'end_date' in body_data:
                end_date = body_data['end_date']
            else:
                end_date = ' '
            table_event.add_row("Date de fin",
                                ":",
                                end_date)

            if 'location' in body_data:
                location = body_data['location']
            else:
                location = ' '
            table_event.add_row("Lieu",
                                ":",
                                location)

            if 'attendees' in body_data:
                attendees = body_data['attendees']
            else:
                attendees = ' '
            table_event.add_row("Nombre de personnes",
                                ":",
                                attendees)

            if 'notes' in body_data:
                notes = body_data['notes']
            else:
                notes = ' '
            table_event.add_row("Notes",
                                ":",
                                notes)

            centered_table_event = Align.center(table_event)
            event_disp = Panel(centered_table_event,
                               style=EVENT_COLOR,
                               title=view_setup['body']['title']
                               )
            disp_layout["events"].update(event_disp)

        else:
            disp_layout["events"].visible = False

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        input_data = display_prompt(view_setup['prompt'])

        console.height = None
        return input_data

    @token_process
    def user_administration(self, view_setup):
        """display the user administration home page """

        clear_screen()

        layout = administration_screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        # users list
        users_data = view_setup["body"]["data"]['users']

        table = Table(box=None)

        table.add_column("No",
                         justify="center",
                         no_wrap=True,
                         style="white")
        table.add_column("Matricule",
                         justify="center",
                         no_wrap=True,
                         style="white")
        table.add_column("Prénom",
                         justify="left",
                         no_wrap=True,
                         style="white")
        table.add_column("Nom",
                         justify="left",
                         no_wrap=True,
                         style="white")
        table.add_column("Email",
                         justify="left",
                         no_wrap=True,
                         style="white")
        table.add_column("Equipe",
                         justify="left",
                         no_wrap=True,
                         style="white")

        for user_data in users_data:
            user = user_data[0]
            team_name = user_data[1]
            table.add_row(
                str(user.id),
                str(user.employee_number),
                user.first_name,
                user.last_name,
                user.email,
                team_name
            )
        centered_table = Align.center(table)
        list_disp = Panel(
            centered_table,
            style=USER_COLOR,
            title=view_setup['body']['title'],
        )
        disp_layout['body'].update(list_disp)

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        choice = display_prompt(view_setup['prompt'])

        return prompt_choice_decode(choice)

    @token_process
    def user_details(self, view_setup):
        """display the user details page """

        clear_screen()

        layout = administration_screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        user = view_setup["body"]["data"]['user']
        user_team = view_setup["body"]["data"]['user_team']

        table = Table(box=None, show_header=False)

        table.add_column(
            "Item", justify="left", no_wrap=True, style=USER_COLOR)
        table.add_column(
            "Separator", justify="left", no_wrap=True, style=USER_COLOR)
        table.add_column(
            "Value", justify="left", no_wrap=True, style="white")

        table.add_row(
            "   Id", ":", str(user.id))
        table.add_row(
            "(1) Matricule", ":", str(user.employee_number))
        table.add_row(
            "(2) Prénom", ":", user.first_name)
        table.add_row(
            "(3) Nom", ":", user.last_name)
        table.add_row(
            "(4) Email", ":", user.email)
        table.add_row(
            "(5) Id Equipe", ":", str(user.team_id))
        table.add_row(
            "    Equipe", ":", user_team)

        centered_table = Align.center(table)
        list_disp = Panel(
            centered_table,
            style=USER_COLOR,
            title=view_setup['body']['title'],
        )
        disp_layout['body'].update(list_disp)

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        if view_setup['type'] == MC_USER_DETAILS:
            choice = display_prompt(view_setup['prompt'])
            return prompt_choice_decode(choice)
        elif view_setup['type'] == MC_USER_UPDATE:
            input_data = display_prompt(view_setup['prompt'])
            return input_data

    @token_process
    def user_creation(self, view_setup):
        """display the creation screen"""

        clear_screen()

        console.height = 15
        layout = administration_screen_layout()

        # header
        user_first_name = view_setup['header']['user_first_name']
        user_last_name = view_setup['header']['user_last_name']
        user_role = view_setup['header']['user_role']

        disp_layout = header_display_create(layout,
                                            user_first_name,
                                            user_last_name,
                                            user_role)

        # body
        body_data = view_setup['body']['data']

        table_user = Table(box=None,
                           show_header=False,
                           )

        table_user.add_column("Item",
                              justify="left",
                              no_wrap=True,
                              style=USER_COLOR)
        table_user.add_column("Separator",
                              justify="left",
                              no_wrap=True,
                              style=USER_COLOR)
        table_user.add_column("Value",
                              justify="left",
                              no_wrap=True,
                              style="white")

        if 'employee_number' in body_data:
            employee_number = body_data['employee_number']
        else:
            employee_number = ' '
        table_user.add_row("Matricule",
                           ":",
                           employee_number)

        if 'first_name' in body_data:
            first_name = body_data['first_name']
        else:
            first_name = ' '
        table_user.add_row("Prénom",
                           ":",
                           first_name)

        if 'last_name' in body_data:
            last_name = body_data['last_name']
        else:
            last_name = ' '
        table_user.add_row("Nom",
                           ":",
                           last_name)

        if 'email' in body_data:
            email = body_data['email']
        else:
            email = ' '
        table_user.add_row("Email",
                           ":",
                           email)

        if 'team_id' in body_data:
            team_id = body_data['team_id']
        else:
            team_id = ' '
        table_user.add_row("No d'équipe",
                           ":",
                           team_id)

        centered_table_user = Align.center(table_user)
        user_disp = Panel(centered_table_user,
                          style=USER_COLOR,
                          title=view_setup['body']['title']
                          )
        disp_layout['body'].update(user_disp)

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        input_data = display_prompt(view_setup['prompt'])

        console.height = None
        return input_data

    def login(self, view_setup):

        clear_screen()

        console.height = 6
        layout = administration_screen_layout()

        # header
        disp_layout = login_header_display_create(layout)

        # body
        disp_layout["body"].visible = False

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        login_dict = {}
        email = Prompt.ask("Entrer votre email")
        login_dict['email'] = email

        password = Prompt.ask("Entrer votre mot de passe", password=True)
        login_dict['password'] = password

        console.height = None
        return login_dict

    def exit(self):
        console.print("Au revoir")
