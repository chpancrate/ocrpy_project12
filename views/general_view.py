import os

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from .view_functions import (
    main_menu_display_create,
    sub_menu_display_create,
    prompt_display_create,
    prompt_choice_decode,
    console,
    screen_layout,
    administration_screen_layout,
    client_creation_prompt_display,
    contract_creation_prompt_display,
    event_creation_prompt_display,
    user_creation_prompt_display,
    clear_screen,
    display_date
)

# reduce console size to allow prompt
OFFSET_HEIGHT = 2
CONSOLE_SIZE = console.height - OFFSET_HEIGHT
console.height = CONSOLE_SIZE


class Screen:
    def general(self, view_setup):
        """display the start screen"""

        clear_screen()

        layout = screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

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
                style="blue",
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
                style="blue",
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
                style="blue",
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
        choice = prompt_display_create(view_setup)

        return prompt_choice_decode(choice)

    def details(self, view_setup):
        """display the details screen"""

        clear_screen()

        layout = screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

        # body
        # client display
        if "client" in view_setup["body"]["data"]:
            client = view_setup["body"]["data"]["client"]

            # client details
            table_client = Table(box=None, show_header=False, title="Client")

            table_client.add_column(
                "Item", justify="left", no_wrap=True, style="bright_blue")
            table_client.add_column(
                "Separator", justify="left", no_wrap=True, style="bright_blue")
            table_client.add_column(
                "Value", justify="left", no_wrap=True, style="white")

            table_client.add_row("    No", ":", str(client.id))
            table_client.add_row("(1) Prénom", ":", client.first_name)
            table_client.add_row("(2) Nom", ":", client.last_name)
            table_client.add_row("(3) Email", ":", client.email)
            table_client.add_row("(4) Telephone", ":", client.telephone)
            table_client.add_row("(5) Entreprise", ":", client.enterprise)
            table_client.add_row("(6) Contact", ":",
                                 str(client.commercial_contact_id))
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
                                style="blue",
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

            table_contract.add_column(
                "Item", justify="left", no_wrap=True, style="bright_blue")
            table_contract.add_column(
                "Separator", justify="left", no_wrap=True, style="bright_blue")
            table_contract.add_column(
                "Value", justify="left", no_wrap=True, style="white")

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

            # event details
            table_event = Table(box=None, show_header=False, title="Evènement")

            table_event.add_column(
                "Item", justify="left", no_wrap=True, style="bright_blue")
            table_event.add_column(
                "Separator", justify="left", no_wrap=True, style="bright_blue")
            table_event.add_column(
                "Value", justify="left", no_wrap=True, style="white")
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
                if event_support:
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
                                  style="blue",
                                  title=(view_setup['body']
                                         ['data']['contract_title'])
                                  )
            disp_layout["contracts"].update(contract_disp)
        else:
            disp_layout["contracts"].visible = False

        # event display
        if "event" in view_setup["body"]["data"]:
            event = view_setup["body"]["data"]['event']

            table_event = Table(box=None, show_header=False, title="Evènement")

            table_event.add_column(
                "Item", justify="left", no_wrap=True, style="bright_blue")
            table_event.add_column(
                "Separator", justify="left", no_wrap=True, style="bright_blue")
            table_event.add_column(
                "Value", justify="left", no_wrap=True, style="white")

            table_event.add_row(
                "(1) Titre", ":", event.title)
            table_event.add_row(
                "(2) No Contrat", ":", str(event.contract_id))
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
            centered_table_event = Align.center(table_event)

            # screen display
            event_disp = Panel(centered_table_event,
                               style="blue",
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
        choice = prompt_display_create(view_setup)

        return prompt_choice_decode(choice)

    def creation(self, view_setup):
        """display the creation screen"""

        clear_screen()

        console.height = 6
        layout = screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

        # body
        disp_layout["body"].visible = False

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        if view_setup['type'] == 'client_creation':
            client_dict = client_creation_prompt_display()
        elif view_setup['type'] == 'contract_creation':
            client_dict = contract_creation_prompt_display()
        elif view_setup['type'] == 'event_creation':
            client_dict = event_creation_prompt_display()

        console.height = None
        return client_dict

    def user_administration(self, view_setup):
        """display the user administration home page """

        clear_screen()

        layout = administration_screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

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
            style="blue",
            title=view_setup["body"]["data"]["users_title"],
        )
        disp_layout['body'].update(list_disp)

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        choice = prompt_display_create(view_setup)

        return prompt_choice_decode(choice)

    def user_details(self, view_setup):
        """display the user details page """

        clear_screen()

        layout = administration_screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

        # body
        user = view_setup["body"]["data"]['user']
        user_team = view_setup["body"]["data"]['user_team']

        table = Table(box=None, show_header=False, title="Evènement")

        table.add_column(
            "Item", justify="left", no_wrap=True, style="bright_blue")
        table.add_column(
            "Separator", justify="left", no_wrap=True, style="bright_blue")
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
            style="blue",
            title=view_setup["body"]["data"]["user_title"],
        )
        disp_layout['body'].update(list_disp)

        # footer
        sub_menu_disp = sub_menu_display_create(
            view_setup["footer"]["actions"], view_setup["footer"]["title"]
        )

        disp_layout["footer"].update(sub_menu_disp)
        console.print(disp_layout)

        # prompt
        choice = prompt_display_create(view_setup)

        return prompt_choice_decode(choice)

    def user_creation(self, view_setup):
        """display the creation screen"""

        clear_screen()

        console.height = 6
        layout = administration_screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

        # body
        disp_layout["body"].visible = False

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        user_dict = user_creation_prompt_display()

        console.height = None
        return user_dict

    def login(self, view_setup):

        clear_screen()

        console.height = 6
        layout = administration_screen_layout()

        # header
        disp_layout = main_menu_display_create(layout)

        # body
        disp_layout["body"].visible = False

        # footer
        disp_layout["footer"].visible = False

        console.print(disp_layout)

        # prompt
        login_dict = {}
        email = Prompt.ask("Entrer votre email")
        login_dict['email'] = email

        password = Prompt.ask("Entrer votre mot de passe")
        login_dict['password'] = password

        console.height = None
        return login_dict
