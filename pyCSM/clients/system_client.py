import requests

import pyCSM.authorization.auth as auth
import pyCSM.services.system_service.system_service as system_service


class systemClient:
    """
        The systemClient class can be used to call various server level commands such as creating log packages,
        backing up the server, setting up active/standby support, etc.
        By using the systemClient class you enter the username and password only when you instantiate the class
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
        Creates a system client to store the server_address, port,
        username, password and token once created.
        Can be then used to call methods from the system_service folder.

        Args:
            server_address(str): IP address or hostname of the CSm server
            server_port (str): The port of the CSM server.
            username (str): username for server login.
            password (str): password for server login.
        """
        self.username = username
        self.password = password
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_token(self.base_url, username, password)

    @staticmethod
    def get_properties():
        """
        Returns a dictionary of the current properties and
        their values set for the file.
        """
        return system_service.get_properties()

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
        return system_service.change_properties(property_dictionary)

    def rest_delete(self, url, data, headers):
        """
        Method to call a REST delete call if one is needed but missing from the package.

        url (str):  url for the csm server and the rest call the user wants to run
        data (dict):  Dictionary of variables used in the body of a REST call.
            ex. params = {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
        headers (dict):  Dictionary of variables used in the headers of a REST call except for the token
            ex. headers = {"Accept-Language": properties["language"],
                        "Content-Type": "application/x-www-form-urlencoded"}
        """
        headers["X-Auth-Token"] = self.tk
        resp = requests.delete(url, headers=headers, data=data,
                               verify=system_service.properties["verify"],
                               cert=system_service.properties["cert"])
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            headers["X-Auth-Token"] = self.tk
            return requests.delete(url, headers=headers, data=data,
                                   verify=system_service.properties["verify"],
                                   cert=system_service.properties["cert"])
        return resp

    def rest_put(self, url, data, headers):
        """
        Method to call a REST put call if one is needed but missing from the package.

        url (str):  url for the csm server and the rest call the user wants to run
        data (dict):  Dictionary of variables used in the body of a REST call.
            ex. params = {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
        headers (dict):  Dictionary of variables used in the headers of a REST call except for the token
            ex. headers = {"Accept-Language": properties["language"],
                        "Content-Type": "application/x-www-form-urlencoded"}
        """
        headers["X-Auth-Token"] = self.tk
        resp = requests.put(url, headers=headers, data=data,
                            verify=system_service.properties["verify"],
                            cert=system_service.properties["cert"])
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            headers["X-Auth-Token"] = self.tk
            return requests.put(url, headers=headers, data=data,
                                verify=system_service.properties["verify"],
                                cert=system_service.properties["cert"])
        return resp

    def rest_post(self, url, data, headers):
        """
        Method to call a REST post call if one is needed but missing from the package.

        url (str):  url for the csm server and the rest call the user wants to run
        data (dict):  Dictionary of variables used in the body of a REST call.
            ex. params = {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
        headers (dict):  Dictionary of variables used in the headers of a REST call except for the token
            ex. headers = {"Accept-Language": properties["language"],
                        "Content-Type": "application/x-www-form-urlencoded"}
        """
        headers["X-Auth-Token"] = self.tk
        resp = requests.post(url, headers=headers, data=data,
                             verify=system_service.properties["verify"],
                             cert=system_service.properties["cert"])
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            headers["X-Auth-Token"] = self.tk
            return requests.post(url, headers=headers, data=data,
                                 verify=system_service.properties["verify"],
                                 cert=system_service.properties["cert"])
        return resp

    def rest_get(self, url, data, headers):
        """
        Method to call a REST get call if one is needed but missing from the package.

        url (str):  url for the csm server and the rest call the user wants to run
        data (dict):  Dictionary of variables used in the body of a REST call.
            ex. params = {"type": device_type, "deviceip": device_ip, "deviceport": device_port,}
        headers (dict):  Dictionary of variables used in the headers of a REST call except for the token
            ex. headers = {"Accept-Language": properties["language"],
                        "Content-Type": "application/x-www-form-urlencoded"}
        """
        headers["X-Auth-Token"] = self.tk
        resp = requests.get(url, headers=headers, data=data,
                            verify=system_service.properties["verify"],
                            cert=system_service.properties["cert"])
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            headers["X-Auth-Token"] = self.tk
            return requests.get(url, headers=headers, data=data,
                                verify=system_service.properties["verify"],
                                cert=system_service.properties["cert"])
        return resp

    def create_log_pkg(self):
        """
        This method will package all log files on the server into a .jar file

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.create_log_pkg(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.create_log_pkg(self.base_url, self.tk)
        return resp

    def get_log_pkgs(self):
        """
        Gets a list of log packages and their location on the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
            """
        resp = system_service.get_log_pkgs(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_log_pkgs(self.base_url, self.tk)
        return resp

    def backup_server(self):
        """
        Creates a zip backup of the CSM server data that can
        be used for restoring the server at a later date

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.backup_server(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.backup_server(self.base_url, self.tk)
        return resp

    def get_server_backups(self):
        """
        Retrieves a list of all server backups.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_server_backups(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_server_backups(self.base_url, self.tk)
        return resp

    def backup_server_and_download(self, file_name):
        """
        Create and downloads a server backup.'

        Args:
            file_name:  The file to write the server backup to

        Returns:
            Server backup data that is written to the specified file.
        """
        resp = system_service.backup_server_and_download(self.base_url, self.tk, file_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.backup_server_and_download(self.base_url, self.tk, file_name)
        return resp

    def set_server_as_standby(self, active_server):
        """
        Issue this command to the server that
        you want to be the standby server.
        Sets the server passed in to be the active server.
        All data on the called server will be replaced with
        the data from the active server.

        Args:
            active_server (str): IP or hostname of the active server.
            This method will use the default port.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.set_server_as_standby(self.base_url, self.tk,
                                                    active_server)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.set_server_as_standby(self.base_url, self.tk,
                                                        active_server)
        return resp

    def get_dual_control_state(self):
        """
        Use this method to determine if dual control is currently enabled of disabled on the server.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_dual_control_state(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_dual_control_state(self.base_url, self.tk)
        return resp

    def change_dual_control_state(self, enable):
        """
        Use this method to enable or disable dual control on the CSM server.

        Args:
            enable (bool): Set to 'true' if you want to enable dual control
            or 'false' if you want to disable.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.change_dual_control_state(self.base_url, self.tk, enable)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.change_dual_control_state(self.base_url, self.tk, enable)
        return resp

    def get_dual_control_requests(self):
        """
        Returns a list of dual control events waiting for approval or rejection

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_dual_control_requests(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_dual_control_requests(self.base_url, self.tk)
        return resp

    def approve_dual_control_request(self, id):
        """
        Approve a dual control request

        Args:
            id (int): ID of the request caller wants to approve.
            ID from the 'requestid' field return from getDualControlEvents.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.approve_dual_control_request(self.base_url, self.tk, id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.approve_dual_control_request(self.base_url, self.tk, id)
        return resp

    def reject_dual_control_request(self, id, comment):
        """
        Reject a dual control request

        Args:
            id (int): ID of the request caller wants to approve.
            ID from the 'requestid' field return from getDualControlEvents.
            comment (str): Comment to the creator of the event on why the
            request was rejected.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.reject_dual_control_request(self.base_url, self.tk, id, comment)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.reject_dual_control_request(self.base_url, self.tk, id, comment)
        return resp

    def get_active_standby_status(self):
        """
        Get the current state of the active standby server connection

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_active_standby_status(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_active_standby_status(self.base_url, self.tk)
        return resp

    def reconnect_active_standby_server(self):
        """
        Reconnect the active standby connection

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.reconnect_active_standby_server(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.reconnect_active_standby_server(self.base_url, self.tk)
        return resp

    def remove_active_or_standby_server(self, ha_server):
        """
        This method removes the alternate CSM server.
        If issued to the active server the standby will be removed.

        Args:
            ha_server (str): hostname of the server to remove

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.remove_active_or_standby_server(self.base_url, self.tk, ha_server)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.remove_active_or_standby_server(self.base_url, self.tk, ha_server)
        return resp

    def set_standby_server(self, standby_server, standby_username, standby_password):
        """
        Reconnect the active standby connection

        Args:
            standby_server (str): IP or hostname of the standby server
            standby_username (str): Username to create a connection to the standby server
            standby_password (str): Password for the user to create a connection to the standby server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.set_standby_server(self.base_url, self.tk, standby_server,
                                                 standby_username, standby_password)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.set_standby_server(self.base_url, self.tk, standby_server,
                                                     standby_username, standby_password)
        return resp

    def takeover_standby_server(self):
        """
        Issues a takeover on the standby server making the standby server an active server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.takeover_standby_server(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.takeover_standby_server(self.base_url, self.tk)
        return resp

    def get_log_events(self, count, session=None):
        """
        get a list of the most recent log events

        Args:
            count (int): The number of messages to return
            session (string): (optional) filter messages on session

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_log_events(self.base_url, self.tk,
                                             count, session)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_log_events(self.base_url, self.tk,
                                                 count, session)
        return resp

    def create_and_download_log_pkg(self, file_name):
        """
        This method will package all log files on the server into a .jar file
        that can be used for support - this call is a synchronous call and
        will not return to caller until package is complete. Call make take a while

        Args:
            file_name: Name of the file to write the log package to

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.create_and_download_log_pkg(self.base_url, self.tk, file_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.create_and_download_log_pkg(self.base_url, self.tk, file_name)
        return resp

    def get_session_types(self):
        """
        Get supported session types

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_session_types(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_session_types(self.base_url, self.tk)
        return resp

    def get_server_version(self):
        """
        Get the version of the server being called

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_server_version(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_server_version(self.base_url, self.tk)
        return resp

    def get_volume_counts(self):
        """
        Get a summary of the volume usage on the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system_service.get_volume_counts(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return system_service.get_volume_counts(self.base_url, self.tk)
        return resp
