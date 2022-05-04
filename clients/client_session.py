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
            sessions.create_session(self.base_url, self.tk,
                                    name, sess_type, desc,
                                    self.verify, self.cert)

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
            sessions.delete_session(self.base_url, self.tk, name,
                                    self.verify, self.cert)

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
            sessions.modify_session_description(self.base_url, self.tk, name, desc,
                                 self.verify, self.cert)

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
            sessions.run_session_command(self.base_url, self.tk, ses_name, com_name,
                                 self.verify, self.cert)

    def wait_for_state(self, ses_name, state, minutes, debug=False):
        """
        Runs until the session is in a given state
        or until it times out and returns the results.

        Args:
            ses_name (str): The name of the session.
            state (str): state of the server that user wants to wait for.
            minutes (double): amount of minutes before it times out
            debug (boolean): True if you want the state
            and status to print in console

        Returns:
            JSON String representing the result of the command.
        """
        start_time = datetime.utcnow()
        resp = sessions.wait_for_state(self.base_url, self.tk,
                                       ses_name, state, minutes, debug,
                                       self.verify, self.cert)
        if resp.status_code == 401:
            minutes = (datetime.utcnow() - start_time).total_seconds()
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            sessions.wait_for_state(self.base_url, self.tk, ses_name,
                                    state, minutes, debug,
                                    self.verify, self.cert)

    def sgc_recover(self, ses_name, com_name, role, backup_id):
        """
        Run a specified command that requires a backup ID parameter
        on a specified SGC session.

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
            sessions.sgc_recover(self.base_url, self.tk, ses_name,
                                 com_name, role, backup_id,
                                 self.verify, self.cert)

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
            schedule.enable_scheduled_task(self.base_url, self.tk, taskid,
                                           self.verify, self.cert)

    def disable_scheduled_task(self, taskid):
        """
        Disable a scheduled task.

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
            schedule.disable_scheduled_task(self.base_url, self.tk, taskid,
                                            self.verify, self.cert)

    def run_scheduled_task(self, taskid, synchronous):
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
            schedule.run_scheduled_task(self.base_url, self.tk, taskid, synchronous,
                                        self.verify, self.cert)

    def get_copysets(self, name):
        """
        Gets all pairs and their info for a given copy set.

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
            copysets.add_copysets(self.base_url, self.tk, name,
                               self.verify, self.cert)

    def remove_copysets(self, name, force, soft):
        """
        Removes Copy Sets from the given session.

        Args:
            name (str): The name of the session.
            force (boolean): Force Set to true if you wish to
            remove the pair from CSM ignoring hardware errors.
            soft (boolean): Keep base relationships on the
            hardware but remove the copy set from the session.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = copysets.remove_copysets(self.base_url, self.tk, name, force, soft,
                                     self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            copysets.remove_copysets(self.base_url, self.tk, name, force, soft,
                                  self.verify, self.cert)

    def export_copysets(self, file_name):
        """
        Exports copysets as a csv file.

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
            copysets.export_copysets.export_cpyst(self.base_url, self.tk, file_name,
                                           self.verify, self.cert)
