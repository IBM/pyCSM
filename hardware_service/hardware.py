import requests

'''

    Description: Methods that make REST calls for hardware type services.

'''


def get_devices(url, tk, device_type, verify=False, cert=None):
    """
    Uses a get request to get info of all the storagedevices of a given type.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_type (str): Type of storage device  ex. ds8000 or svc.

    Returns:
        Returns JSON String representing the result of the command.
    """
    getd_url = f"{url}/storagedevices/connectioninfo"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "type": {device_type}
    }
    return requests.get(getd_url, headers=headers, data=params,
                        verify=verify, cert=cert)


def add_device(url, tk, device_type, device_ip, device_port, device_username,
               device_password, second_ip=None, second_port=None,
               second_username=None, second_password=None,
               verify=False, cert=None):
    """
    This method will create a connection from the
    server to a specified storage system.

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_type (str): Type of storage device  ex. ds8000 or svc.
        device_ip (str): IP address or hostname for the storage system.
        device_port (str): Port for the connection to the storage system.
        device_username (str): Username for the storage system connection.
        device_password (str): Password for the storage system connection.
        second_ip (str) (OPTIONAL): For DS8000 storage systems,
        the IP address or hostname of a secondary HMC system.
        second_port (str) (OPTIONAL): Port to use for the connection
        to the secondary HMC system for DS8000 connections
        second_username (str) (OPTIONAL): Username for the connection
        to the secondary HMC system for DS8000 connections.
        second_password (str) (OPTIONAL): Password for the connection
        to the secondary HMC system for DS8000 connections.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.

    """

    addd_url = f"{url}/storagedevices"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "type": device_type,
        "deviceip": device_ip,
        "deviceport": device_port,
        "deviceusername": device_username,
        "devicepassword": device_password,
        "seconddeviceip": second_ip,
        "seconddeviceport": second_port,
        "seconddeviceusername": second_username,
        "seconddevicepassword": second_password
    }
    return requests.put(addd_url, headers=headers, data=params,
                        verify=verify, cert=cert)


def remove_device(url, tk, system_id, verify=False, cert=None):
    """
    This method will remove a specified storage system connection

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_id (str): The id of the storage system to be removed.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    remove_url = f"{url}/storagedevices/{system_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.delete(remove_url, headers=headers,
                           verify=verify, cert=cert)


def update_device_site_location(url, tk, system_id, location, verify=False, cert=None):
    """
    Set a user defined site location for a given storage system

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_id (str): The id of the storage system to be updated.
        location (str): The name of the location to set on the storage system.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    update_url = f"{url}/storagedevices/{system_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "location": location
    }
    return requests.post(update_url, headers=headers, data=params,
                         verify=verify, cert=cert)


def get_volumes(url, tk, system_name, verify=False, cert=None):
    """
    This method will return all volumes for a given
    storage system based off the input system name.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_name (str): The name of the storage system.

    Returns:
        JSON String representing all the volumes for that storage system.
    """
    get_url = f"{url}/storagedevices/volumes/{system_name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def export_vol_writeio_history(url, tk, session_name, start_time, end_time,
                       verify=False, cert=None):
    """
    Exports ESE Box History for a session in csv format to a file.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        session_name (str): The name of the session.
        start_time (str): Start time YYYY-MM-DD. Type:str
        end_time (str): End time YYYY-MM-DD.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    export_url = f"{url}/sessions/{session_name}/exportesevolumehistory"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "starttime": start_time,
        "endtime": end_time
    }
    return requests.put(export_url, headers=headers, data=params,
                        verify=verify, cert=cert)


def get_paths(url, tk, verify=False, cert=None):
    """
    Queries all the logical paths on the storage system.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/storagedevices/paths"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def get_path_on_storage_system(url, tk, system_id, verify=False, cert=None):
    """
    Query for all paths on the given storage system.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_id (str): The id of the storage system to be updated.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/storagedevices/paths/{system_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def refresh_config(url, tk, system_id, verify=False, cert=None):
    """
    Refreshes the configuration for the given storage system.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_id (str): The id of the storage system to be updated.

    Returns:
        JSON String representing the result of the command.
    """
    refresh_url = f"{url}/storagedevices/{system_id}/refreshconfig"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(refresh_url, headers=headers, verify=verify, cert=cert)
