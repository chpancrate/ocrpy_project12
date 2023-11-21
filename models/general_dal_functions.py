from .user_dal_functions import get_user_by_id
from .team_dal_functions import get_team_by_id
from .role_dal_functions import get_role_by_id


def get_user_role(user_id):
    """ get role for the user
    parameters :
    user_id
    returns :
    'status': ok or ko
    'role': role of the user
    'error': error details (if status == ko)
    """
    result = {}
    result_user = get_user_by_id(user_id)
    if result_user['status'] == 'ok':
        result_team = get_team_by_id(result_user['user'].team_id)
        if result_team['status'] == 'ok':
            result_role = get_role_by_id(result_team['team'].role_id)
            if result_role['status'] == 'ok':
                result['status'] = 'ok'
                result['user_role'] = result_role['role'].name
            else:
                result['status'] = 'ko'
                result['error'] = result_role['error']
        else:
            result['status'] = 'ko'
            result['error'] = result_team['error']
    else:
        result['status'] = 'ko'
        result['error'] = result_user['error']

    return result
