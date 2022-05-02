from authorization import auth
from hardware_service import hardware


class hardwareClient:
    """
    Client used to store server information, Rest token and
    can call methods in the hardware_service folder.
    """

    def __init__(self, server_address, server_port, username, password,
                 verify=False, cert=None):
        """
        Creates a hardware client to store the server_address,
        port, username, password and token once created.

        Args:
            server_address(str): IP address or hostname of the CSM server
            server_port (str): The port of the CSM server.
            username (str): username for server login.
            password (str): password for server login.
        """
        self.username = username
        self.password = password
        self.cert = cert
        self.verify = verify
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_tk(self.base_url, username, password,
                              self.verify, self.cert)

    def get_devices(self, device_type):
        """
        Uses a get request to get info of all
        the storagedevices of a given type.

        Args:
            device_type (str): Type of storage device  ex. ds8000 or svc.

        Returns:
            Returns JSON String representing the result of the command.
        """
        resp = hardware.get_devices(self.base_url, self.tk, device_type,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.get_devices(self.base_url, self.tk, device_type,
                                        self.verify, self.cert)
        return resp

    def add_device(self, device_type, device_ip, device_port,
                   device_username, device_password, second_ip=None,
                   second_port=None, second_username=None,
                   second_password=None):
        """
        This method will create a connection from the server
        to a specified storage system

        Args:
            device_type (str): Type of storage device  ex. ds8000 or svc.
            device_ip (str): IP address or hostname for the storage system.
            device_port (str): Port to use for the connection
            to the storage system.
            device_username (str): Username for the storage system connection.
            device_password (str): Password for the storage system connection.
            second_ip (str) (OPTIONAL): For DS8000 storage systems,
            the IP address or hostname of a secondary HMC system.
            second_port (str) (OPTIONAL): Port to use for the connection
            to the secondary HMC system for DS8000 connections.
            second_username (str) (OPTIONAL): Username for the connection
            to the secondary HMC system for DS8000 connections.
            second_password (str) (OPTIONAL): Password for the connection
            to the secondary HMC system for DS8000 connections.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
            """
        resp = hardware.add_device(self.base_url, self.tk, device_type,
                                   device_ip, device_port, device_username,
                                   device_password, second_ip, second_port,
                                   second_username, second_password,
                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.add_device(self.base_url, self.tk, device_type,
                                       device_ip, device_port, device_username,
                                       device_password, second_ip, second_port,
                                       second_username, second_password,
                                       self.verify, self.cert)
        return resp

    def remove_device(self, system_id):
        """
        This method will remove a specified storage system connection

        Args:
            system_id (str): The id of the storage system to be removed.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = hardware.remove_device(self.base_url, self.tk, system_id,
                                      self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.remove_device(self.base_url, self.tk, system_id,
                                          self.verify, self.cert)
        return resp

    def update_device(self, system_id, location):
        """
        Set a user defined site location for a given storage system

        Args:
            system_id (str): The id of the storage system to be updated.
            location (str): The name of the location to set
            on the storage system.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
            """
        resp = hardware.update_device(self.base_url, self.tk,
                                      system_id, location,
                                      self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.update_device(self.base_url, self.tk,
                                          system_id, location,
                                          self.verify, self.cert)
        return resp

    def get_volumes(self, system_name):
        """
        This method will return all volumes for a given storage system
        based off the input devicename from the get storage devices query

        Args:
            system_name (str): The name of the storage system.

        Returns:
            JSON String representing all the volumes for that storage system.
        """
        resp = hardware.get_volumes(self.base_url, self.tk, system_name,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.get_volumes(self.base_url, self.tk, system_name,
                                        self.verify, self.cert)
        return resp

    def export_vol_writeio_history(self, session_name, start_time, end_time):
        """
        Exports ESE Box History for a session in csv format to a file.

        Args:
            session_name (str): The name of the session.
            start_time (str): Start time YYYY-MM-DD. Type:str
            end_time (str): End time YYYY-MM-DD.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = hardware.export_vol_writeio_history(self.base_url, self.tk,
                                           session_name, start_time, end_time,
                                           self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.export_vol_writeio_history(self.base_url, self.tk,
                                               session_name, start_time,
                                               end_time, self.cert,
                                               self.verify)
        return resp

    def get_paths(self):
        """
        Queries all the logical paths on the storage system.

        Returns:
            JSON String representing the result of the command.
            """
        resp = hardware.get_paths(self.base_url, self.tk,
                                  self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.get_paths(self.base_url, self.tk,
                                      self.verify, self.cert)
        return resp

    def get_path(self, system_id):
        """
        Query for all paths on the given storage system.

        Args:
            system_id (str): The id of the storage system to be updated.

            Returns:
                JSON String representing the result of the command.
            """
        resp = hardware.get_path(self.base_url, self.tk, system_id,
                                 self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.get_path(self.base_url, self.tk, system_id,
                                     self.verify, self.cert)
        return resp

    def refresh_config(self, system_id):
        """
        Refreshes the configuration for the given storage system.

        Args:
            system_id (str): The id of the storage system to be updated.

        Returns:
            JSON String representing the result of the command.
        """
        resp = hardware.refresh_config(self.base_url, self.tk, system_id,
                                       self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_tk(self.base_url, self.username, self.password,
                                  self.verify, self.cert)
            return hardware.refresh_config(self.base_url, self.tk, system_id,
                                           self.verify, self.cert)
        return resp
