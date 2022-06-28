from datetime import datetime
import pyCSM.authorization.auth as auth
import pyCSM.services.session_service.session_service as session_service
import pyCSM.services.session_service.schedule_service as schedule_service
import pyCSM.services.session_service.copyset_service as copyset_service


class sessionClient:
    """
        The sessionClient class can be used to call various session level commands such as creating sessions,
        adding or removing copy sets, running commands against the session or scheduled task, etc.
        By using the sessionClient class you enter the username and password only when you instantiate the class
        which will obtain a token to the server that will be used on all calls using the class.
        In the event that the token expires, the client will automatically handle the error and retrieve a new token
        prior to retrying the call.
|
        The client makes RESTAPI calls to the server and returns the results.  For more details on what is returned from a call,
        see the `CSM Documentation <https://www.ibm.com/docs/en/csm>`_ for the specific release.
|
    """

    def __init__(self, server_address, server_port, username, password):
        """
        Creates a session client to store the server_address,
        port, username, password and token once created.
        Can be then used to call methods from the session_service folder.

        Args:
            server_address(str): IP address or hostname of the CSm server.
            server_port (str): The port of the CSM server.
            username (str): username for server login.
            password (str): password for server login.
        """
        self.username = username
        self.password = password
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_token(self.base_url, self.username, self.password)

    def create_session(self, name, sess_type, desc):
        """
        Create a copy services manager session.
        A session must be created before copy sets can
        be placed into the session and managed by the server.

        Args:
            name (str): The name of the session that will be created.
            sess_type: The type of session to create.
            desc (str) (Optional): description for the session
        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.create_session(self.base_url, self.tk,
                                              name, sess_type, desc)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.create_session(self.base_url, self.tk,
                                                  name, sess_type, desc)
        return resp

    def create_session_by_volgroup_name(self, volgroup, type, desc=None):
        """
        Create a copy services manager session and automatically creates a session name
        and populates the session based on the passed in volume group

        Args:
            volgroup (str): The name of the specv volume group that will be created.
            type (str): type The type of session to create. Only Spec V Snapshot supports this today.  Type is the "shortname" for the copy type returned in the /system/sessiontypes query.
            desc (str): description Optional description for the session

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.create_session_by_volgroup_name(self.base_url, self.tk,
                                                               volgroup, type, desc)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.create_session_by_volgroup_name(self.base_url, self.tk,
                                                                   volgroup, type, desc, )
        return resp

    def delete_session(self, name):
        """
        Deletes a copy services manager session.
        Only inactive sessions can be deleted.

         Args:
            name (str): The name of the session that will be deleted.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.delete_session(self.base_url, self.tk, name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.delete_session(self.base_url, self.tk, name)
        return resp

    def get_session_info(self, name):
        """
        This method returns the detailed information for a given session.

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.get_session_info(self.base_url, self.tk, name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_session_info(self.base_url, self.tk, name)
        return resp

    def get_session_overviews(self):
        """
        This method returns the overview summary
        information for all sessions managed by the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.get_session_overviews(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_session_overviews(self.base_url, self.tk)
        return resp

    def get_session_overviews_short(self):
        """
        This method returns minimal overview summary
        information for all sessions managed by the server.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.get_session_overviews_short(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_session_overviews_short(self.base_url, self.tk)
        return resp

    def get_available_commands(self, name):
        """
        Returns the list of available commands for a session
        based on the session's current state

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = session_service.get_available_commands(self.base_url, self.tk, name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_available_commands(self.base_url, self.tk, name)
        return resp

    def get_session_options(self, name):
        """
        Gets the options for the given session.
        The results returned from this method will vary
        depending on the session type.

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_session_options(self.base_url, self.tk, name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_session_options(self.base_url, self.tk, name)
        return resp

    def modify_session_description(self, name, desc):
        """
        Changes the description field for a given session.

        Args:
            name (str): The name of the session.
            desc (str): description for the session

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.modify_session_description(self.base_url, self.tk, name, desc)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.modify_session_description(self.base_url, self.tk, name, desc)
        return resp

    def run_session_command(self, ses_name, com_name):
        """
        Run a command against a session.

        Args:
            ses_name (str): The name of the session.
            com_name (str): The name of the command.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.run_session_command(self.base_url, self.tk, ses_name, com_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.run_session_command(self.base_url, self.tk, ses_name, com_name)
        return resp

    def wait_for_state(self, ses_name, state, minutes, debug=False):
        """
        Runs until the session is in a given state
        or until it times out and returns the results.

        Args:
            ses_name (str): The name of the session.
            state (str): state of the server that user wants to wait for.
            minutes (double): number of minutes before it times out
            debug (boolean): True if you want the state and status to print in console

        Returns:
            A dictionary with "state_reached": boolean for whether the state was reached
            and "session_info": JSON string representing the response of the command
        """
        start_time = datetime.utcnow()
        result_dict = session_service.wait_for_state(self.base_url, self.tk,
                                                     ses_name, state, minutes, debug)
        resp = result_dict["state_reached"]
        if resp.status_code == 401:
            minutes = (datetime.utcnow() - start_time).total_seconds()
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.wait_for_state(self.base_url, self.tk, ses_name,
                                                  state, minutes, debug)
        return result_dict

    def sgc_recover(self, ses_name, com_name, role, backup_id):
        """
        Run a Recover command to the specified Safeguarded Copy backup ID.

        Args:
            ses_name (str): The name of the session.
            com_name (str): The name of the command.
            role: The name of role where the backups reside.
            backup_id: The ID of the backup to send to the run command.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.sgc_recover(self.base_url, self.tk,
                                           ses_name, com_name, role, backup_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.sgc_recover(self.base_url, self.tk, ses_name,
                                               com_name, role, backup_id)
        return resp

    def get_backup_details(self, name, role, backup_id):
        """
        Gets detailed information for a given backup in a session.

        Args:
            name (str): The name of the session.
            role: The name of role where the backups reside.
            backup_id: The ID of the backup to send to the run command.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_backup_details(self.base_url, self.tk,
                                                  name, role, backup_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_backup_details(self.base_url, self.tk,
                                                      name, role, backup_id)
        return resp

    def get_snapshot_details_by_name(self, name, role, snapshot_name):
        """
        Gets detailed information for a given snapshot in a session.

        Args:
            name (str): The name of the session.
            role: The name of role where the snapshot resides.
            snapshot_name: The name of the snapshot to return

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_snapshot_details_by_name(self.base_url, self.tk,
                                                            name, role, snapshot_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_snapshot_details_by_name(self.base_url, self.tk,
                                                                name, role, snapshot_name)
        return resp

    def get_scheduled_tasks(self):
        """
        Returns a list of scheduled tasks defined on the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule_service.get_scheduled_tasks(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return schedule_service.get_scheduled_tasks(self.base_url, self.tk)
        return resp

    @staticmethod
    def get_properties():
        """
        Returns a dictionary of the current properties and
        their values set for the file.
        """
        return session_service.get_properties()

    @staticmethod
    def change_properties(property_dictionary):
        """
        Takes a dictionary of properties and the values that
        user wants to change and changes them in the file.

        Args:
            property_dictionary (dict): Dictionary of the keys and values that need
            to be changed in the file.
            ex. {"language":"en-UK", "verify":True}

        Returns:
            Returns the new properties dictionary.
        """
        return session_service.change_properties(property_dictionary)

    def enable_scheduled_task(self, taskid):
        """
        Enable a scheduled task to run based off the
        schedule defined on the task.

        Args:
            taskid (str): ID of the schedule task to enable.  Use the get_scheduled_task() command to get the task id

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule_service.enable_scheduled_task(self.base_url, self.tk, taskid)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return schedule_service.enable_scheduled_task(self.base_url, self.tk, taskid)
        return resp

    def disable_scheduled_task(self, taskid):
        """
        Disable a scheduled task from running automatically.

        Args:
            taskid (str): ID of the schedule task to enable.  Use the get_scheduled_task() command to get the task id

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule_service.disable_scheduled_task(self.base_url, self.tk, taskid)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return schedule_service.disable_scheduled_task(self.base_url, self.tk, taskid)
        return resp

    def run_scheduled_task(self, taskid, synchronous=False):
        """
        Run a scheduled task immediately.  Synchronous value set to true if call should not return until task
        is complete.  False if you want it to run in the asynchronous after the call completes.

        Args:
            taskid (str): ID of the schedule task to enable.
            synchronous (boolean):  True if you don't want the command to complete until the task completes

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule_service.run_scheduled_task(self.base_url, self.tk, taskid, synchronous)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return schedule_service.run_scheduled_task(self.base_url, self.tk, taskid, synchronous)
        return resp

    def get_copysets(self, name):
        """
        Gets all copy sets and their info for a given session.

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = copyset_service.get_copysets(self.base_url, self.tk, name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.get_copysets(self.base_url, self.tk, name)
        return resp

    def add_copysets(self, name, copyset, roleorder=None):
        """
        Add copy sets to a given session

        Args:
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
        resp = copyset_service.add_copysets(self.base_url, self.tk, name, copyset,
                                            roleorder)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.add_copysets(self.base_url, self.tk, name, copyset,
                                                roleorder)
        return resp

    def remove_copysets(self, name, copysets, force=None, soft=None):
        """
        Removes Copy Sets from the given session.

        Args:
            name (str): The name of the session.
            copyset (str): List of copy sets to add to the session.
                ex. "DS8000:1245.KTLM:VOL:0001", "DS8000:1245.KTLM:VOL:0101"
            force (boolean): Force Set to true if you wish to remove the pair from CSM ignoring hardware errors.
            soft (boolean): Keep base relationships on the hardware but remove the copy set from the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = copyset_service.remove_copysets(self.base_url, self.tk, name, copysets, force, soft)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.remove_copysets(self.base_url, self.tk, name, copysets, force, soft)
        return resp

    def export_copysets(self, name, file_name):
        """
        Exports copysets from given session as a csv file and downloads it to the calling system.

        Args:
            name:  Name of the session to export copysets for
            file_name: Name for the csv file location  (ex.  ""/Users/myuser/CSM/Export/myexport.csv")

        Returns:
            JSON String representing the result of the command.
        """
        resp = copyset_service.export_copysets(self.base_url, self.tk, name, file_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.export_copysets.export_cpyst(self.base_url, self.tk, name, file_name)
        return resp

    def get_pair_info(self, name, rolepair):
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
        resp = copyset_service.get_pair_info(self.base_url, self.tk, name,
                                             rolepair)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.get_pair_info.export_cpyst(self.base_url, self.tk, name,
                                                              rolepair)
        return resp

    def enable_scheduled_task_at_time(self, task_id, start_time):
        """
        Enable the task at the given time

        Args:
            task_id (int): ID of the schedule task to enable
            start_time (str): Time to enable the task. Format of yyyy-MM-dd'T'HH-mm (ex. "2022-07-04T12-00")

        Returns:
            JSON String representing the result of the command.
            'I' = successful,'W' = warning, 'E' = error.
        """
        resp = copyset_service.enable_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                             start_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.enable_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                                 start_time)
        return resp

    def run_scheduled_task_at_time(self, task_id, start_time):
        """
        Run a scheduled task immediately.

        Args:
            task_id (int): ID of the schedule task to enable
            start_time (str): Time to enable the task.  Format of yyyy-MM-dd'T'HH-mm (ex. "2022-07-04T12-00")

        Returns:
            JSON String representing the result of the command.
            'I' = successful,'W' = warning, 'E' = error.
        """
        resp = copyset_service.run_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                          start_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return copyset_service.run_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                              start_time)
        return resp

    def run_backup_command(self, name, role, backup_id, cmd):
        """
        Used to perform a recover or expire for the specified backup.

        Args:
            name (str): The name of the session.
            role: The name of role where the backups reside.
            backup_id: The ID of the backup to send to the run command.
            cmd (str): command to run  (ex.  "Recover Backup", "Expire Backup")

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.run_backup_command(self.base_url, self.tk,
                                                  name, role, backup_id,
                                                  cmd)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.run_backup_command(self.base_url, self.tk,
                                                      name, role, backup_id,
                                                      cmd)
        return resp

    def export_lss_oos_history(self, name, rolepair, start_time,
                               end_time):
        """
        Export LSS OOS History for a session in csv format to a file.

        Args:
            name (str): The name of the session.
            rolepair (str): The role pair name to query
            start_time (str): Start time YYYY-MM-DD
            end_time (str): End time YYYY-MM-DD

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.export_lss_oos_history(self.base_url, self.tk,
                                                      name, rolepair, start_time,
                                                      end_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.export_lss_oos_history(self.base_url, self.tk,
                                                          name, rolepair, start_time,
                                                          end_time)
        return resp

    def export_device_writeio_history(self, name, start_time,
                                      end_time):
        """
        Export ESE Box History for a session in csv format to a file

        Args:
            name (str): The name of the session.
            start_time (str): Start time YYYY-MM-DD
            end_time (str): End time YYYY-MM-DD

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.export_device_writeio_history(self.base_url, self.tk,
                                                             name, start_time,
                                                             end_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.export_device_writeio_history(self.base_url, self.tk,
                                                                 name, start_time,
                                                                 end_time)
        return resp

    def get_rpo_history(self, name, rolepair, start_time,
                        end_time):
        """
        Export ESE Box History for a session in csv format to a file

        Args:
            url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
            tk (str): Rest token for the CSM server.
            name (str): The name of the session.
            start_time (str): Start time YYYY-MM-DD  (ex. "2020-04-22")
            end_time (str): End time YYYY-MM-DD   (ex. "2020-04-22")

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_rpo_history(self.base_url, self.tk,
                                               name, rolepair, start_time,
                                               end_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_rpo_history(self.base_url, self.tk,
                                                   name, rolepair, start_time,
                                                   end_time)
        return resp

    def get_recovered_backups(self, name):
        """
        Gets all recovered backups for Spec V Safeguarded Copy session.

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_recovered_backups(self.base_url, self.tk,
                                                     name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_recovered_backups(self.base_url, self.tk,
                                                         name)
        return resp

    def get_recovered_backup_details(self, name, backup_id):
        """
        Gets the pair information for a specific recovered backup on a specific session

        Args:
            name (str): The name of the session.
            backup_id (int): the backupid to get the detailed info for

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_recovered_backup_details(self.base_url, self.tk,
                                                            name, backup_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_recovered_backup_details(self.base_url, self.tk,
                                                                name, backup_id)
        return resp

    def get_snapshot_clones(self, name):
        """
        Gets all clones for snapshots in for Spec V Safeguarded Copy session.

        Args:
            name (str): The name of the session.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_snapshot_clones(self.base_url, self.tk,
                                                   name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_snapshot_clones(self.base_url, self.tk,
                                                       name)
        return resp

    def get_snapshot_clone_details_by_name(self, name, snapshot_name):
        """
        Gets the pair details for the thin clone of the specified snapshot in the session

        Args:
           name (str): The name of the session.
           snapshot_name (str): the name of the snapshot to get clone details for
           
        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_snapshot_clone_details_by_name(self.base_url, self.tk,
                                                                  name, snapshot_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_snapshot_clone_details_by_name(self.base_url, self.tk,
                                                                      name, snapshot_name)
        return resp

    def get_rolepair_info(self, name, rolepair):
        """
        Gets a summary for a given role pair in a session.

        Args:
            name (str): The name of the session.
            rolepair (str): The name of the role pair.

        Returns:
            JSON String representing the result of the command.
        """
        resp = session_service.get_rolepair_info(self.base_url, self.tk,
                                                 name, rolepair)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return session_service.get_rolepair_info(self.base_url, self.tk,
                                                     name, rolepair)
        return resp
