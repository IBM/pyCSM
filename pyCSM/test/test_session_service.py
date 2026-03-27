# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import unittest
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus

import responses

from pyCSM.services.session_service import session_service


class TestSessionService(unittest.TestCase):
    """Test cases for session service methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://testserver:8088/CSM/web"
        self.token = "test_token_12345"
        
        # Reset properties to default before each test
        session_service.properties = {
            "language": "en-US",
            "verify": False,
            "cert": None
        }

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()

    """SESSION MANAGEMENT"""

    @responses.activate
    def test_create_session_success(self):
        """Test successful creation of a session"""
        session_name = "TEST_SESSION_01"
        session_type = "Metro Mirror"
        description = "Test session for Metro Mirror replication"
        
        mock_response = {
            "status": "I",
            "message": "Session created successfully",
            "data": {
                "session_name": session_name,
                "session_type": session_type,
                "description": description,
                "state": "Inactive",
                "created_at": "2026-03-17T15:00:00Z",
                "created_by": "admin",
                "copyset_count": 0
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.create_session(
            self.base_url,
            self.token,
            session_name,
            session_type,
            description
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['session_type'] == session_type
        assert response.json()['data']['description'] == description
        assert response.json()['data']['state'] == 'Inactive'
        assert response.json()['data']['copyset_count'] == 0
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_create_session_without_description_success(self):
        """Test successful creation of a session without description"""
        session_name = "TEST_SESSION_02"
        session_type = "Global Mirror"
        
        mock_response = {
            "status": "I",
            "message": "Session created successfully",
            "data": {
                "session_name": session_name,
                "session_type": session_type,
                "description": None,
                "state": "Inactive",
                "created_at": "2026-03-17T15:05:00Z",
                "created_by": "admin",
                "copyset_count": 0
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.create_session(
            self.base_url,
            self.token,
            session_name,
            session_type
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['session_type'] == session_type
        assert response.json()['data']['description'] is None
        assert len(responses.calls) == 1

    @responses.activate
    def test_delete_session_success(self):
        """Test successful deletion of a session"""
        session_name = "TEST_SESSION_01"
        
        mock_response = {
            "status": "I",
            "message": "Session deleted successfully",
            "data": {
                "session_name": session_name,
                "deleted_at": "2026-03-17T15:10:00Z",
                "deleted_by": "admin",
                "previous_state": "Inactive"
            }
        }
        
        responses.add(
            responses.DELETE,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.delete_session(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['previous_state'] == 'Inactive'
        assert 'deleted_at' in response.json()['data']
        assert 'deleted_by' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_get_session_info_success(self):
        """Test successful retrieval of session information"""
        session_name = "PROD_SESSION_01"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "session_type": "Metro Mirror",
                "description": "Production Metro Mirror session",
                "state": "Active",
                "created_at": "2026-03-15T10:00:00Z",
                "created_by": "admin",
                "last_modified": "2026-03-17T14:30:00Z",
                "copyset_count": 25,
                "copysets": [
                    {
                        "copyset_name": "COPYSET_001",
                        "source_volume": "VOL001",
                        "target_volume": "VOL002",
                        "state": "Synchronized"
                    },
                    {
                        "copyset_name": "COPYSET_002",
                        "source_volume": "VOL003",
                        "target_volume": "VOL004",
                        "state": "Synchronized"
                    }
                ],
                "session_options": {
                    "auto_start": True,
                    "consistency_group": True,
                    "rpo_threshold": 300
                },
                "statistics": {
                    "total_data_transferred_gb": 1250.5,
                    "average_rpo_seconds": 45,
                    "last_sync_time": "2026-03-17T15:15:00Z"
                }
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_session_info(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify session info data
        session_data = response.json()['data']
        assert session_data['session_name'] == session_name
        assert session_data['session_type'] == 'Metro Mirror'
        assert session_data['state'] == 'Active'
        assert session_data['copyset_count'] == 25
        assert len(session_data['copysets']) == 2
        assert session_data['copysets'][0]['state'] == 'Synchronized'
        assert session_data['session_options']['auto_start'] is True
        assert session_data['statistics']['average_rpo_seconds'] == 45

    @responses.activate
    def test_create_session_by_volgroup_name_success(self):
        """Test successful creation of a session by volume group name"""
        volgroup_name = "PROD_VOLGROUP_01"
        session_type = "SVC"  # Spec V Snapshot short name
        description = "Session created from volume group"
        
        mock_response = {
            "status": "I",
            "message": "Session created successfully from volume group",
            "data": {
                "session_name": "SESSION_PROD_VOLGROUP_01_20260317",
                "volgroup_name": volgroup_name,
                "session_type": session_type,
                "description": description,
                "state": "Inactive",
                "created_at": "2026-03-17T15:20:00Z",
                "created_by": "admin",
                "auto_populated": True,
                "copyset_count": 15,
                "copysets": [
                    {
                        "copyset_name": "COPYSET_001",
                        "source_volume": "VOL_001",
                        "target_volume": "VOL_001_SNAP",
                        "state": "Ready"
                    },
                    {
                        "copyset_name": "COPYSET_002",
                        "source_volume": "VOL_002",
                        "target_volume": "VOL_002_SNAP",
                        "state": "Ready"
                    }
                ],
                "volume_group_info": {
                    "total_volumes": 15,
                    "total_capacity_gb": 500.0,
                    "storage_system": "SVC_CLUSTER_01"
                }
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/byvolgroup",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.create_session_by_volgroup_name(
            self.base_url,
            self.token,
            volgroup_name,
            session_type,
            description
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['volgroup_name'] == volgroup_name
        assert response.json()['data']['session_type'] == session_type
        assert response.json()['data']['description'] == description
        assert response.json()['data']['auto_populated'] is True
        assert response.json()['data']['copyset_count'] == 15
        assert len(response.json()['data']['copysets']) == 2
        assert response.json()['data']['volume_group_info']['total_volumes'] == 15
        assert 'session_name' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_create_session_by_volgroup_name_without_description_success(self):
        """Test successful creation of a session by volume group name without description"""
        volgroup_name = "TEST_VOLGROUP_02"
        session_type = "SVC"
        
        mock_response = {
            "status": "I",
            "message": "Session created successfully from volume group",
            "data": {
                "session_name": "SESSION_TEST_VOLGROUP_02_20260317",
                "volgroup_name": volgroup_name,
                "session_type": session_type,
                "description": None,
                "state": "Inactive",
                "created_at": "2026-03-17T15:25:00Z",
                "created_by": "admin",
                "auto_populated": True,
                "copyset_count": 8,
                "volume_group_info": {
                    "total_volumes": 8,
                    "total_capacity_gb": 200.0,
                    "storage_system": "SVC_CLUSTER_02"
                }
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/byvolgroup",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.create_session_by_volgroup_name(
            self.base_url,
            self.token,
            volgroup_name,
            session_type
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['volgroup_name'] == volgroup_name
        assert response.json()['data']['description'] is None
        assert response.json()['data']['auto_populated'] is True
        assert response.json()['data']['copyset_count'] == 8

    """SESSION COMMANDS & OPERATIONS"""

    @responses.activate
    def test_get_available_commands_success(self):
        """Test successful retrieval of available commands for a session"""
        session_name = "PROD_SESSION_01"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "session_state": "Inactive",
                "available_commands": [
                    {
                        "command_name": "start",
                        "display_name": "Start Session",
                        "description": "Start the replication session",
                        "requires_confirmation": False,
                        "estimated_duration_seconds": 30
                    },
                    {
                        "command_name": "establish",
                        "display_name": "Establish Session",
                        "description": "Establish the session relationships",
                        "requires_confirmation": True,
                        "estimated_duration_seconds": 120
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/availablecommands",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_available_commands(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify available commands data
        commands_data = response.json()['data']
        assert commands_data['session_name'] == session_name
        assert commands_data['session_state'] == 'Inactive'
        assert len(commands_data['available_commands']) == 2
        assert commands_data['available_commands'][0]['command_name'] == 'start'
        assert commands_data['available_commands'][0]['requires_confirmation'] is False
        assert commands_data['available_commands'][1]['command_name'] == 'establish'
        assert commands_data['available_commands'][1]['requires_confirmation'] is True

    @responses.activate
    def test_get_session_options_success(self):
        """Test successful retrieval of session options"""
        session_name = "PROD_SESSION_01"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "session_type": "Metro Mirror",
                "options": {
                    "auto_start": {
                        "value": True,
                        "type": "boolean",
                        "description": "Automatically start session after creation",
                        "modifiable": True
                    },
                    "consistency_group": {
                        "value": True,
                        "type": "boolean",
                        "description": "Enable consistency group for multi-volume sessions",
                        "modifiable": False
                    },
                    "rpo_threshold": {
                        "value": 300,
                        "type": "integer",
                        "unit": "seconds",
                        "description": "Recovery Point Objective threshold",
                        "min_value": 60,
                        "max_value": 3600,
                        "modifiable": True
                    },
                    "sync_mode": {
                        "value": "synchronous",
                        "type": "string",
                        "description": "Synchronization mode",
                        "allowed_values": ["synchronous", "asynchronous"],
                        "modifiable": False
                    },
                    "compression_enabled": {
                        "value": False,
                        "type": "boolean",
                        "description": "Enable data compression",
                        "modifiable": True
                    },
                    "encryption_enabled": {
                        "value": True,
                        "type": "boolean",
                        "description": "Enable data encryption in transit",
                        "modifiable": False
                    }
                },
                "last_modified": "2026-03-17T14:00:00Z"
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/options",
            json=mock_response,
            status=HTTPStatus.OK.value,
        )
        
        response = session_service.get_session_options(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/json"
        
        # Verify session options data
        options_data = response.json()['data']
        assert options_data['session_name'] == session_name
        assert options_data['session_type'] == 'Metro Mirror'
        assert len(options_data['options']) == 6
        assert options_data['options']['auto_start']['value'] is True
        assert options_data['options']['auto_start']['modifiable'] is True
        assert options_data['options']['rpo_threshold']['value'] == 300
        assert options_data['options']['rpo_threshold']['unit'] == 'seconds'
        assert options_data['options']['sync_mode']['value'] == 'synchronous'
        assert 'asynchronous' in options_data['options']['sync_mode']['allowed_values']
        assert options_data['options']['encryption_enabled']['value'] is True

    @responses.activate
    def test_run_session_command_success(self):
        """Test successful execution of a session command"""
        session_name = "PROD_SESSION_01"
        command_name = "start"
        
        mock_response = {
            "status": "I",
            "message": "Command executed successfully",
            "data": {
                "session_name": session_name,
                "command_name": command_name,
                "command_display_name": "Start Session",
                "execution_status": "completed",
                "started_at": "2026-03-17T15:30:00Z",
                "completed_at": "2026-03-17T15:30:25Z",
                "duration_seconds": 25,
                "previous_state": "Inactive",
                "new_state": "Active",
                "affected_copysets": 25,
                "result_details": {
                    "copysets_started": 25,
                    "copysets_failed": 0,
                    "synchronization_initiated": True,
                    "estimated_sync_time_minutes": 15
                }
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.run_session_command(
            self.base_url,
            self.token,
            session_name,
            command_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['command_name'] == command_name
        assert response.json()['data']['execution_status'] == 'completed'
        assert response.json()['data']['previous_state'] == 'Inactive'
        assert response.json()['data']['new_state'] == 'Active'
        assert response.json()['data']['affected_copysets'] == 25
        assert response.json()['data']['result_details']['copysets_started'] == 25
        assert response.json()['data']['result_details']['copysets_failed'] == 0
        assert response.json()['data']['result_details']['synchronization_initiated'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_run_session_command_stop_success(self):
        """Test successful execution of stop command on active session"""
        session_name = "PROD_SESSION_01"
        command_name = "stop"
        
        mock_response = {
            "status": "I",
            "message": "Session stopped successfully",
            "data": {
                "session_name": session_name,
                "command_name": command_name,
                "command_display_name": "Stop Session",
                "execution_status": "completed",
                "started_at": "2026-03-17T15:35:00Z",
                "completed_at": "2026-03-17T15:35:10Z",
                "duration_seconds": 10,
                "previous_state": "Active",
                "new_state": "Inactive",
                "affected_copysets": 25,
                "result_details": {
                    "copysets_stopped": 25,
                    "copysets_failed": 0,
                    "data_synchronized": True
                }
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/{session_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.run_session_command(
            self.base_url,
            self.token,
            session_name,
            command_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['command_name'] == command_name
        assert response.json()['data']['previous_state'] == 'Active'
        assert response.json()['data']['new_state'] == 'Inactive'
        assert response.json()['data']['result_details']['data_synchronized'] is True
        assert len(responses.calls) == 1

    """BACKUP MANAGEMENT"""

    @responses.activate
    def test_get_backup_details_success(self):
        """Test successful retrieval of backup details"""
        session_name = "PROD_SESSION_01"
        role = "target"
        backup_id = "BACKUP_20260317_001"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "role": role,
                "backup_id": backup_id,
                "backup_name": "PROD_BACKUP_20260317_150000",
                "backup_type": "Full",
                "state": "Available",
                "created_at": "2026-03-17T15:00:00Z",
                "size_gb": 125.5,
                "copysets": [
                    {
                        "copyset_name": "COPYSET_001",
                        "source_volume": "VOL001",
                        "backup_volume": "VOL002_BACKUP_001",
                        "size_gb": 50.2
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/backups/{role}/{backup_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_backup_details(
            self.base_url,
            self.token,
            session_name,
            role,
            backup_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['data']['backup_id'] == backup_id
        assert response.json()['data']['role'] == role
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token

    @responses.activate
    def test_run_backup_command_success(self):
        """Test successful execution of backup command"""
        session_name = "PROD_SESSION_01"
        role = "target"
        backup_id = "BACKUP_20260317_001"
        command = "Recover Backup"
        
        mock_response = {
            "status": "I",
            "message": "Backup recovery initiated successfully",
            "data": {
                "session_name": session_name,
                "backup_id": backup_id,
                "command": command,
                "execution_status": "in_progress"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/{session_name}/backups/{role}/{backup_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.run_backup_command(
            self.base_url,
            self.token,
            session_name,
            role,
            backup_id,
            command
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['command'] == command
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token

    @responses.activate
    def test_get_recovered_backup_details_success(self):
        """Test successful retrieval of recovered backup details"""
        session_name = "PROD_SESSION_01"
        backup_id = "BACKUP_20260317_001"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "backup_id": backup_id,
                "recovery_status": "completed",
                "pairs": [
                    {
                        "copyset_name": "COPYSET_001",
                        "recovery_status": "completed"
                    }
                ],
                "total_pairs": 25,
                "successful_pairs": 25
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/recoveredbackups/{backup_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_recovered_backup_details(
            self.base_url,
            self.token,
            session_name,
            backup_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['data']['backup_id'] == backup_id
        assert response.json()['data']['recovery_status'] == 'completed'
        assert response.json()['data']['total_pairs'] == 25
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token


    """SNAPSHOT MANAGEMENT"""

    @responses.activate
    def test_get_snapshot_clones_success(self):
        """Test successful retrieval of snapshot clones"""
        session_name = "SGC_SESSION_01"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "session_type": "Spec V Safeguarded Copy",
                "total_clones": 3,
                "clones": [
                    {
                        "clone_id": "CLONE_001",
                        "snapshot_name": "SNAPSHOT_20260317_001",
                        "clone_name": "CLONE_SNAPSHOT_001",
                        "state": "Active",
                        "created_at": "2026-03-17T14:00:00Z",
                        "source_volume": "VOL001",
                        "clone_volume": "VOL001_CLONE",
                        "size_gb": 100.0,
                        "thin_provisioned": True,
                        "space_used_gb": 15.5
                    },
                    {
                        "clone_id": "CLONE_002",
                        "snapshot_name": "SNAPSHOT_20260317_002",
                        "clone_name": "CLONE_SNAPSHOT_002",
                        "state": "Active",
                        "created_at": "2026-03-17T14:30:00Z",
                        "source_volume": "VOL002",
                        "clone_volume": "VOL002_CLONE",
                        "size_gb": 150.0,
                        "thin_provisioned": True,
                        "space_used_gb": 22.3
                    },
                    {
                        "clone_id": "CLONE_003",
                        "snapshot_name": "SNAPSHOT_20260317_003",
                        "clone_name": "CLONE_SNAPSHOT_003",
                        "state": "Suspended",
                        "created_at": "2026-03-17T15:00:00Z",
                        "source_volume": "VOL003",
                        "clone_volume": "VOL003_CLONE",
                        "size_gb": 200.0,
                        "thin_provisioned": True,
                        "space_used_gb": 45.8
                    }
                ],
                "total_space_used_gb": 83.6,
                "total_capacity_gb": 450.0
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/clones",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_snapshot_clones(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify snapshot clones data
        clones_data = response.json()['data']
        assert clones_data['session_name'] == session_name
        assert clones_data['session_type'] == 'Spec V Safeguarded Copy'
        assert clones_data['total_clones'] == 3
        assert len(clones_data['clones']) == 3
        assert clones_data['clones'][0]['clone_id'] == 'CLONE_001'
        assert clones_data['clones'][0]['state'] == 'Active'
        assert clones_data['clones'][0]['thin_provisioned'] is True
        assert clones_data['clones'][1]['space_used_gb'] == 22.3
        assert clones_data['clones'][2]['state'] == 'Suspended'
        assert clones_data['total_space_used_gb'] == 83.6
        assert clones_data['total_capacity_gb'] == 450.0

    @responses.activate
    def test_get_snapshot_clone_details_by_name_success(self):
        """Test successful retrieval of snapshot clone details by name"""
        session_name = "SGC_SESSION_01"
        snapshot_name = "SNAPSHOT_20260317_001"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "snapshot_name": snapshot_name,
                "clone_details": {
                    "clone_id": "CLONE_001",
                    "clone_name": "CLONE_SNAPSHOT_001",
                    "state": "Active",
                    "created_at": "2026-03-17T14:00:00Z",
                    "created_by": "admin",
                    "last_modified": "2026-03-17T14:05:00Z",
                    "thin_provisioned": True,
                    "space_efficiency_ratio": 6.45
                },
                "pairs": [
                    {
                        "pair_id": "PAIR_001",
                        "source_volume": "VOL001",
                        "snapshot_volume": "VOL001_SNAP",
                        "clone_volume": "VOL001_CLONE",
                        "size_gb": 100.0,
                        "space_used_gb": 15.5,
                        "state": "Synchronized",
                        "io_operations": {
                            "read_ops": 12500,
                            "write_ops": 3200,
                            "total_ops": 15700
                        }
                    },
                    {
                        "pair_id": "PAIR_002",
                        "source_volume": "VOL002",
                        "snapshot_volume": "VOL002_SNAP",
                        "clone_volume": "VOL002_CLONE",
                        "size_gb": 150.0,
                        "space_used_gb": 22.3,
                        "state": "Synchronized",
                        "io_operations": {
                            "read_ops": 18700,
                            "write_ops": 4500,
                            "total_ops": 23200
                        }
                    }
                ],
                "total_pairs": 2,
                "total_size_gb": 250.0,
                "total_space_used_gb": 37.8,
                "performance_metrics": {
                    "average_read_latency_ms": 2.5,
                    "average_write_latency_ms": 3.8,
                    "throughput_mbps": 125.5
                }
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/clonesBySnapshotName/{snapshot_name}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = session_service.get_snapshot_clone_details_by_name(
            self.base_url,
            self.token,
            session_name,
            snapshot_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == mock_response
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
        
        # Verify snapshot clone details data
        clone_data = response.json()['data']
        assert clone_data['session_name'] == session_name
        assert clone_data['snapshot_name'] == snapshot_name
        assert clone_data['clone_details']['clone_id'] == 'CLONE_001'
        assert clone_data['clone_details']['state'] == 'Active'
        assert clone_data['clone_details']['thin_provisioned'] is True
        assert clone_data['clone_details']['space_efficiency_ratio'] == 6.45
        assert len(clone_data['pairs']) == 2
        assert clone_data['total_pairs'] == 2
        assert clone_data['pairs'][0]['state'] == 'Synchronized'
        assert clone_data['pairs'][0]['io_operations']['total_ops'] == 15700
        assert clone_data['pairs'][1]['space_used_gb'] == 22.3
        assert clone_data['total_size_gb'] == 250.0
        assert clone_data['total_space_used_gb'] == 37.8
        assert clone_data['performance_metrics']['throughput_mbps'] == 125.5
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token

    """HISTORY & MONITORING"""

    @responses.activate
    def test_get_rpo_history_success(self):
        """Test successful retrieval of RPO history"""
        session_name = "PROD_SESSION_01"
        rolepair = "source-target"
        start_time = "2026-03-10"
        end_time = "2026-03-17"
        
        mock_response = {
            "status": "I",
            "message": "RPO history retrieved successfully",
            "data": {
                "session_name": session_name,
                "rolepair": rolepair,
                "total_records": 168,
                "average_rpo_seconds": 45.2
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}/getrpohistory/{rolepair}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = session_service.get_rpo_history(
            self.base_url,
            self.token,
            session_name,
            rolepair,
            start_time,
            end_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['total_records'] == 168
        assert len(responses.calls) == 1

    @responses.activate
    def test_export_lss_oos_history_success(self):
        """Test successful export of LSS OOS history"""
        session_name = "PROD_SESSION_01"
        rolepair = "source-target"
        start_time = "2026-03-10"
        end_time = "2026-03-17"
        
        mock_response = {
            "status": "I",
            "message": "LSS OOS history exported successfully",
            "data": {
                "session_name": session_name,
                "file_name": "lss_oos_history.csv",
                "total_records": 1250
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}/exportlssooshistory/{rolepair}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = session_service.export_lss_oos_history(
            self.base_url,
            self.token,
            session_name,
            rolepair,
            start_time,
            end_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['file_name'].endswith('.csv')
        assert len(responses.calls) == 1

    @responses.activate
    def test_export_device_writeio_history_success(self):
        """Test successful export of device write I/O history"""
        session_name = "PROD_SESSION_01"
        start_time = "2026-03-10"
        end_time = "2026-03-17"
        
        mock_response = {
            "status": "I",
            "message": "Device write I/O history exported successfully",
            "data": {
                "session_name": session_name,
                "file_name": "device_writeio_history.csv",
                "total_records": 2520
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/{session_name}/exporteseboxhistory",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = session_service.export_device_writeio_history(
            self.base_url,
            self.token,
            session_name,
            start_time,
            end_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['file_name'].endswith('.csv')
        assert len(responses.calls) == 1

    """ROLE PAIR MANAGEMENT"""

    @responses.activate
    def test_get_rolepair_info_success(self):
        """Test successful retrieval of role pair information"""
        session_name = "PROD_SESSION_01"
        rolepair = "source-target"
        
        mock_response = {
            "status": "success",
            "data": {
                "session_name": session_name,
                "rolepair": rolepair,
                "state": "Active",
                "total_copysets": 25
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/sequences/{rolepair}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = session_service.get_rolepair_info(
            self.base_url,
            self.token,
            session_name,
            rolepair
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['data']['rolepair'] == rolepair
        assert response.json()['data']['total_copysets'] == 25
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_pair_info_success(self):
        """Test successful retrieval of pair information"""
        session_name = "PROD_SESSION_01"
        rolepair = "source-target"
        
        mock_response = {
            "status": "I",
            "data": {
                "session_name": session_name,
                "rolepair": rolepair,
                "total_pairs": 25,
                "pairs": [
                    {
                        "pair_id": "PAIR_001",
                        "state": "Synchronized"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/pairs/{rolepair}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        from pyCSM.services.session_service import copyset_service
        
        response = copyset_service.get_pair_info(
            self.base_url,
            self.token,
            session_name,
            rolepair
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['total_pairs'] == 25
        assert len(responses.calls) == 1


if __name__ == '__main__':
    unittest.main()