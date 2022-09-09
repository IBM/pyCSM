import json
import warnings
import requests

properties = {
    "language": "en-US",
    "verify": False,
    "cert": None
}


def get_properties():
    """
    Returns a dictionary of the current properties and
    their values set for the file.
    """
    return properties


def change_properties(property_dictionary):
    """
    Takes a dictionary of properties and the values that
    user wants to change and changes them in the file.

    Args:
        property_dictionary (dict): Dictionary of the keys and values that need
        to be changed in the file.
        ex. {"language":"en-UK", "verify":True}

    Return:
        Returns the new properties dictionary.
    """
    for key in property_dictionary:
        properties[key] = property_dictionary[key]
    return properties


def get_token(url, username, password):
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
        "Accept-Language": properties["language"],
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "username": username,
        "password": password
    }
    warnings.filterwarnings("ignore")
    resp = requests.post(tk_url, headers=auth_headers,
                         data=params, verify=properties["verify"], cert=properties["cert"])
    tk = json.loads(resp.text)['token']
    return tk
