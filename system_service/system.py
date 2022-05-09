import requests


def create_log_pkg(url, tk, verify=False, cert=None):
    """
    This method will package all log files on the server into a .jar file

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    make_url = f"{url}/system/logpackages"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(make_url, headers=headers, verify=verify, cert=cert)


def get_log_pkgs(url, tk, verify=False, cert=None):
    """
    Gets a list of log packages and their location on the server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
        """
    get_url = f"{url}/system/logpackages"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def backup_server(url, tk, verify=False, cert=None):
    """
    Creates a zip backup of the CSM server data
    that can be used for restoring the server at a later date

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    backup_url = f"{url}/system/backupserver"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(backup_url, headers=headers, verify=verify, cert=cert)


def get_server_backups(url, tk, verify=False, cert=None):
    """
    Retrieves a list of all server backups.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    backup_url = f"{url}/system/backupserver"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(backup_url, headers=headers, verify=verify, cert=cert)


def backup_download_server(url, tk, verify=False, cert=None):
    """
    Create and downloads a server backup.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        A file downloaded into the client.
    """
    backup_url = f"{url}/system/backupserver/download"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(backup_url, headers=headers, verify=verify, cert=cert)


def set_server_as_standby(url, tk, active_server, verify=False, cert=None):
    """
    Issue this command to the server that you want to be the standby server.
    Sets the server passed in to be the active server. All data on
    the called server will be replaced with the data from the active server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        active_server (str): IP or hostname of the active server.
        This method will use the default port.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    set_url = f"{url}/system/ha/setServerAsStandby/{active_server}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(set_url, headers=headers, verify=verify, cert=cert)


def get_dual_control_state(url, tk, verify=False, cert=None):
    """
    Use this method to determine if dual control is currently enabled of disabled on the server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/dualcontrol"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def change_dual_control_state(url, tk, enable, verify=False, cert=None):
    """
    Use this method to enable or disable dual control on the CSM server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        enable (bool): Set to 'true' if you want to enable dual control or
        'false' if you want to disable.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    post_url = f"{url}/system/dualcontrol/{enable}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(post_url, headers=headers, verify=verify, cert=cert)


def get_dual_control_requests(url, tk, verify=False, cert=None):
    """
    Returns a list of dual control events waiting for approval or rejection

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/dualcontrol/requests"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def approve_dual_control_request(url, tk, id, verify=False, cert=None):
    """
    Approve a dual control request

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        id (int): ID of the request caller wants to approve.
        ID from the 'requestid' field return from getDualControlEvents.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    post_url = f"{url}/system/dualcontrol/approve/{id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(post_url, headers=headers, verify=verify, cert=cert)


def reject_dual_control_request(url, tk, id, comment, verify=False, cert=None):
    """
    Reject a dual control request

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        id (int): ID of the request caller wants to approve.
        ID from the 'requestid' field return from getDualControlEvents.
        comment (str): Comment to the creator of the event on why the request was rejected.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    post_url = f"{url}/system/dualcontrol/reject/{id})/{comment}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.post(post_url, headers=headers, verify=verify, cert=cert)


def get_active_standby_status(url, tk, verify=False, cert=None):
    """
    Get the current state of the active standby server connection

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/ha"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def reconnect_active_standby_server(url, tk, verify=False, cert=None):
    """
    Reconnect the active standby connection

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/ha/reconnect"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(put_url, headers=headers, verify=verify, cert=cert)


def remove_active_or_standby_server(url, tk, haServer, verify=False, cert=None):
    """
    Remove the alternate server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        haServer (str): hostname of the server to remove

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/ha/removeHaServer/{haServer}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(put_url, headers=headers, verify=verify, cert=cert)


def set_standby_server(url, tk, standby_server, standby_username, standby_password, verify=False, cert=None):
    """
    Sets the server passed in to be the standby server. All data on the passed
    in server will be replaced with the data from the called server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        standby_server (str): IP or hostname of the standby server
        standby_username (str): Username to create a connection to the
        standby server
        standby_password (str): Password for the user to create a connection
        to the standby server

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/ha/setStandbyServer/{standby_server}/{standby_username}/{standby_password}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(put_url, headers=headers, verify=verify, cert=cert)


def takeover_standby_server(url, tk, verify=False, cert=None):
    """
    Issues a takeover on the standby server making the standby server an active server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/ha/takeover"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(put_url, headers=headers, verify=verify, cert=cert)
