# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

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


def get_copysets(url, tk, name, mtls_header=None):
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
    if tk is not None:
        headers = {
            "Accept-Language": properties["language"],
            "X-Auth-Token": str(tk),
        }
    else:
        headers = {
            "Accept-Language": properties["language"],
            "X-Client-Certificate": open_cert_file(mtls_header),
        }
    return requests.get(getcs_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def add_copysets(url, tk, name, copysets, roleorder=None, mtls_header=None):
    """
    Add copy sets to a given session

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        copysets (list): List of copysets to add to a session
            ex. (Single Copy set with two volumes)
                [["DS8000:2107.GXZ91:VOL:D000","DS8000:2107.GXZ91:VOL:D001"]]
            ex. (Two Copy sets with two volumes each)
                "[[DS8000:1245.KTLM:VOL:0001","DS8000:1245.KTLM:VOL:0101"],
                  ["DS8000:2107.GXZ91:VOL:D004","DS8000:2107.GXZ91:VOL:D005"]]"
        roleorder (list): Optional list of the role names depicting the order of the volumes passed in on copysets
            ex. ["H1", "H2"]

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    add_url = f"{url}/sessions/{name}/copysets"
    if tk is not None:
        headers = {
            "Accept-Language": properties["language"],
            "X-Auth-Token": str(tk),
            "Content-Type": "application/x-www-form-urlencoded"

        }
    else:
        headers = {
            "Accept-Language": properties["language"],
            "X-Client-Certificate": open_cert_file(mtls_header),
            "Content-Type": "application/x-www-form-urlencoded"

        }
    params = {
        "copysets": str(copysets),
        "roleOrder": str(roleorder)
    }
    return requests.post(add_url, headers=headers, data=params,
                         verify=properties["verify"], cert=properties["cert"])


def remove_copysets(url, tk, name, copysets, force=False, soft=False, mtls_header=None):
    """
    Removes Copy Sets from the given session.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        copyset (str): list of copyset hosts to remove from a session
            ex. ["DS8000:2107.GXZ91:VOL:D000"]
            ex. ["DS8000:1245.KTLM:VOL:0001", "DS8000:2107.GXZ91:VOL:D004"]
        force (boolean): Force Set to true if you wish to remove the pair from CSM ignoring hardware errors.
        soft (boolean): Keep base relationships on the hardware but remove the copy set from the session.


    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    remove_url = f"{url}/sessions/{name}/{force}/{soft}/copysets"
    if tk is not None:
        headers = {
            "Accept-Language": properties["language"],
            "X-Auth-Token": str(tk),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    else:
        headers = {
            "Accept-Language": properties["language"],
            "X-Client-Certificate": open_cert_file(mtls_header),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    params = {
        "copysets": str(copysets)
    }
    return requests.delete(remove_url, headers=headers,
                           data=params, verify=properties["verify"], cert=properties["cert"])


def export_copysets(url, tk, name, file_name, mtls_header=None):
    """
    Exports copysets as a csv file and downloads it to the calling system.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name:  Name of the session to export copysets for
        file_name: Name for the csv file location  (ex.  ""/Users/myuser/CSM/Export/myexport.csv")

    Returns:
        JSON String representing the result of the command.
    """
    export_url = f"{url}/sessions/{name}/copysets/download"
    if tk is not None:
        headers = {
            "Accept-Language": properties["language"],
            "X-Auth-Token": str(tk),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    else:
        headers = {
            "Accept-Language": properties["language"],
            "X-Client-Certificate": open_cert_file(mtls_header),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    resp = requests.get(export_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    return resp


def get_pair_info(url, tk, name, rolepair, mtls_header=None):
    """
    Get all the pairs for the session in a given role pair.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        rolepair (str): The name of the role pair to query in the session

    Returns:
        JSON String representing the result of the command.
        'I' = successful,'W' = warning, 'E' = error.
    """
    get_url = f"{url}/sessions/{name}/pairs/{rolepair}"
    if tk is not None:
        headers = {
            "Accept-Language": properties["language"],
            "X-Auth-Token": str(tk),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    else:
        headers = {
            "Accept-Language": properties["language"],
            "X-Client-Certificate": open_cert_file(mtls_header),
            "Content-Type": "application/x-www-form-urlencoded"
        }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])

def open_cert_file(file_location):
    """
    Opens the certificate file and returns the contents
    Args:
        file_location (str): The location of the certificate file
    Returns:
        str: The contents of the certificate file
        """
    with open(file_location, 'rb') as f:
        return f.read().decode('utf-8').replace('\r', '').replace('\n', '')