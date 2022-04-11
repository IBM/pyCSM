import requests


def get_scheduled_tasks(url, tk, verify=False, cert=None):
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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(getst_url, headers=headers, verify=verify, cert=cert)


def enable_scheduled_task(url, tk, taskid, verify=False, cert=None):
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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(enable_url, headers=headers, verify=verify, cert=cert)


def disable_scheduled_task(url, tk, taskid, verify=False, cert=None):
    """
    Disable a scheduled task.

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
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(disable_url, headers=headers,
                         verify=verify, cert=cert)


def run_scheduled_task(url, tk, taskid, verify=False, cert=None):
    """
    Run a scheduled task immediately.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        taskid (str): ID of the schedule task to enable.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    run_url = f"{url}/sessions/scheduledtasks/{taskid}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(run_url, headers=headers, verify=verify, cert=cert)
