from datetime import datetime
from authorization import auth
from session_service import sessions, schedule, copysets


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

    def __init__(self, server_address, server_port, username, password,
                 verify=False, cert=None):
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
        self.cert = cert
        self.verify = verify
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_token(self.base_url, self.username, self.password,
                                 self.verify, self.cert)

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
        resp = sessions.create_session(self.base_url, self.tk,
                                       name, sess_type, desc,
                                       self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.create_session(self.base_url, self.tk,
                                           name, sess_type, desc,
                                           self.verify, self.cert)
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
        resp = sessions.delete_session(self.base_url, self.tk, name,
                                       self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.delete_session(self.base_url, self.tk, name,
                                           self.verify, self.cert)
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
        resp = sessions.get_session_info(self.base_url, self.tk, name,
                                         self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_session_info(self.base_url, self.tk, name,
                                             self.verify, self.cert)
        return resp

    def get_session_overviews(self):
        """
        This method returns the overview summary
        information for all sessions managed by the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = sessions.get_session_overviews(self.base_url, self.tk,
                                              self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_session_overviews(self.base_url, self.tk,
                                                  self.verify, self.cert)
        return resp

    def get_session_overviews_short(self):
        """
        This method returns minimal overview summary
        information for all sessions managed by the server.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = sessions.get_session_overviews_short(self.base_url, self.tk,
                                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_session_overviews_short(self.base_url, self.tk,
                                                        self.verify, self.cert)
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
        resp = sessions.get_available_commands(self.base_url, self.tk, name,
                                               self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_available_commands(self.base_url, self.tk, name,
                                                   self.verify, self.cert)
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
        resp = sessions.get_session_options(self.base_url, self.tk, name,
                                            self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_session_options(self.base_url, self.tk, name,
                                                self.verify, self.cert)
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
        resp = sessions.modify_session_description(self.base_url, self.tk, name, desc,
                                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.modify_session_description(self.base_url, self.tk, name, desc,
                                                       self.verify, self.cert)
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
        resp = sessions.run_session_command(self.base_url, self.tk, ses_name, com_name,
                                            self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.run_session_command(self.base_url, self.tk, ses_name, com_name,
                                                self.verify, self.cert)
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
        result_dict = sessions.wait_for_state(self.base_url, self.tk,
                                              ses_name, state, minutes, debug,
                                              self.verify, self.cert)
        resp = result_dict["state_reached"]
        if resp.status_code == 401:
            minutes = (datetime.utcnow() - start_time).total_seconds()
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.wait_for_state(self.base_url, self.tk, ses_name,
                                           state, minutes, debug,
                                           self.verify, self.cert)
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
        resp = sessions.sgc_recover(self.base_url, self.tk,
                                    ses_name, com_name, role, backup_id,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.sgc_recover(self.base_url, self.tk, ses_name,
                                        com_name, role, backup_id,
                                        self.verify, self.cert)
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
        resp = sessions.get_backup_details(self.base_url, self.tk,
                                           name, role, backup_id,
                                           self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_backup_details(self.base_url, self.tk,
                                               name, role, backup_id,
                                               self.verify, self.cert)
        return resp

    def get_scheduled_tasks(self):
        """
        Returns a list of scheduled tasks defined on the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule.get_scheduled_tasks(self.base_url, self.tk,
                                            self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return schedule.get_scheduled_tasks(self.base_url, self.tk,
                                                self.verify, self.cert)
        return resp

    def enable_scheduled_task(self, taskid):
        """
        Enable a scheduled task to run based off the
        schedule defined on the task.

        Args:
            taskid (str): ID of the schedule task to enable.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule.enable_scheduled_task(self.base_url, self.tk, taskid,
                                              self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return schedule.enable_scheduled_task(self.base_url, self.tk, taskid,
                                                  self.verify, self.cert)
        return resp

    def disable_scheduled_task(self, taskid):
        """
        Disable a scheduled task from running automatically.

        Args:
            taskid (str): ID of the schedule task to enable.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = schedule.disable_scheduled_task(self.base_url, self.tk, taskid,
                                               self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return schedule.disable_scheduled_task(self.base_url, self.tk, taskid,
                                                   self.verify, self.cert)
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
        resp = schedule.run_scheduled_task(self.base_url, self.tk, taskid, synchronous,
                                           self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return schedule.run_scheduled_task(self.base_url, self.tk, taskid, synchronous,
                                               self.verify, self.cert)
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
        resp = copysets.get_copysets(self.base_url, self.tk, name,
                                     self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.get_copysets(self.base_url, self.tk, name,
                                         self.verify, self.cert)
        return resp

    def add_copysets(self, name, copysets):
        """
        Add copy sets to a given session

        Args:
            name (str): The name of the session.
            copysets (str): List of copy sets to add to the session.
            ex."DS8000:1245.KTLM:VOL:0001", "DS8000:1245.KTLM:VOL:0101"

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = copysets.add_copysets(self.base_url, self.tk, name,
                                     self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.add_copysets(self.base_url, self.tk, name,
                                         self.verify, self.cert)
        return resp

    def remove_copysets(self, name, force, soft):
        """
        Removes Copy Sets from the given session.

        Args:
            name (str): The name of the session.
            force (boolean): Force Set to true if you wish to remove the pair from CSM ignoring hardware errors.
            soft (boolean): Keep base relationships on the hardware but remove the copy set from the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = copysets.remove_copysets(self.base_url, self.tk, name, force, soft,
                                        self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.remove_copysets(self.base_url, self.tk, name, force, soft,
                                            self.verify, self.cert)
        return resp

    def export_copysets(self, file_name):
        """
        Exports copysets as a csv file and downloads it to the calling system.

        Args:
            file_name: Name for the csv file location

        Returns:
            JSON String representing the result of the command.
        """
        resp = copysets.export_copysets(self.base_url, self.tk, file_name,
                                        self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.export_copysets.export_cpyst(self.base_url, self.tk, file_name,
                                                         self.verify, self.cert)
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
        resp = copysets.get_pair_info(self.base_url, self.tk, name,
                                      rolepair, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.get_pair_info.export_cpyst(self.base_url, self.tk, name,
                                                       rolepair, self.verify, self.cert)
        return resp

    def enable_scheduled_task_at_time(self, task_id, start_time):
        """
        Enable the task at the given time

        Args:
            task_id (int): ID of the schedule task to enable
            start_time (str): Time to enable the task.
            Format of yyyy-MM-dd'T'HH-mm.

        Returns:
            JSON String representing the result of the command.
            'I' = successful,'W' = warning, 'E' = error.
        """
        resp = copysets.enable_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                      start_time, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.enable_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                          start_time, self.verify, self.cert)
        return resp

    def run_scheduled_task_at_time(self, task_id, start_time):
        """
        Run a scheduled task immediately.

        Args:
            task_id (int): ID of the schedule task to enable
            start_time (str): Time to enable the task.
            Format of yyyy-MM-dd'T'HH-mm.

        Returns:
            JSON String representing the result of the command.
            'I' = successful,'W' = warning, 'E' = error.
        """
        resp = copysets.run_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                   start_time, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return copysets.run_scheduled_task_at_time(self.base_url, self.tk, task_id,
                                                       start_time, self.verify, self.cert)
        return resp

    def run_backup_command(self, name, role, backup_id, cmd):
        """
        Used to perform a recover or expire for the specified backup.

        Args:
            name (str): The name of the session.
            role: The name of role where the backups reside.
            backup_id: The ID of the backup to send to the run command.
            cmd (str): command to run

        Returns:
            JSON String representing the result of the command.
        """
        resp = sessions.run_backup_command(self.base_url, self.tk,
                                           name, role, backup_id,
                                           cmd, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.run_backup_command(self.base_url, self.tk,
                                               name, role, backup_id,
                                               cmd, self.verify, self.cert)
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
        resp = sessions.export_lss_oos_history(self.base_url, self.tk,
                                               name, rolepair, start_time,
                                               end_time, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.export_lss_oos_history(self.base_url, self.tk,
                                                   name, rolepair, start_time,
                                                   end_time, self.verify, self.cert)
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
        resp = sessions.export_lss_oos_history(self.base_url, self.tk,
                                               name, start_time,
                                               end_time, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.export_lss_oos_history(self.base_url, self.tk,
                                                   name, start_time,
                                                   end_time, self.verify, self.cert)
        return resp

    def get_rpo_history(self, name, rolepair, start_time,
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
        resp = sessions.get_rpo_history(self.base_url, self.tk,
                                        name, rolepair, start_time,
                                        end_time, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return sessions.get_rpo_history(self.base_url, self.tk,
                                            name, rolepair, start_time,
                                            end_time, self.verify, self.cert)
        return resp
