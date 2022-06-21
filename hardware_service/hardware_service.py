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


def add_device(url, tk, device_type, device_ip, device_username,
               device_password, device_port=None, second_ip=None, second_port=None,
               second_username=None, second_password=None,
               verify=False, cert=None):
    """
    Use this method to create a connection from the CSM server to a specified storage system

    Args:
        url (str): Base url of csm server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_type (str): Type of storage device  ex. ds8000 or svc.
        device_ip (str): IP address or hostname for the primary HMC for the storage system.
        device_username (str): Username for the storage system connection.
        device_password (str): Password for the storage system connection.
        device_port (str) (OPTIONAL): Port to use for the connection to the storage system.
        second_ip (str) (OPTIONAL): For DS8000 storage systems, the IP address or hostname of a secondary HMC.
        second_port (str) (OPTIONAL): Port to use for the connection to the secondary HMC.
        second_username (str) (OPTIONAL): Username for the connection to the secondary HMC.
        second_password (str) (OPTIONAL): Password for the connection to the secondary HMC.

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
    Use this method to remove the connection to the specified storage system

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
    Use this method to retrieve all volumes for a given storage system

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
    Exports a summary of the write i/o history for all volumes in a session to a csv file between the given times.

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
   Queries all the logical paths for all DS8000 storage systems connected to the CSM server.

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
    Query for all logical paths on the given DS8000 storage system.

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
    Refreshes the configuration for the given storage system.  Issuing this command will force the CSM server
        to requery the hardware for any new or deleted volumes.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        system_id (str): The id of the storage system to be updated.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    refresh_url = f"{url}/storagedevices/{system_id}/refreshconfig"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(refresh_url, headers=headers, verify=verify, cert=cert)


def map_volumes_to_host(url, tk, device_id, force,
                        hostname, is_host_cluster,
                        volumes, scsi="", verify=False, cert=None):
    """
    Map volumes to a host

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_id (str): The id for the storage device    (ex. "FAB3-DEV13")
        force (bool): boolean of whether user would like to force command
        hostname (str): name of the host
        is_host_cluster (bool): boolean variable that indicates whether host is a cluster
        scsi (str)  Specify the scsi id if desired otherwise ""
        volumes (str)  List of volumes to map to the host  (ex. ["mVol0_211115100540","mVol1_211115100540"])

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/storagedevices/mapvolstohost"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    if scsi == "":
        params = {
            "deviceId": device_id,
            "force": force,
            "hostname": hostname,
            "isHostCluster": is_host_cluster,
            "volumes": str(volumes)
        }
    else :
        params = {
            "deviceId": device_id,
            "force": force,
            "hostname": hostname,
            "isHostCluster": is_host_cluster,
            "scsi": scsi,
            "volumes": str(volumes)
        }

    return requests.put(put_url, headers=headers, data=params, verify=verify, cert=cert)


def get_svchosts(url, tk, device_id, verify=False, cert=None):
    """
    Get the hosts defined on the SVC based storage system

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_id (str): The id of the storage system being used. (ex. "FAB3-DEV13")

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/storagedevices/svchost/{device_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def unmap_volumes_to_host(url, tk, device_id, force,
                          hostname, is_host_cluster,
                          volumes, verify=False, cert=None):
    """
    UnMap volumes from a host

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_id (str): The id for the storage device   (ex. "FAB3-DEV13")
        force (bool): boolean of whether user would like to force command
        hostname (str): name of the host
        is_host_cluster (bool): boolean variable that indicates whether host is a cluster
        volumes (str) List of volumes to map to the host  (ex. ["mVol0_211115100540","mVol1_211115100540"])

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/storagedevices/unmapvolstohost"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "deviceId": device_id,
        "force": force,
        "hostname": hostname,
        "isHostCluster": is_host_cluster,
        "volumes": str(volumes)
    }
    return requests.put(put_url, headers=headers, data=params, verify=verify, cert=cert)


def update_connection_info(url, tk, device_ip, device_password, device_username,
                           connection_name, verify=False, cert=None):
    """
    Update the userid/pw for a given storage system

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        device_ip (str): Primary IP address for the storage system.
        device_password (str): New password for the storage system connection
        device_username (str): New user name for the storage system connection
        connection_name (str): Name of the connection. ex. HMC:9.11.114.59

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    put_url = f"{url}/storagedevices/updatehmc"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }

    params = {
        "deviceip": device_ip,
        "devicepassword": device_password,
        "deviceusername": device_username,
        "name": connection_name
    }

    return requests.put(put_url, headers=headers, data=params, verify=verify, cert=cert)


def get_volumes_by_wwn(url, tk, wwn_name, verify=False, cert=None):
    """
    Return the information for all volumes based on the list of WWNs passed in.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        wwn_name (str):  The volume wwn you would like to query or a subset of the volume wwn for a volume list

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    get_url = f"{url}/storagedevices/volumes/volwwn/{wwn_name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {
        "name": wwn_name
    }

    return requests.get(get_url, headers=headers, data=params, verify=verify, cert=cert)