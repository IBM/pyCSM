import requests

"""

    Description: Methods that make REST calls for copyset type services

"""


def get_copysets(url, tk, name, verify=False, cert=None):
    """
    Gets all copy sets and their info for a given session.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful,'W' = warning, 'E' = error.
    """
    getcs_url = f"{url}/sessions/{name}/copysets"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(getcs_url, headers=headers, verify=verify, cert=cert)


def add_copysets(url, tk, name, copysets, verify=False, cert=None):
    """
    Add copy sets to a given session

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        copysets (str): List of copy sets to add to the session.
            ex. "DS8000:1245.KTLM:VOL:0001", "DS8000:1245.KTLM:VOL:0101"

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    add_url = f"{url}/sessions/{name}/copysets"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        'copysets': "[[" + copysets + "]]"
    }
    return requests.post(add_url, headers=headers, data=params,
                         verify=verify, cert=cert)


def remove_copysets(url, tk, name, force, soft, verify=False, cert=None):
    """
    Removes Copy Sets from the given session.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        force (boolean): Force Set to true if you wish to remove the pair from CSM ignoring hardware errors.
        soft (boolean): Keep base relationships on the hardware but remove the copy set from the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    remove_url = f"{url}/sessions/{name}/{force}/{soft}/copysets"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.delete(remove_url, headers=headers,
                           verify=verify, cert=cert)


def export_copysets(url, tk, file_name, verify=False, cert=None):
    """
    Exports copysets as a csv file and downloads it to the calling system.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        file_name: Name for the csv file location

    Returns:
        JSON String representing the result of the command.
    """
    export_url = f"{url}/sessions/dog/copysets/download"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk)
    }
    resp = requests.get(export_url, headers=headers, verify=verify, cert=cert)
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    return resp
