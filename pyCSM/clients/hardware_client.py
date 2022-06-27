import pyCSM.authorization.auth as auth
import pyCSM.services.hardware_service.hardware_service as hardware_service


class hardwareClient:
    """

    The hardwareClient class can be used to call various hardware level commands such as adding device connections,
    removing device connections, getting lists of volumes, etc.  By using the hardwareClient class you enter the
    username and password only when you instantiate the class which will obtain a token to the server that will be
    used on all calls using the class.  In the event that the token expires, the client will automatically handle the
    error and retrieve a new token prior to retrying the call.
    The client makes RESTAPI calls to the server and returns the results.  For more details on what is returned from a call,
    see the `CSM Documentation <https://www.ibm.com/docs/en/csm>`_ for the specific release.
    """

    def __init__(self, server_address, server_port, username, password):
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
        self.base_url = f"https://{server_address}:{server_port}/CSM/web"
        self.tk = auth.get_token(self.base_url, username, password)

    @staticmethod
    def get_properties():
        """
        Returns a dictionary of the current properties and
        their values set for the file.
        """
        return hardware_service.get_properties()

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
        return hardware_service.change_properties(property_dictionary)

    def get_devices(self, device_type):
        """
        Use this call to return the storage system for all storage systems of the passed in type.

        Args:
            device_type (str): Type of storage device  ex. ds8000 or svc.

        Returns:
             Returns JSON String representing the result of the command.

        """
        resp = hardware_service.get_devices(self.base_url, self.tk, device_type)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_devices(self.base_url, self.tk, device_type)
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
        resp = hardware_service.add_device(self.base_url, self.tk, device_type,
                                           device_ip, device_username,
                                           device_password, device_port, second_ip, second_port,
                                           second_username, second_password)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.add_device(self.base_url, self.tk, device_type,
                                               device_ip, device_username,
                                               device_password, device_port,
                                               second_ip, second_port,
                                               second_username, second_password)
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
        resp = hardware_service.remove_device(self.base_url, self.tk, system_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.remove_device(self.base_url, self.tk, system_id)
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
        resp = hardware_service.update_device_site_location(self.base_url, self.tk,
                                                            system_id, location)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.update_device_site_location(self.base_url, self.tk,
                                                                system_id, location)
        return resp

    def get_volumes(self, system_name):
        """

        Use this method to retrieve all volumes for a given storage system

        Args:
            system_name (str): The name of the storage system.

        Returns:
            JSON String representing all the volumes for that storage system.

        """
        resp = hardware_service.get_volumes(self.base_url, self.tk, system_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_volumes(self.base_url, self.tk, system_name)
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
        resp = hardware_service.export_vol_writeio_history(self.base_url, self.tk,
                                                           session_name, start_time, end_time)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.export_vol_writeio_history(self.base_url, self.tk,
                                                               session_name, start_time,
                                                               end_time)
        return resp

    def get_paths(self):
        """

        Queries all the logical paths for all DS8000 storage systems connected to the CSM server.

        Returns:
            JSON String representing the result of the command.

        """
        resp = hardware_service.get_paths(self.base_url, self.tk)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_paths(self.base_url, self.tk)
        return resp

    def get_path_on_storage_system(self, system_id):
        """

        Query for all logical paths on the given DS8000 storage system.

        Args:
            system_id (str): The id of the storage system to be updated.

        Returns:
            JSON String representing the result of the command.

        """
        resp = hardware_service.get_path_on_storage_system(self.base_url, self.tk, system_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_path_on_storage_system(self.base_url, self.tk, system_id)
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
        resp = hardware_service.refresh_config(self.base_url, self.tk, system_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.refresh_config(self.base_url, self.tk, system_id)
        return resp

    def map_volumes_to_host(self, device_id, force,
                            hostname, is_host_cluster,
                            volumes, scsi=""):
        """
        Use this method to retrieve all volumes for a given storage system

        Args:
            device_id (str): The id for the storage device.   (ex. "FAB3-DEV13")
            force (bool): boolean of whether user would like to force command
            hostname (str): name of the host
            is_host_cluster (bool): boolean variable that indicates whether host is a cluster
            scsi (str) Specify the scsi id if desired otherwise ""
            volumes (str)  List of volumes to map to the host  (ex. ["mVol0_211115100540","mVol1_211115100540"])

        Returns:
            JSON String representing all the volumes for that storage system.
        """
        resp = hardware_service.map_volumes_to_host(self.base_url, self.tk, device_id, force,
                                                    hostname, is_host_cluster,
                                                    volumes, scsi)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.map_volumes_to_host(self.base_url, self.tk, device_id, force,
                                                        hostname, is_host_cluster,
                                                        volumes, scsi)
        return resp

    def get_svchosts(self, device_id):
        """
        Get the hosts defined on the SVC based storage system

        Args:
            device_id (str): The id of the storage system being used.  (ex. "FAB3-DEV13")

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = hardware_service.get_svchosts(self.base_url, self.tk, device_id)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_svchosts(self.base_url, self.tk, device_id)
        return resp

    def unmap_volumes_to_host(self, device_id, force,
                              hostname, is_host_cluster,
                              volumes):
        """
        Use this method to retrieve all volumes for a given storage system

        Args:
            device_id (str): The id for the storage device   (ex. "FAB3-DEV13")
            force (bool): boolean of whether user would like to force command
            hostname (str): name of the host
            is_host_cluster (bool): boolean variable that indicates whether host is a cluster
            volumes (str) List of volumes to map to the host  (ex. ["mVol0_211115100540","mVol1_211115100540"])

        Returns:
            JSON String representing all the volumes for that storage system.
        """
        resp = hardware_service.unmap_volumes_to_host(self.base_url, self.tk, device_id, force,
                                                      hostname, is_host_cluster,
                                                      volumes)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.unmap_volumes_to_host(self.base_url, self.tk, device_id, force,
                                                          hostname, is_host_cluster,
                                                          volumes)
        return resp

    def update_connection_info(self, device_ip, device_password, device_username,
                               connection_name):
        """
        Update the userid/pw for a given storage system

        Args:
            device_ip (str): Primary IP address for the storage system.
            device_password (str): New password for the storage system connection
            device_username (str): New user name for the storage system connection
            connection_name (str): Name of the connection. ex. HMC:9.11.114.59

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = hardware_service.update_connection_info(self.base_url, self.tk, device_ip,
                                                       device_password, device_username, connection_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.update_connection_info(self.base_url, self.tk, device_ip,
                                                           device_password, device_username, connection_name)
        return resp

    def get_volumes_by_wwn(self, wwn_name):
        """
        Return the information for all volumes based on the list of WWNs passed in.

        Args:
            wwn_name (str): The volume wwn you would like to query or a subset of the volume wwn for a volume list

        Returns:
            JSON String representing the result of the command.
            'I' = successful, 'W' = warning, 'E' = error.
        """
        resp = hardware_service.get_volumes_by_wwn(self.base_url, self.tk, wwn_name)
        if resp.status_code == 401:
            self.tk = auth.get_token(self.base_url, self.username, self.password)
            return hardware_service.get_volumes_by_wwn(self.base_url, self.tk, wwn_name)
        return resp
