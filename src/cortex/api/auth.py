"""## Authentication_.

After your application is successfully connected_ to the Cortex service, you must go through the authentication
procedure.

First, you should call getUserLogin_ to check if the user has already logged in though `EMOTIV Launcher`_. Then, you
must call requestAccess_ to ask the user to approve your application.

Finally, call authorize_ to generate a Cortex token or you can reuse a token that you previously got from this method,
if it is not expired.

.. _Authentication: https://emotiv.gitbook.io/cortex-api/authentication
.. _connected: https://emotiv.gitbook.io/cortex-api/connecting-to-the-cortex-api
.. _getUserLogin: https://emotiv.gitbook.io/cortex-api/authentication/getuserlogin
.. _`EMOTIV Launcher`: https://emotiv.gitbook.io/emotiv-launcher/
.. _requestAccess: https://emotiv.gitbook.io/cortex-api/authentication/requestaccess
.. _authorize: https://emotiv.gitbook.io/cortex-api/authentication/authorize

"""

from typing import Literal

from cortex.api.id import AuthID
from cortex.api.types import AuthorizeRequest, BaseRequest


def get_info() -> BaseRequest:
    """Get the Cortex info.

    Read More:
        [getCortexInfo](https://emotiv.gitbook.io/cortex-api/authentication/getcortexinfo)

    Returns:
        BaseRequest: The Cortex info.

    """
    _info = {'id': AuthID.CORTEX_INFO, 'jsonrpc': '2.0', 'method': 'getCortexInfo'}

    return _info


def get_user_login() -> BaseRequest:
    """Get the current logged in user.

    Read More:
        [getUserLogin](https://emotiv.gitbook.io/cortex-api/authentication/getuserlogin)

    Returns:
        BaseRequest: The user login request.

    """
    _login = {'id': AuthID.USER_LOGIN, 'jsonrpc': '2.0', 'method': 'getUserLogin'}

    return _login


def access(client_id: str, client_secret: str, *, method: Literal['requestAccess', 'hasAccessRight']) -> BaseRequest:
    """Request access or verify access right.

    Keyword Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.
        method (Literal['requestAccess', 'hasAccessRight']): The method.

    Read More:
        [requestAccess](https://emotiv.gitbook.io/cortex-api/authentication/requestaccess)
        [hasAccessRight](https://emotiv.gitbook.io/cortex-api/authentication/hasaccessright)

    Returns:
        BaseRequest: The access status.

    """
    if method not in ('requestAccess', 'hasAccessRight'):
        raise ValueError('method must be either "requestAccess" or "hasAccessRight".')

    if method == 'requestAccess':
        _id = AuthID.REQUEST_ACCESS
    else:
        _id = AuthID.HAS_ACCESS_RIGHT

    _access = {
        'id': _id,
        'jsonrpc': '2.0',
        'method': method,
        'params': {'clientId': client_id, 'clientSecret': client_secret},
    }

    return _access


def authorize(
    client_id: str,
    client_secret: str,
    *,
    license: str | None = None,  # pylint: disable=redefined-builtin
    debit: int | None = None,
) -> AuthorizeRequest:
    """Authorize the client.

    Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.

    Keyword Args:
        license (str): The license.
        debit (int): Number of sessions to debit from the license,
            so it can be spent locally without having to authorize
            again. You need to debit the license only if you want to
            *activate a session*. The default is 0.

    Read More:
        [authorize](https://emotiv.gitbook.io/cortex-api/authentication/authorize)

    Returns:
        AuthorizeRequest: The authorization status.

    """
    _params = {'clientId': client_id, 'clientSecret': client_secret}

    if license is not None:
        _params['license'] = license

    if debit is not None:
        _params['debit'] = debit  # type: ignore[assignment]

    authorization = {'id': AuthID.AUTHORIZE, 'jsonrpc': '2.0', 'method': 'authorize', 'params': _params}

    return authorization


def generate_new_token(auth: str, client_id: str, client_secret: str) -> BaseRequest:
    """Generate a new token.

    Notes:
        This function is used to generate a new Cortex token. You can
        use this method to extend the expiration date of a token.

    Read More:
        [generateNewToken](https://emotiv.gitbook.io/cortex-api/authentication/generatenewtoken)

    Args:
        auth (str): The Cortex authentication token.
        client_id (str): The client ID.
        client_secret (str): The client secret.

    Returns:
        BaseRequest: The new token.

    """
    _token = {
        'id': AuthID.GEN_NEW_TOKEN,
        'jsonrpc': '2.0',
        'method': 'generateNewToken',
        'params': {'cortexToken': auth, 'clientId': client_id, 'clientSecret': client_secret},
    }

    return _token


def get_user_info(auth: str) -> BaseRequest:
    """Get the current user information.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [getUserInformation](https://emotiv.gitbook.io/cortex-api/authentication/getuserinfo)

    Returns:
       BaseRequest: The user information.

    """
    _info = {'id': AuthID.USER_INFO, 'jsonrpc': '2.0', 'method': 'getUserInformation', 'params': {'cortexToken': auth}}

    return _info


def get_license_info(auth: str) -> BaseRequest:
    """Get the current license information.

    Args:
        auth (str): The Cortex authentication token.

    Read More:
        [getLicenseInfo](https://emotiv.gitbook.io/cortex-api/authentication/getlicenseinfo)

    Returns:
        BaseRequest: The license information.

    """
    _info = {'id': AuthID.LICENSE_INFO, 'jsonrpc': '2.0', 'method': 'getLicenseInfo', 'params': {'cortexToken': auth}}

    return _info
