import json
import time
from datetime import datetime
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


def create_session(url, tk, name, sess_type, desc=None):
    """
    Create a copy services manager session. A session must be created before
    copy sets can be placed into the session and managed by the server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session that will be created.
        sess_type: The type of session to create.
        desc (str) (Optional): description for the session
    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    create_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "type": sess_type,
        "description": desc
    }
    return requests.put(create_url, headers=headers, data=params,
                        verify=properties["verify"], cert=properties["cert"])


def delete_session(url, tk, name):
    """
    Deletes a copy services manager session.
    Only inactive sessions can be deleted.

     Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session that will be deleted.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    delete_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.delete(delete_url, headers=headers,
                           verify=properties["verify"], cert=properties["cert"])


def get_session_info(url, tk, name):
    """
    This method returns the detailed information for a given session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    getsi_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(getsi_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_session_overviews(url, tk):
    """
    This method returns the overview summary information
    for all sessions managed by the server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    gets_url = f"{url}/sessions"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(gets_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_session_overviews_short(url, tk):
    """
    This method returns minimal overview summary information
    for all sessions managed by the server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    gets_url = f"{url}/sessions/short"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(gets_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_available_commands(url, tk, name):
    """
    Returns the list of available commands
    for a session based on the session's current state

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    getc_url = f"{url}/sessions/{name}/availablecommands"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(getc_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_session_options(url, tk, name):
    """
    Gets the options for the given session. The results returned
    from this method will vary depending on the session type.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
    """
    geto_url = f"{url}/sessions/{name}/options"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(geto_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def modify_session_description(url, tk, name, desc):
    """
    Changes the description field for a given session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        desc (str): description for the session

    Returns:
        JSON String representing the result of the command.
    """
    desc_url = f"{url}/sessions/{name}/description"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "description": desc
    }
    return requests.post(desc_url, headers=headers, data=params,
                         verify=properties["verify"], cert=properties["cert"])


def run_session_command(url, tk, ses_name, com_name):
    """
    Run a command against a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        com_name (str): The name of the command.

    Returns:
        JSON String representing the result of the command.
    """
    runc_url = f"{url}/sessions/{ses_name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "cmd": com_name
    }
    return requests.post(runc_url, headers=headers, data=params,
                         verify=properties["verify"], cert=properties["cert"])


def wait_for_state(url, tk, ses_name, state, minutes=5, debug=False):
    """
    Runs until the session is in a given state
    or until it times out and returns the results.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        state (str): state of the server that user wants to wait for.
        minutes (double): number of minutes before it times out
        debug (boolean): True if you want the state and status to print in console

    Returns:
        A dictionary with "state_reached": boolean for whether the state was reached
        and "session_info": JSON string representing the response of the command
    """
    start_time = datetime.utcnow()
    resp = get_session_info(url, tk, ses_name, verify=properties["verify"], cert=properties["cert"])
    time_passed = (datetime.utcnow() - start_time).total_seconds()
    while str(json.loads(resp.text)['state']) != state \
            and time_passed < minutes * 60:
        if debug:
            print("Status: " + json.loads(resp.text)['status']
                  + ", State: " + json.loads(resp.text)['state'])
        time.sleep(10)
        resp = get_session_info(url, tk, ses_name)
        if resp.status_code == 401:
            return {"state_reached": False, "session_info": resp}
        time_passed = (datetime.utcnow() - start_time).total_seconds()

    if time_passed < minutes * 60:
        if debug:
            print(f"Session has reached {state} state.")
        return {"state_reached": True, "session_info": resp}
    else:
        if debug:
            print(f'Timeout: Command exceeded {minutes} minutes.')
        return {"state_reached": False, "session_info": resp}


def sgc_recover(url, tk, ses_name, com_name, role, backup_id):
    """
   Run a Recover command to the specified Safeguarded Copy backup ID.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        com_name (str): The name of the command.
        role: The name of role where the backups reside.
        backup_id: The ID of the backup to send to the run command.

    Returns:
        JSON String representing the result of the command.
    """
    rec_url = f"{url}/sessions/{ses_name}/backups/{role}/{backup_id}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "cmd": com_name
    }
    return requests.post(rec_url, headers=headers, data=params,
                         verify=properties["verify"], cert=properties["cert"])


def get_backup_details(url, tk, name, role, backup_id):
    """
    Gets detailed information for a given backup in a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        role: The name of role where the backups reside.
        backup_id: The ID of the backup to send to the run command.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/backups/{role}/{backup_id}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_snapshot_details_by_name(url, tk, name, role, snapshot_name):
    """
    Gets detailed information for a given snapshot in a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        role: The name of role where the snapshot resides.
        snapshot_name: The name of the snapshot to return

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/snapshotsByName/{role}/{snapshot_name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def run_backup_command(url, tk, name, role, backup_id, cmd):
    """
    Used to perform a recover or expire for the specified backup.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        role: The name of role where the backups reside.
        backup_id: The ID of the backup to send to the run command.
        cmd (str): command to run  (ex.  "Recover Backup", "Expire Backup")

    Returns:
        JSON String representing the result of the command.
    """
    post_url = f"{url}/sessions/{name}/backups/{role}/{backup_id}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "cmd": cmd
    }
    return requests.post(post_url, headers=headers, data=params, verify=properties["verify"], cert=properties["cert"])


def export_lss_oos_history(url, tk, name, rolepair, start_time,
                           end_time):
    """
    Export LSS OOS History for a session in csv format to a file

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        rolepair (str): The role pair name to query
        start_time (str): Start time YYYY-MM-DD
        end_time (str): End time YYYY-MM-DD

    Returns:
        JSON String representing the result of the command.
    """
    put_url = f"{url}/sessions/{name}/exportlssooshistory/{rolepair}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "starttime": start_time,
        "endtime": end_time
    }
    return requests.put(put_url, headers=headers, data=params, verify=properties["verify"], cert=properties["cert"])


def export_device_writeio_history(url, tk, name, start_time,
                                  end_time):
    """
    Export ESE Box History for a session in csv format to a file

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        start_time (str): Start time YYYY-MM-DD
        end_time (str): End time YYYY-MM-DD

    Returns:
        JSON String representing the result of the command.
    """
    put_url = f"{url}/sessions/{name}/exporteseboxhistory"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "starttime": start_time,
        "endtime": end_time
    }
    return requests.put(put_url, headers=headers, data=params, verify=properties["verify"], cert=properties["cert"])


def get_rpo_history(url, tk, name, rolepair, start_time,
                    end_time):
    """
    Export ESE Box History for a session in csv format to a file

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        start_time (str): Start time YYYY-MM-DD (ex. "2020-04-22")
        end_time (str): End time YYYY-MM-DD (ex. "2020-04-22")

    Returns:
        JSON String representing the result of the command.
    """
    put_url = f"{url}/sessions/{name}/getrpohistory/{rolepair}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "starttime": start_time,
        "endtime": end_time
    }
    return requests.put(put_url, headers=headers, data=params, verify=properties["verify"], cert=properties["cert"])


def get_recovered_backups(url, tk, name):
    """
    Gets all recovered backups for Spec V Safeguarded Copy session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/recoveredbackups"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_recovered_backup_details(url, tk, name, backup_id):
    """
    Gets the pair information for a specific recovered backup on a specific session

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        backup_id (int): the backupid to get the detailed info for

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/recoveredbackups/{backup_id}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_snapshot_clones(url, tk, name):
    """
    Gets all clones for snapshots in for Spec V Safeguarded Copy session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/clones"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def create_session_by_volgroup_name(url, tk, volgroup, type, desc=None):
    """
    Create a copy services manager session and automatically creates a session name
    and populates the session based on the passed in volume group

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        volgroup (str): The name of the specv volume group that will be created.
        type (str): type The type of session to create. Only Spec V Snapshot supports this today. Type is the "shortname" for the copy type returned in the /system/sessiontypes query.
        desc (str): description Optional description for the session

    Returns:
        JSON String representing the result of the command.
    """
    put_url = f"{url}/sessions/byvolgroup"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "volgroup": volgroup,
        "type": type,
        "description": desc
    }
    return requests.put(put_url, headers=headers, data=params, verify=properties["verify"], cert=properties["cert"])


def get_snapshot_clone_details_by_name(url, tk, name, snapshot_name):
    """
    Gets the pair details for the thin clone of the specified snapshot in the session

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        snapshot_name (str): the name of the snapshot to get clone details for

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/clonesBySnapshotName/{snapshot_name}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])


def get_rolepair_info(url, tk, name, rolepair):
    """
    Gets a summary for a given role pair in a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        rolepair (str): The name of the role pair.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/sequences/{rolepair}"
    headers = {
        "Accept-Language": properties["language"],
        "X-Auth-Token": str(tk),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return requests.get(get_url, headers=headers, verify=properties["verify"], cert=properties["cert"])
