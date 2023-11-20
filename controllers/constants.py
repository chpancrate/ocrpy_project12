# constant used in controller and view for diplay purpose

from models.client_models import CONTRACT_STATUS

DATE_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT_DISP = 'JJ/MM/AAAA HH:MM'

# messages
MSG_ERROR = ("une erreur s'est produite veuillez réessayer,\n"
             "si l'erreur persiste contactez votre administrateur")
MSG_CLIENT_NOT_FOUND = 'Le client est inexistant'
MSG_CONTRACT_NOT_FOUND = ('Le contrat est inexistant, '
                          'est déjà lié à un évènement '
                          'ou non lié à un de vos client')
MSG_EVENT_NOT_FOUND = "L'évènement est inexistant"

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
MSG_EXPIRED_SESSION = "Votre session a expiré merci de vous reconnecter"

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
MENU_CONTRACT_FILTER_UNPAID_KEYS = 'fop'
MENU_CONTRACT_FILTER_UNPAID_LABEL = 'Contrats non payés'
MENU_CONTRACT_FILTER_UNSIGNED_KEYS = 'fos'
MENU_CONTRACT_FILTER_UNSIGNED_LABEL = 'Contrats non signés'

MENU_EVENTS_LIST_KEYS = 'e'
MENU_EVENTS_LIST_LABEL = 'Liste Evènement'
MENU_EVENTS_DETAILS_KEYS = 'de'
MENU_EVENTS_DETAILS_LABEL = 'Détails Evènement'
MENU_EVENT_UPDATE_KEYS = 'me'
MENU_EVENT_UPDATE_LABEL = 'Modifier Evènement'
MENU_EVENT_CREATE_KEYS = 'ce'
MENU_EVENT_CREATE_LABEL = 'Créer Evènement'
MENU_EVENT_FILTER_OWNED_KEYS = 'fev'
MENU_EVENT_FILTER_OWNED_LABEL = 'Vos évènements'
MENU_EVENT_FILTER_UNASSIGNED_KEYS = 'fes'
MENU_EVENT_FILTER_UNASSIGNED_LABEL = 'Evènements sans support'

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

# prompts
PRPT_CLIENT_LASTNAME = "Entrer le nom du client"
PRPT_CLIENT_FIRSTNAME = "Entrer le prénom du client"
PRPT_CLIENT_EMAIL = "Entrer l'email"
PRPT_CLIENT_TELEPHONE = "Entrer le numéro de téléphone"
PRPT_CLIENT_ENTERPRISE = "Entrer le nom de l'entreprise"
PRPT_CLIENT_COMMERCIAL_ID = "Entrer le numero du contact commercial"
PRPT_CLIENT_CREATION = "Voulez-vous créer le client ?"

PRPT_CLIENT_ID = "Entrer le No du client"
PRPT_CONTRACT_TOTAL_AMOUNT = "Entrer le montant total du contrat"
PRPT_CONTRACT_UNPAID_AMOUNT = "Entrer le montant non payé du contrat"
PRPT_CONTRACT_STATUS = "Entrer le status du contrat"
PRPT_CONTRACT_CREATION = "Voulez-vous créer le contrat ?"

PRPT_EVENT_TITLE = "Entrer le titre de l'évènement"
PRPT_CONTRACT_ID = "Entrer le No de contrat"
PRPT_EVENT_START_DATE = "Entrer la date et l'heure de début"
PRPT_EVENT_END_DATE = "Entrer la date et l'heure de fin"
PRPT_EVENT_LOCATION = "Entrer le lieu de l'évènement"
PRPT_EVENT_ATTENDEES = "Entrer le nombre de personnes"
PRPT_EVENT_NOTES = "Entrer les notes concernant l'évènement"
PRPT_EVENT_SUPPORT_ID = "Entrer le numero du contact support"
PRPT_EVENT_CREATION = "Voulez-vous créer l'évènement ?"

PRPT_USER_EMPLOYEE_ID = "Entrer le Matricule"
PRPT_USER_FIRST_NAME = "Entrer le prénom"
PRPT_USER_LAST_NAME = "Entrer le nom"
PRPT_USER_EMAIL = "Entrer l'email"
PRPT_USER_TEAM_ID = "Entrer le numéro d'équipe"
PRPT_USER_PASSWORD = "Entrer le mot de passe"
PRPT_USER_CREATION = "Voulez-vous créer l'utilisateur ?"

PRPT_ACTIONS = "Quel est votre choix ?"
PRPT_NEW_DATA = "Quelle est la nouvelle valeur?"

YES_NO_CHOICE = ['o', 'n']

# titles
TITLE_CLIENT_DETAILS = "Détais du client"
TITLE_CLIENTS_LISTS = "Liste des clients"
TITLE_CLIENTS_HOME = "Vos clients"

TITLE_CONTRACT_DETAILS = "Détais du contrat"
TITLE_CONTRACTS_LISTS = "Liste des contrats"
TITLE_CONTRACTS_HOME = "Vos contrats"

TITLE_EVENT_DETAILS = "Détais de l'évènement"
TITLE_EVENTS_LISTS = "Liste des évènements"
TITLE_EVENTS_HOME = "Vos évènements"

TITLE_USER_DETAILS = "Utilisateur"
TITLE_USER_LISTS = "Liste des utilisateurs"
