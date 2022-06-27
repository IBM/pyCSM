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


def get_scheduled_tasks(url, tk):
    """
    Returns a list of scheduled tasks defined on the server

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    getst_url = f"{url}/sessions/scheduledtasks"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(getst_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def enable_scheduled_task(url, tk, taskid):
    """
    Enable a scheduled task to run based off the schedule defined on the task.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        taskid (str): ID of the schedule task to enable.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    enable_url = f"{url}/sessions/scheduledtasks/enable/{taskid}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(enable_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def disable_scheduled_task(url, tk, taskid):
    """
    Disable a scheduled task from running automatically.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        taskid (str): ID of the schedule task to enable.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    disable_url = f"{url}/sessions/scheduledtasks/disable/{taskid}"

    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(disable_url, headers=headers,
                         verify=properties["verify"], cert=properties["cert"])


def run_scheduled_task(url, tk, taskid, synchronous=False):
    """
    Run a scheduled task immediately.  Synchronous value set to true if call should not return until task
    is complete.  False if you want it to run in the asynchronous after the call completes.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        taskid (str): ID of the schedule task to enable.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    run_url = f"{url}/sessions/scheduledtasks/{taskid}/{synchronous}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(run_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
