import json
import warnings
import requests


def get_token(url, username, password, verify=False, cert=None):
    """

    Retrieves a REST token from the server to be used for future REST commands.

    Args:
        url (str): Base url of csm server ex. https://servername:port/CSM/web.
        username (str): username for server login.
        password (str): password for server login.

    Returns:
        Returns a token string to be used to make future rest calls to the
        given CSM server.

    """
    tk_url = f"{url}/system/v1/tokens"
    auth_headers = {
        "Accept-Language": "en-US",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "username": username,
        "password": password
    }
    warnings.filterwarnings("ignore")
    resp = requests.post(tk_url, headers=auth_headers,
                         data=params, verify=verify, cert=cert)
    tk = json.loads(resp.text)['token']
    return tk
