# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import unittest
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus
import tempfile
import os

import responses

from pyCSM.services.system_service import system_service


class TestSystemService(unittest.TestCase):
    """Test cases for system service methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://testserver:8088/CSM/web"
        self.token = "test_token_12345"
        
        # Reset properties to default before each test
        system_service.properties = {
            "language": "en-US",
            "verify": False,
            "cert": None
        }

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()

    """LOG PACKAGES"""

    @responses.activate
    def test_create_log_pkg_success(self):
        """Test successful creation of log package"""
        mock_response = {
            "status": "I",
            "message": "Log package created successfully",
            "data": {
                "package_name": "csm_logs_2026-03-16_10-30-00.jar",
                "package_size": "15728640"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/logpackages",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = system_service.create_log_pkg(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert 'package_name' in response.json()['data']
        assert response.json()['data']['package_name'].endswith('.jar')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_get_log_pkgs_success(self):
        """Test successful retrieval of log packages"""
        mock_response = {
            "status": "success",
            "data": {
                "packages": [
                    {
                        "name": "csm_logs_2026-03-16_10-30-00.jar",
                        "size": "15728640"
                    },
                    {
                        "name": "csm_logs_2026-03-15_14-20-00.jar",
                        "size": "12582912"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/logpackages",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = system_service.get_log_pkgs(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify package data
        packages = response.json()['data']['packages']
        assert len(packages) == 2
        assert packages[0]['name'] == 'csm_logs_2026-03-16_10-30-00.jar'
        assert packages[1]['size'] == '12582912'

    """BACKUPS"""

    @responses.activate
    def test_backup_server_success(self):
        """Test successful creation of server backup"""
        mock_response = {
            "status": "I",
            "message": "Server backup created successfully",
            "data": {
                "backup_name": "csm_backup_2026-03-16_11-45-00.zip",
                "backup_size": "52428800",
                "created_at": "2026-03-16T11:45:00Z",
                "location": "/opt/ibm/csm/backups/csm_backup_2026-03-16_11-45-00.zip"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/backupserver",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = system_service.backup_server(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert 'backup_name' in response.json()['data']
        assert response.json()['data']['backup_name'].endswith('.zip')
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_get_server_backups_success(self):
        """Test successful retrieval of server backups"""
        mock_response = {
            "status": "success",
            "data": {
                "backups": [
                    {
                        "name": "csm_backup_2026-03-16_11-45-00.zip",
                        "size": "52428800",
                        "created_at": "2026-03-16T11:45:00Z",
                        "location": "/opt/ibm/csm/backups/csm_backup_2026-03-16_11-45-00.zip"
                    },
                    {
                        "name": "csm_backup_2026-03-15_10-30-00.zip",
                        "size": "48234496",
                        "created_at": "2026-03-15T10:30:00Z",
                        "location": "/opt/ibm/csm/backups/csm_backup_2026-03-15_10-30-00.zip"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/backupserver",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = system_service.get_server_backups(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify backup data
        backups = response.json()['data']['backups']
        assert len(backups) == 2
        assert backups[0]['name'] == 'csm_backup_2026-03-16_11-45-00.zip'
        assert backups[1]['size'] == '48234496'
        assert backups[1]['location'].endswith('.zip')

    """" HA Management """

    @responses.activate
    def test_set_server_as_standby_success(self):
        """Test successful setting of server as standby"""
        active_server = "192.168.1.100"
        
        mock_response = {
            "status": "I",
            "message": "Server set as standby successfully",
            "data": {
                "standby_server": "192.168.1.101",
                "active_server": active_server,
                "ha_status": "configured",
                "sync_status": "in_progress"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/ha/setServerAsStandby/{active_server}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.set_server_as_standby(
            self.base_url,
            self.token,
            active_server
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['active_server'] == active_server
        assert response.json()['data']['ha_status'] == 'configured'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
    @responses.activate
    def test_set_standby_server_success(self):
        """Test successful setting of standby server"""
        standby_server = "192.168.1.101"
        standby_username = "admin"
        standby_password = "standby_pass123"
        
        mock_response = {
            "status": "I",
            "message": "Standby server configured successfully",
            "data": {
                "standby_server": standby_server,
                "active_server": "192.168.1.100",
                "ha_status": "configured",
                "sync_status": "initializing",
                "connection_established": True
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/ha/setStandbyServer/{standby_server}/{standby_username}/{standby_password}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.set_standby_server(
            self.base_url,
            self.token,
            standby_server,
            standby_username,
            standby_password
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['standby_server'] == standby_server
        assert response.json()['data']['ha_status'] == 'configured'
        assert response.json()['data']['connection_established'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_get_active_standby_status_success(self):
        """Test successful retrieval of active/standby server status"""
        mock_response = {
            "status": "success",
            "data": {
                "ha_configured": True,
                "active_server": {
                    "hostname": "csm-active-01",
                    "ip": "192.168.1.100",
                    "status": "active",
                    "last_heartbeat": "2026-03-16T16:15:00Z"
                },
                "standby_server": {
                    "hostname": "csm-standby-01",
                    "ip": "192.168.1.101",
                    "status": "standby",
                    "last_heartbeat": "2026-03-16T16:15:00Z"
                },
                "connection_status": "connected",
                "sync_status": "synchronized",
                "last_sync": "2026-03-16T16:14:30Z"
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/ha",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_active_standby_status(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify HA status data
        ha_data = response.json()['data']
        assert ha_data['ha_configured'] is True
        assert ha_data['active_server']['status'] == 'active'
        assert ha_data['standby_server']['status'] == 'standby'
        assert ha_data['connection_status'] == 'connected'
        assert ha_data['sync_status'] == 'synchronized'

    @responses.activate
    def test_remove_active_or_standby_server_success(self):
        """Test successful removal of active or standby server"""
        ha_server = "csm-standby-01"
        
        mock_response = {
            "status": "I",
            "message": "HA server removed successfully",
            "data": {
                "removed_server": ha_server,
                "ha_status": "disabled",
                "remaining_server": "csm-active-01"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/ha/removeHaServer/{ha_server}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.remove_active_or_standby_server(
            self.base_url,
            self.token,
            ha_server
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['removed_server'] == ha_server
        assert response.json()['data']['ha_status'] == 'disabled'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
    
    @responses.activate
    def test_reconnect_active_standby_server_success(self):
        """Test successful reconnection of active/standby server"""
        mock_response = {
            "status": "I",
            "message": "Active/standby connection reconnected successfully",
            "data": {
                "connection_status": "reconnected",
                "active_server": "csm-active-01",
                "standby_server": "csm-standby-01",
                "sync_initiated": True,
                "reconnect_time": "2026-03-16T19:10:00Z"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/ha/reconnect",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.reconnect_active_standby_server(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['connection_status'] == 'reconnected'
        assert response.json()['data']['sync_initiated'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_takeover_standby_server_success(self):
        """Test successful takeover by standby server"""
        mock_response = {
            "status": "I",
            "message": "Standby server takeover completed successfully",
            "data": {
                "new_active_server": "csm-standby-01",
                "previous_active_server": "csm-active-01",
                "new_role": "active",
                "previous_role": "standby"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/ha/takeover",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.takeover_standby_server(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['new_role'] == 'active'
        assert response.json()['data']['previous_role'] == 'standby'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
  
    """DUAL CONTROL"""

    @responses.activate
    def test_get_dual_control_state_success(self):
        """Test successful retrieval of dual control state"""
        mock_response = {
            "status": "success",
            "data": {
                "dual_control_enabled": True,
                "configured_by": "admin",
                "configured_at": "2026-03-15T10:00:00Z",
                "pending_requests": 3
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/dualcontrol",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_dual_control_state(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert response.json()['data']['dual_control_enabled'] is True
        assert response.json()['data']['pending_requests'] == 3
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_change_dual_control_state_success(self):
        """Test successful change of dual control state"""
        enable = True
        
        mock_response = {
            "status": "I",
            "message": "Dual control enabled successfully",
            "data": {
                "dual_control_enabled": enable,
                "changed_by": "admin",
                "changed_at": "2026-03-16T22:00:00Z",
                "previous_state": False
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/system/dualcontrol/{enable}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.change_dual_control_state(
            self.base_url,
            self.token,
            enable
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['dual_control_enabled'] is True
        assert response.json()['data']['previous_state'] is False
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_get_dual_control_requests_success(self):
        """Test successful retrieval of dual control requests"""
        mock_response = {
            "status": "success",
            "data": {
                "requests": [
                    {
                        "request_id": 1001,
                        "action": "delete_session",
                        "session_name": "PROD_SESSION_01",
                        "requested_by": "user1",
                        "requested_at": "2026-03-16T20:30:00Z",
                        "status": "pending"
                    },
                    {
                        "request_id": 1002,
                        "action": "modify_copyset",
                        "session_name": "TEST_SESSION_02",
                        "requested_by": "user2",
                        "requested_at": "2026-03-16T21:15:00Z",
                        "status": "pending"
                    },
                    {
                        "request_id": 1003,
                        "action": "remove_device",
                        "device_id": "DS8000:2107.ABC12",
                        "requested_by": "user3",
                        "requested_at": "2026-03-16T21:45:00Z",
                        "status": "pending"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/dualcontrol/requests",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_dual_control_requests(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        
        # Verify dual control requests data
        requests_data = response.json()['data']['requests']
        assert len(requests_data) == 3
        assert requests_data[0]['request_id'] == 1001
        assert requests_data[0]['status'] == 'pending'
        assert requests_data[1]['action'] == 'modify_copyset'
        assert requests_data[2]['action'] == 'remove_device'
    
    @responses.activate
    def test_approve_dual_control_request_success(self):
        """Test successful approval of dual control request"""
        request_id = 1001
        
        mock_response = {
            "status": "I",
            "message": "Dual control request approved successfully",
            "data": {
                "request_id": request_id,
                "action": "delete_session",
                "session_name": "PROD_SESSION_01",
                "requested_by": "user1",
                "approved_by": "admin",
                "approved_at": "2026-03-16T22:30:00Z",
                "status": "approved"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/system/dualcontrol/approve/{request_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.approve_dual_control_request(
            self.base_url,
            self.token,
            request_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['request_id'] == request_id
        assert response.json()['data']['status'] == 'approved'
        assert 'approved_by' in response.json()['data']
        assert 'approved_at' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_reject_dual_control_request_success(self):
        """Test successful rejection of dual control request"""
        request_id = 1002
        reject_comment = "Request does not meet security requirements"
        
        mock_response = {
            "status": "I",
            "message": "Dual control request rejected successfully",
            "data": {
                "request_id": request_id,
                "action": "modify_copyset",
                "session_name": "TEST_SESSION_02",
                "requested_by": "user2",
                "rejected_by": "admin",
                "rejected_at": "2026-03-16T22:45:00Z",
                "rejection_comment": reject_comment,
                "status": "rejected"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/system/dualcontrol/reject/{request_id}/{reject_comment}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.reject_dual_control_request(
            self.base_url,
            self.token,
            request_id,
            reject_comment
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['request_id'] == request_id
        assert response.json()['data']['status'] == 'rejected'
        assert response.json()['data']['rejection_comment'] == reject_comment
        assert 'rejected_by' in response.json()['data']
        assert 'rejected_at' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    """SYSTEM INFORMATION"""

    @responses.activate
    def test_get_session_types_success(self):
        """Test successful retrieval of session types"""
        mock_response = {
            "status": "success",
            "data": {
                "session_types": [
                    {
                        "type": "Metro Mirror",
                        "code": "MM",
                        "description": "Synchronous replication for local disaster recovery",
                        "supported": True
                    },
                    {
                        "type": "Global Mirror",
                        "code": "GM",
                        "description": "Asynchronous replication for remote disaster recovery",
                        "supported": True
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/sessiontypes",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_session_types(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify session types data
        session_types = response.json()['data']['session_types']
        assert len(session_types) == 2
        assert session_types[0]['type'] == 'Metro Mirror'
        assert session_types[0]['code'] == 'MM'
        assert session_types[1]['type'] == 'Global Mirror'
        assert all(st['supported'] for st in session_types)

    @responses.activate
    def test_get_server_version_success(self):
        """Test successful retrieval of server version"""
        mock_response = {
            "status": "success",
            "data": {
                "version": "8.5.2.1",
                "build": "20260315-1200",
                "release_date": "2026-03-15",
                "product_name": "IBM Copy Services Manager",
                "api_version": "2.0",
                "supported_protocols": ["REST", "CLI"],
                "platform": "Linux x86_64"
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/version",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_server_version(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify version data
        version_data = response.json()['data']
        assert version_data['version'] == '8.5.2.1'
        assert version_data['product_name'] == 'IBM Copy Services Manager'
        assert version_data['api_version'] == '2.0'
        assert 'REST' in version_data['supported_protocols']
        assert 'CLI' in version_data['supported_protocols']

    @responses.activate
    def test_get_volume_counts_success(self):
        """Test successful retrieval of volume counts"""
        mock_response = {
            "status": "success",
            "data": {
                "total_volumes": 15420,
                "volumes_by_type": {
                    "source": 7850,
                    "target": 7570
                },
                "volumes_by_session_type": {
                    "Metro Mirror": 4200,
                    "Global Mirror": 5800,
                    "Global Copy": 3100,
                    "FlashCopy": 2320
                },
                "last_updated": "2026-03-16T23:00:00Z"
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/volcounts",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_volume_counts(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify volume counts data
        volume_data = response.json()['data']
        assert volume_data['total_volumes'] == 15420
        assert volume_data['volumes_by_type']['source'] == 7850
        assert volume_data['volumes_by_type']['target'] == 7570
        assert volume_data['volumes_by_session_type']['Metro Mirror'] == 4200
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    """EMAIL NOTIFICATIONS"""

    @responses.activate
    def test_get_email_notifications_enabled_success(self):
        """Test successful retrieval of email notifications enabled status"""
        mock_response = {
            "status": "success",
            "data": {
                "email_notifications_enabled": True,
                "smtp_server": "smtp.example.com",
                "smtp_port": 587,
                "from_address": "csm-alerts@example.com",
                "last_modified": "2026-03-15T10:00:00Z",
                "modified_by": "admin"
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/notification/email/alert",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_email_notifications_enabled(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert response.json()['data']['email_notifications_enabled'] is True
        assert response.json()['data']['smtp_server'] == 'smtp.example.com'
        assert response.json()['data']['smtp_port'] == 587
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_put_email_notifications_enabled_success(self):
        """Test successful enabling of email notifications"""
        enabled = True
        
        mock_response = {
            "status": "I",
            "message": "Email notifications enabled successfully",
            "data": {
                "email_notifications_enabled": enabled,
                "smtp_server": "smtp.example.com",
                "smtp_port": 587,
                "from_address": "csm-alerts@example.com",
                "modified_at": "2026-03-26T05:50:00Z",
                "modified_by": "admin"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/system/notification/email/alert",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.put_email_notifications_enabled(
            self.base_url,
            self.token,
            enabled
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['email_notifications_enabled'] is True
        assert 'modified_at' in response.json()['data']
        assert 'modified_by' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_get_email_recipients_success(self):
        """Test successful retrieval of email recipients"""
        mock_response = {
            "status": "success",
            "data": {
                "recipients": [
                    {
                        "email": "admin@example.com",
                        "alert_types": ["all"],
                        "sessions": ["*"],
                        "added_at": "2026-03-10T08:00:00Z",
                        "added_by": "admin"
                    },
                    {
                        "email": "ops-team@example.com",
                        "alert_types": ["session", "session_rpo", "task_failed"],
                        "sessions": ["PROD_SESSION_01", "PROD_SESSION_02"],
                        "added_at": "2026-03-12T14:30:00Z",
                        "added_by": "admin"
                    },
                    {
                        "email": "storage-admin@example.com",
                        "alert_types": ["config", "comm", "pathing"],
                        "sessions": ["*"],
                        "added_at": "2026-03-15T09:15:00Z",
                        "added_by": "superadmin"
                    }
                ],
                "total_recipients": 3
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/system/notification/email/alert",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = system_service.get_email_recipients(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify recipients data
        recipients_data = response.json()['data']
        assert recipients_data['total_recipients'] == 3
        recipients = recipients_data['recipients']
        assert len(recipients) == 3
        assert recipients[0]['email'] == 'admin@example.com'
        assert recipients[0]['alert_types'] == ['all']
        assert recipients[0]['sessions'] == ['*']
        assert recipients[1]['email'] == 'ops-team@example.com'
        assert 'session' in recipients[1]['alert_types']
        assert 'PROD_SESSION_01' in recipients[1]['sessions']
        assert recipients[2]['email'] == 'storage-admin@example.com'
        assert 'config' in recipients[2]['alert_types']


if __name__ == '__main__':
    unittest.main()
