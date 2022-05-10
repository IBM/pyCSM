from authorization import auth
from hardware_service import hardware


class hardwareClient:
    """

    The hardwareClient class can be used to call various hardware level commands such as adding device connections,
    removing device connections, getting lists of volumes, etc.  By using the hardwareClient class you enter the
    username and password only when you instantiate the class which will obtain a token to the server that will be
    used on all calls using the class.  In the event that the token expires, the client will automatically handle the
    error and retrieve a new token prior to retrying the call.
|
    The client makes RESTAPI calls to the server and returns the results.  For more details on what is returned from a call,
    see the `CSM Documentation <https://www.ibm.com/docs/en/csm>`_ for the specific release.
|
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
        self.tk = auth.get_token(self.base_url, username, password,
                                 self.verify, self.cert)

    def get_devices(self, device_type):
        """
        Use this call to return the storage system for all storage systems of the passed in type.

        Args:
            device_type (str): Type of storage device  ex. ds8000 or svc.

        Returns:
             Returns JSON String representing the result of the command.

        """
        resp = hardware.get_devices(self.base_url, self.tk, device_type,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.get_devices(self.base_url, self.tk, device_type,
                                        self.verify, self.cert)
        return resp

    def add_device(self, device_type, device_ip,
                   device_username, device_password,
                   device_port=None, second_ip=None,
                   second_port=None, second_username=None,
                   second_password=None):
        """

        Use this method to create a connection from the CSM server to a specified storage system

        Args:
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
        resp = hardware.add_device(self.base_url, self.tk, device_type,
                                   device_ip, device_port, device_username,
                                   device_password, second_ip, second_port,
                                   second_username, second_password,
                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.add_device(self.base_url, self.tk, device_type,
                                       device_ip, device_port, device_username,
                                       device_password, second_ip, second_port,
                                       second_username, second_password,
                                       self.verify, self.cert)
        return resp

    def remove_device(self, system_id):
        """

        Use this method to remove the connection to the specified storage system

        Args:
             system_id (str): The id of the storage system to be removed.

        Returns:
             JSON String representing the result of the command.
             'I' = successful, 'W' = warning, 'E' = error.

        """
        resp = hardware.remove_device(self.base_url, self.tk, system_id,
                                      self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.remove_device(self.base_url, self.tk, system_id,
                                          self.verify, self.cert)
        return resp

    def update_device_site_location(self, system_id, location):
        """
        Set a user defined site location for a given storage system

        Args:
             system_id (str): The id of the storage system to be updated.
             location (str): The name of the location to set on the storage system.

        Returns:
             JSON String representing the result of the command.
             'I' = successful, 'W' = warning, 'E' = error.

        """
        resp = hardware.update_device_site_location(self.base_url, self.tk,
                                                    system_id, location,
                                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.update_device_site_location(self.base_url, self.tk,
                                                        system_id, location,
                                                        self.verify, self.cert)
        return resp

    def get_volumes(self, system_name):
        """

        Use this method to retrieve all volumes for a given storage system

        Args:
            system_name (str): The name of the storage system.

        Returns:
            JSON String representing all the volumes for that storage system.

        """
        resp = hardware.get_volumes(self.base_url, self.tk, system_name,
                                    self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.get_volumes(self.base_url, self.tk, system_name,
                                        self.verify, self.cert)
        return resp

    def export_vol_writeio_history(self, session_name, start_time, end_time):
        """

        Exports a summary of the write i/o history for all volumes in a session to a csv file between the given times.

        Args:
            session_name (str): The name of the session.
            start_time (str): Start time YYYY-MM-DD.
            end_time (str): End time YYYY-MM-DD.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.

        """
        resp = hardware.export_vol_writeio_history(self.base_url, self.tk,
                                                   session_name, start_time, end_time,
                                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.export_vol_writeio_history(self.base_url, self.tk,
                                                       session_name, start_time,
                                                       end_time, self.cert,
                                                       self.verify)
        return resp

    def get_paths(self):
        """

        Queries all the logical paths for all DS8000 storage systems connected to the CSM server.

        Returns:
            JSON String representing the result of the command.

        """
        resp = hardware.get_paths(self.base_url, self.tk,
                                  self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.get_paths(self.base_url, self.tk,
                                      self.verify, self.cert)
        return resp

    def get_path_on_storage_system(self, system_id):
        """

        Query for all logical paths on the given DS8000 storage system.

        Args:
            system_id (str): The id of the storage system to be updated.

        Returns:
            JSON String representing the result of the command.

        """
        resp = hardware.get_path_on_storage_system(self.base_url, self.tk, system_id,
                                                   self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.get_path_on_storage_system(self.base_url, self.tk, system_id,
                                                       self.verify, self.cert)
        return resp

    def refresh_config(self, system_id):
        """

        Refreshes the configuration for the given storage system.  Issuing this command will force the CSM server
        to requery the hardware for any new or deleted volumes.

        Args:
            system_id (str): The id of the storage system to be refreshed.

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.

        """
        resp = hardware.refresh_config(self.base_url, self.tk, system_id,
                                       self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.refresh_config(self.base_url, self.tk, system_id,
                                           self.verify, self.cert)
        return resp

    def map_volumes_to_host(self, device_id, force,
                            hostname, is_host_cluster, scsi,
                            volumes):
        """
        Use this method to retrieve all volumes for a given storage system

        Args:
            device_id (str): The id for the storage device
            force (bool): boolean of whether user would like to force command
            hostname (str): name of the host
            is_host_cluster (bool): boolean variable that indicates whether host is a cluster
            scsi (str)
            volumes (str)

        Returns:
            JSON String representing all the volumes for that storage system.
        """
        resp = hardware.map_volumes_to_host(self.base_url, self.tk, device_id, force,
                                            hostname, is_host_cluster, scsi,
                                            volumes, self.verify, self.cert)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password,
                                     self.verify, self.cert)
            return hardware.map_volumes_to_host(self.base_url, self.tk, device_id, force,
                                                hostname, is_host_cluster, scsi,
                                                volumes, self.verify, self.cert)
        return resp
