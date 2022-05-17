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


def remove_copysets(url, tk, name, force, soft, copyset, verify=False, cert=None):
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
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "copysets": copyset
    }
    return requests.delete(remove_url, headers=headers,
                           data=params, varify=verify, cert=cert)


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


def get_pair_info(url, tk, name, rolepair, verify=False, cert=None):
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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def enable_scheduled_task_at_time(url, tk, task_id, start_time, verify=False, cert=None):
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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(post_url, headers=headers, verify=verify, cert=cert)


def run_scheduled_task_at_time(url, tk, task_id, start_time, verify=False, cert=None):
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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(post_url, headers=headers, verify=verify, cert=cert)
