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


def create_log_pkg(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(make_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_log_pkgs(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def backup_server(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(backup_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_server_backups(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(backup_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def backup_server_and_download(url, tk, file_name):
    """
    Create and downloads a server backup.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        file_name:  The file to write the server backup to

    Returns:
        A file downloaded into the client with the specified filename
    """
    backup_url = f"{url}/system/backupserver/download"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resp = requests.get(backup_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    return resp


def set_server_as_standby(url, tk, active_server):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(set_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_dual_control_state(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def change_dual_control_state(url, tk, enable):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(post_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_dual_control_requests(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def approve_dual_control_request(url, tk, id):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(post_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def reject_dual_control_request(url, tk, id, comment):
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
    post_url = f"{url}/system/dualcontrol/reject/{id}/{comment}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.post(post_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_active_standby_status(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def reconnect_active_standby_server(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(put_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def remove_active_or_standby_server(url, tk, haServer):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(put_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def set_standby_server(url, tk, standby_server, standby_username, standby_password):
    """
    Sets the server passed in to be the standby server. All data on the passed
    in server will be replaced with the data from the called server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        standby_server (str): IP or hostname of the standby server
        standby_username (str): Username to create a connection to the standby server
        standby_password (str): Password for the user to create a connection to the standby server

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/ha/setStandbyServer/{standby_server}/{standby_username}/{standby_password}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(put_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def takeover_standby_server(url, tk):
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
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.put(put_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_log_events(url, tk, count, session=None):
    """
    get a list of the most recent log events

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        count (int): The number of messages to return
        session (string): (optional) filter messages on session

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/logevents"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "count": count,
        "session": session
    }
    return requests.get(get_url, headers=headers, data=params,
                        verify=properties["verify"], cert=properties["cert"])


def create_and_download_log_pkg(url, tk, file_name):
    """
    This method will package all log files on the server into a .jar file
    that can be used for support - this call is a synchronous call and
    will not return to caller until package is complete. Call make take a while

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        file_name: Name of the file to write the log package to

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/system/logpackages/synchronous/download"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    resp = requests.get(put_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
    with open(file_name, 'wb') as f:
        f.write(resp.content)
    return resp


def get_session_types(url, tk):
    """
    Get supported session types

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/sessiontypes"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_server_version(url, tk):
    """
    Get the version of the server being called

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/version"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_volume_counts(url, tk):
    """
    Get a summary of the volume usage on the server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/system/volcounts"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
