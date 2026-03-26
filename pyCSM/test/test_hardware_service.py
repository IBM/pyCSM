# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import unittest
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus

import responses

from pyCSM.services.hardware_service import hardware_service


class TestHardwareService(unittest.TestCase):
    """Test cases for hardware service methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://testserver:8088/CSM/web"
        self.token = "test_token_12345"
        self.device_type = "ds8000"
        self.system_id = "TEST_SYSTEM_001"
        
        # Reset properties to default before each test
        hardware_service.properties = {
            "language": "en-US",
            "verify": False,
            "cert": None
        }

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()

    @responses.activate
    def test_get_devices_success(self):
        """Test successful retrieval of storage devices"""
        # Mock response data
        mock_response = {
            "status": "success",
            "data": [
                {
                    "id": "SYSTEM_001",
                    "type": "ds8000",
                    "ip": "192.168.1.100",
                    "name": "DS8K_Primary"
                },
                {
                    "id": "SYSTEM_002",
                    "type": "ds8000",
                    "ip": "192.168.1.101",
                    "name": "DS8K_Secondary"
                }
            ]
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/storagedevices/connectioninfo?type={self.device_type}",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        # Execute test
        response = hardware_service.get_devices(
            self.base_url,
            self.token,
            self.device_type
        )
        
        # Assertions
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_add_device_success(self):
        """Test successful addition of a storage device"""
        device_ip = "192.168.1.100"
        device_username = "admin"
        device_password = "password123"
        device_port = "8452"
        
        mock_response = {
            "status": "I",
            "message": "Device added successfully",
            "data": {
                "id": "NEW_SYSTEM_001",
                "type": self.device_type,
                "ip": device_ip
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/storagedevices",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.add_device(
            self.base_url,
            self.token,
            self.device_type,
            device_ip,
            device_username,
            device_password,
            device_port=device_port
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        # Ensure request_body is a string for comparison
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None
        assert f'deviceip={device_ip}' in request_body
        assert f'deviceusername={device_username}' in request_body
        assert f'devicepassword={device_password}' in request_body
        assert f'deviceport={device_port}' in request_body

    @responses.activate
    def test_remove_device_success(self):
        """Test successful removal of a storage device"""
        system_id = "SYSTEM_TO_REMOVE_001"
        
        mock_response = {
            "status": "I",
            "message": "Device removed successfully",
            "data": {
                "id": system_id,
                "removed": True
            }
        }
        
        responses.add(
            responses.DELETE,
            f"{self.base_url}/storagedevices/{system_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.remove_device(
            self.base_url,
            self.token,
            system_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['removed'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_get_volumes_success(self):
        """Test successful retrieval of volumes for a storage system"""
        system_name = "DS8K_Primary"
        
        # Mock response data with multiple volumes
        mock_response = {
            "status": "success",
            "data": {
                "volumes": [
                    {
                        "id": "0000",
                        "name": "Volume_0000",
                        "capacity": "10737418240",
                        "state": "normal",
                        "pool": "P0",
                        "lss": "00"
                    },
                    {
                        "id": "0001",
                        "name": "Volume_0001",
                        "capacity": "21474836480",
                        "state": "normal",
                        "pool": "P0",
                        "lss": "00"
                    },
                    {
                        "id": "0002",
                        "name": "Volume_0002",
                        "capacity": "53687091200",
                        "state": "normal",
                        "pool": "P1",
                        "lss": "01"
                    }
                ]
            }
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/storagedevices/volumes/{system_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        # Execute test
        response = hardware_service.get_volumes(
            self.base_url,
            self.token,
            system_name
        )
        
        # Assertions
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify volume data
        volumes = response.json()['data']['volumes']
        assert len(volumes) == 3
        assert volumes[0]['id'] == '0000'
        assert volumes[1]['capacity'] == '21474836480'
        assert volumes[2]['pool'] == 'P1'

    @responses.activate
    def test_export_vol_writeio_history_success(self):
        """Test successful export of volume write I/O history"""
        session_name = "TEST_SESSION_001"
        start_time = "2026-01-01"
        end_time = "2026-01-31"
        
        mock_response = {
            "status": "I",
            "message": "Volume write I/O history exported successfully",
            "data": {
                "session": session_name,
                "export_file": "volume_history_2026-01-01_2026-01-31.csv",
                "records_exported": 150
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}/exportesevolumehistory",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.export_vol_writeio_history(
            self.base_url,
            self.token,
            session_name,
            start_time,
            end_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        # Handle both str and bytes types
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None
        assert f'starttime={start_time}' in request_body
        assert f'endtime={end_time}' in request_body

    @responses.activate
    def test_get_paths_success(self):
        """Test successful retrieval of logical paths for all DS8000 storage systems"""
        # Mock response data with multiple paths
        mock_response = {
            "status": "success",
            "data": {
                "paths": [
                    {
                        "system_id": "DS8K_001",
                        "path_id": "PATH_001",
                        "source_port": "I0001",
                        "target_port": "5005076306FFD1A0",
                        "state": "online",
                        "type": "FC"
                    },
                    {
                        "system_id": "DS8K_001",
                        "path_id": "PATH_002",
                        "source_port": "I0002",
                        "target_port": "5005076306FFD1A1",
                        "state": "online",
                        "type": "FC"
                    },
                    {
                        "system_id": "DS8K_002",
                        "path_id": "PATH_003",
                        "source_port": "I0001",
                        "target_port": "5005076306FFD2A0",
                        "state": "offline",
                        "type": "FC"
                    }
                ]
            }
        }
        
        # Register mock response
        responses.add(
            responses.GET,
            f"{self.base_url}/storagedevices/paths",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        # Execute test
        response = hardware_service.get_paths(
            self.base_url,
            self.token
        )
        
        # Assertions
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify path data
        paths = response.json()['data']['paths']
        assert len(paths) == 3
        assert paths[0]['system_id'] == 'DS8K_001'
        assert paths[1]['state'] == 'online'
        assert paths[2]['system_id'] == 'DS8K_002'


    @responses.activate
    def test_add_zos_host_success(self):
        """Test successful addition of a z/OS host connection"""
        host_ip = "192.168.2.100"
        username = "zosadmin"
        password = "zospass123"
        host_port = "6800"
        
        mock_response = {
            "status": "I",
            "message": "z/OS host connection added successfully",
            "data": {
                "host_ip": host_ip,
                "host_port": host_port,
                "username": username,
                "connection_status": "active"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/storagedevices/zoshost",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.add_zos_host(
            self.base_url,
            self.token,
            host_ip,
            password,
            username,
            host_port
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None, "Request body should not be None"
        assert f'hostip={host_ip}' in request_body
        assert f'username={username}' in request_body
        assert f'password={password}' in request_body
        assert f'hostport={host_port}' in request_body

    @responses.activate
    def test_get_zos_candidate_success(self):
        """Test successful retrieval of z/OS candidate devices"""
        mock_response = {
            "status": "success",
            "data": {
                "candidates": [
                    {
                        "device_id": "DS8000:BOX:2107.KXZ91",
                        "device_type": "DS8000",
                        "serial_number": "2107.KXZ91",
                        "status": "available",
                        "attached": True
                    },
                    {
                        "device_id": "DS8000:BOX:2107.ABC12",
                        "device_type": "DS8000",
                        "serial_number": "2107.ABC12",
                        "status": "available",
                        "attached": True
                    },
                    {
                        "device_id": "DS8000:BOX:2107.XYZ99",
                        "device_type": "DS8000",
                        "serial_number": "2107.XYZ99",
                        "status": "unavailable",
                        "attached": False
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/storagedevices/zoscandidate",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.get_zos_candidate(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify candidate device data
        candidates = response.json()['data']['candidates']
        assert len(candidates) == 3
        assert candidates[0]['device_id'] == 'DS8000:BOX:2107.KXZ91'
        assert candidates[1]['attached'] is True
        assert candidates[2]['status'] == 'unavailable'

    @responses.activate
    def test_remove_zos_host_success(self):
        """Test successful removal of a z/OS host connection"""
        host_ip = "192.168.2.100"
        host_port = "6800"
        
        mock_response = {
            "status": "I",
            "message": "z/OS host connection removed successfully",
            "data": {
                "host_ip": host_ip,
                "host_port": host_port,
                "removed": True
            }
        }
        
        responses.add(
            responses.DELETE,
            f"{self.base_url}/storagedevices/zoshost",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = hardware_service.remove_zos_host(
            self.base_url,
            self.token,
            host_ip,
            host_port
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None, "Request body should not be None"
        assert f'hostip={host_ip}' in request_body
        assert f'hostport={host_port}' in request_body

    @responses.activate
    def test_add_zos_cert_success(self):
        """Test successful addition of a z/OS certificate"""
        # Create a temporary mock certificate file
        import tempfile
        import os
        
        # Create a temporary file to simulate a certificate
        with tempfile.NamedTemporaryFile(mode='w', suffix='.crt', delete=False) as cert_file:
            cert_file.write("-----BEGIN CERTIFICATE-----\n")
            cert_file.write("MIIDXTCCAkWgAwIBAgIJAKJ5VZ5Z5Z5ZMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV\n")
            cert_file.write("BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX\n")
            cert_file.write("-----END CERTIFICATE-----\n")
            cert_path = cert_file.name
        
        try:
            mock_response = {
                "status": "I",
                "message": "z/OS certificate added successfully",
                "data": {
                    "certificate_added": True,
                    "certificate_name": os.path.basename(cert_path)
                }
            }
            
            responses.add(
                responses.POST,
                f"{self.base_url}/storagedevices/zoscert",
                json=mock_response,
                status=HTTPStatus.OK.value,
            )
            
            response = hardware_service.add_zos_cert(
                self.base_url,
                self.token,
                cert_path
            )
            
            assert response.status_code == HTTPStatus.OK.value
            assert response.json()['status'] == 'I'
            assert len(responses.calls) == 1
            assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
            assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
            
        finally:
            # Clean up the temporary file
            if os.path.exists(cert_path):
                os.unlink(cert_path)

    @responses.activate
    def test_add_zos_device_success(self):
        """Test successful addition of a storage system through z/OS host connection"""
        device_id = "DS8000.BOX.5996.LM921"
        
        mock_response = {
            "status": "I",
            "message": "z/OS device added successfully",
            "data": {
                "device_id": device_id,
                "added": True,
                "connection_type": "zos"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/storagedevices/zosdevice",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.add_zos_device(
            self.base_url,
            self.token,
            device_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['added'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify request parameters
        request_body: bytes | str | None = responses.calls[0].request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode('application/x-www-form-urlencoded')
        assert request_body is not None
        assert f'deviceid={device_id}' in request_body

    @responses.activate
    def test_map_volumes_to_host_success(self):
        """Test successful mapping of volumes to a host"""
        device_id = "FAB3-DEV13"
        force = False
        hostname = "test-host-01"
        is_host_cluster = False
        scsi = "1"
        volumes = ["mVol0_211115100540", "mVol1_211115100540"]
        
        mock_response = {
            "status": "I",
            "message": "Volumes mapped to host successfully",
            "data": {
                "device_id": device_id,
                "hostname": hostname,
                "volumes_mapped": volumes,
                "scsi_id": scsi
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/storagedevices/mapvolstohost",
            json=mock_response,
            status=HTTPStatus.OK.value,

        )
        
        response = hardware_service.map_volumes_to_host(
            self.base_url,
            self.token,
            device_id,
            force,
            hostname,
            is_host_cluster,
            volumes,
            scsi=scsi
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None
        assert f'deviceId={device_id}' in request_body
        assert f'hostname={hostname}' in request_body
        assert f'scsi={scsi}' in request_body

    @responses.activate
    def test_unmap_volumes_to_host_success(self):
        """Test successful unmapping of volumes from a host"""
        device_id = "FAB3-DEV13"
        force = False
        hostname = "test-host-01"
        is_host_cluster = False
        volumes = ["mVol0_211115100540", "mVol1_211115100540"]
        
        mock_response = {
            "status": "I",
            "message": "Volumes unmapped from host successfully",
            "data": {
                "device_id": device_id,
                "hostname": hostname,
                "volumes_unmapped": volumes
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/storagedevices/unmapvolstohost",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.unmap_volumes_to_host(
            self.base_url,
            self.token,
            device_id,
            force,
            hostname,
            is_host_cluster,
            volumes
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify request parameters
        request_body = responses.calls[0].request.body
        if isinstance(request_body, bytes):
            request_body = request_body.decode('utf-8')
        assert request_body is not None
        assert f'deviceId={device_id}' in request_body
        assert f'hostname={hostname}' in request_body

    @responses.activate
    def test_get_zos_host_success(self):
        """Test successful retrieval of z/OS host connections"""
        mock_response = {
            "status": "success",
            "data": {
                "zos_hosts": [
                    {
                        "host_ip": "192.168.2.100",
                        "host_port": "6800",
                        "username": "zosadmin1",
                        "connection_status": "active",
                        "last_connected": "2026-03-10T10:30:00Z"
                    },
                    {
                        "host_ip": "192.168.2.101",
                        "host_port": "6800",
                        "username": "zosadmin2",
                        "connection_status": "active",
                        "last_connected": "2026-03-10T09:15:00Z"
                    },
                    {
                        "host_ip": "192.168.2.102",
                        "host_port": "6801",
                        "username": "zosadmin3",
                        "connection_status": "inactive",
                        "last_connected": "2026-03-09T14:20:00Z"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/storagedevices/zoshost",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = hardware_service.get_zos_host(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify z/OS host data
        zos_hosts = response.json()['data']['zos_hosts']
        assert len(zos_hosts) == 3
        assert zos_hosts[0]['host_ip'] == '192.168.2.100'
        assert zos_hosts[1]['connection_status'] == 'active'
        assert zos_hosts[2]['host_port'] == '6801'


if __name__ == '__main__':
    unittest.main()

# Made with Bob
