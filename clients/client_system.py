from authorization import auth
from system_service import system


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

    def __init__(self, server_address, server_port, username, password,
                 verify=False, cert=None):
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
        self.cert = cert
        self.verify = verify
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_token(self.base_url, username, password)

    def create_log_pkg(self):
        """
        This method will package all log files on the server into a .jar file

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system.create_log_pkg(self.base_url, self.tk,
                                     self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.create_log_pkg(self.base_url, self.tk,
                                  self.verify, self.cert)

    def get_log_pkgs(self):
        """
        Gets a list of log packages and their location on the server

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
            """
        resp = system.get_log_pkgs(self.base_url, self.tk,
                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return system.get_log_pkgs(self.base_url, self.tk, self.verify,
                                       self.cert)
        return resp

    def backup_server(self):
        """
        Creates a zip backup of the CSM server data that can
        be used for restoring the server at a later date

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system.backup_server(self.base_url, self.tk,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.backup_server(self.base_url, self.tk,
                                 self.verify, self.cert)

    def get_server_backups(self):
        """
        Retrieves a list of all server backups.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system.get_server_backups(self.base_url, self.tk,
                                         self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.get_server_backups(self.base_url, self.tk,
                                      self.verify, self.cert)

    def backup_download_server(self):
        """
        Create and downloads a server backup.

        Returns:
            A file downloaded into the client.
        """
        resp = system.backup_dowload_server(self.base_url, self.tk,
                                            self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.backup_dowload_server(self.base_url, self.tk,
                                         self.verify, self.cert)

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
        resp = system.set_server_as_standby(self.base_url, self.tk,
                                            active_server, self.verify,
                                            self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.set_server_as_standby(self.base_url, self.tk,
                                         active_server, self.verify, self.cert)

    def get_dual_control_state(self):
        """
        Use this method to determine if dual control is currently enabled of disabled on the server.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system.get_dual_control_state(self.base_url, self.tk,
                                             self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.get_dual_control_state(self.base_url, self.tk,
                                          self.verify, self.cert)

    def change_dual_control_state(self, enable):
        """
        Use this method to enable or disable dual control on the CSM server.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = system.get_dual_control_state(self.base_url, self.tk, enable,
                                             self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            system.get_dual_control_state(self.base_url, self.tk, enable,
                                          self.verify, self.cert)
