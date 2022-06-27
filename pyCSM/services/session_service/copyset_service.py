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


def get_copysets(url, tk, name):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
    }
    return requests.get(getcs_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def add_copysets(url, tk, name, copysets, roleorder=None):
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
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"

    }
    params = {
        "copysets": str(copysets),
        "roleOrder": str(roleorder)
    }
    return requests.post(add_url, headers=headers, data=params,
                         verify=properties["verify"], cert=properties["cert"])


def remove_copysets(url, tk, name, copysets, force=False, soft=False):
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
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "copysets": str(copysets)
    }
    return requests.delete(remove_url, headers=headers,
                           data=params, verify=properties["verify"], cert=properties["cert"])


def export_copysets(url, tk, name, file_name):
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
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    resp = requests.get(export_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    return resp


def get_pair_info(url, tk, name, rolepair):
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
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def enable_scheduled_task_at_time(url, tk, task_id, start_time):
    """
    Enable the task at the given time

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        task_id (int): ID of the schedule task to enable
        start_time (str): Time to enable the task.
        Format of yyyy-MM-dd'T'HH-mm.

    Returns:
        JSON String representing the result of the command.
        'I' = successful,'W' = warning, 'E' = error.
    """
    post_url = f"{url}/sessions/scheduledtasks/enable/{task_id}/{start_time}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(post_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def run_scheduled_task_at_time(url, tk, task_id, start_time):
    """
    Run a scheduled task immediately.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        task_id (int): ID of the schedule task to enable
        start_time (str): Time to enable the task.
        Format of yyyy-MM-dd'T'HH-mm.

    Returns:
        JSON String representing the result of the command.
        'I' = successful,'W' = warning, 'E' = error.
    """
    post_url = f"{url}/sessions/scheduledtasks/{task_id}/runat/{start_time}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(post_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
