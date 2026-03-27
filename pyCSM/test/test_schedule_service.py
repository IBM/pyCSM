# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import unittest
import json
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus

import responses

from pyCSM.services.session_service import schedule_service


class TestScheduleService(unittest.TestCase):
    """Test cases for schedule service methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://testserver:8088/CSM/web"
        self.token = "test_token_12345"
        
        # Reset properties to default before each test
        schedule_service.properties = {
            "language": "en-US",
            "verify": False,
            "cert": None
        }

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()

    """SCHEDULED TASK MANAGEMENT"""

    @responses.activate
    def test_get_scheduled_tasks_success(self):
        """Test successful retrieval of all scheduled tasks"""
        mock_response = {
            "status": "I",
            "message": "Scheduled tasks retrieved successfully",
            "data": {
                "total_tasks": 3,
                "tasks": [
                    {
                        "task_id": "TASK_001",
                        "task_name": "Daily Backup",
                        "task_type": "backup",
                        "session_name": "PROD_SESSION_01",
                        "command": "Create Backup",
                        "schedule": {
                            "frequency": "daily",
                            "time": "02:00:00",
                            "timezone": "UTC"
                        },
                        "enabled": True,
                        "last_run": "2026-03-17T02:00:00Z",
                        "last_run_status": "success",
                        "next_run": "2026-03-18T02:00:00Z",
                        "created_by": "admin",
                        "created_at": "2026-03-01T10:00:00Z"
                    },
                    {
                        "task_id": "TASK_002",
                        "task_name": "Weekly Sync Check",
                        "task_type": "sync",
                        "session_name": "PROD_SESSION_01",
                        "command": "Verify Sync",
                        "schedule": {
                            "frequency": "weekly",
                            "day_of_week": "Sunday",
                            "time": "03:00:00",
                            "timezone": "UTC"
                        },
                        "enabled": True,
                        "last_run": "2026-03-16T03:00:00Z",
                        "last_run_status": "success",
                        "next_run": "2026-03-23T03:00:00Z",
                        "created_by": "admin",
                        "created_at": "2026-03-01T10:30:00Z"
                    },
                    {
                        "task_id": "TASK_003",
                        "task_name": "Monthly Report",
                        "task_type": "report",
                        "session_name": "PROD_SESSION_01",
                        "command": "Generate Report",
                        "schedule": {
                            "frequency": "monthly",
                            "day_of_month": 1,
                            "time": "00:00:00",
                            "timezone": "UTC"
                        },
                        "enabled": False,
                        "last_run": "2026-03-01T00:00:00Z",
                        "last_run_status": "success",
                        "next_run": "2026-04-01T00:00:00Z",
                        "created_by": "admin",
                        "created_at": "2026-02-15T14:00:00Z"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/scheduledtasks",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.get_scheduled_tasks(
            self.base_url,
            self.token
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['total_tasks'] == 3
        assert len(response.json()['data']['tasks']) == 3
        
        # Verify first task details
        task1 = response.json()['data']['tasks'][0]
        assert task1['task_id'] == 'TASK_001'
        assert task1['task_name'] == 'Daily Backup'
        assert task1['task_type'] == 'backup'
        assert task1['session_name'] == 'PROD_SESSION_01'
        assert task1['enabled'] is True
        assert task1['schedule']['frequency'] == 'daily'
        assert task1['last_run_status'] == 'success'
        
        # Verify second task details
        task2 = response.json()['data']['tasks'][1]
        assert task2['task_id'] == 'TASK_002'
        assert task2['schedule']['frequency'] == 'weekly'
        assert task2['schedule']['day_of_week'] == 'Sunday'
        
        # Verify third task (disabled)
        task3 = response.json()['data']['tasks'][2]
        assert task3['task_id'] == 'TASK_003'
        assert task3['enabled'] is False
        assert task3['schedule']['frequency'] == 'monthly'
        
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"


    @responses.activate
    def test_create_scheduled_task_success(self):
        """Test successful creation of a scheduled task"""
        task_json = {
            "task_name": "Hourly Sync",
            "task_type": "sync",
            "session_name": "TEST_SESSION_01",
            "command": "Start Session",
            "schedule": {
                "frequency": "hourly",
                "minute": 0,
                "timezone": "UTC"
            },
            "enabled": True,
            "notification_email": "admin@example.com"
        }
        
        task_json_str = json.dumps(task_json)
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task created successfully",
            "data": {
                "task_id": "TASK_004",
                "task_name": "Hourly Sync",
                "task_type": "sync",
                "session_name": "TEST_SESSION_01",
                "command": "Start Session",
                "schedule": {
                    "frequency": "hourly",
                    "minute": 0,
                    "timezone": "UTC"
                },
                "enabled": True,
                "notification_email": "admin@example.com",
                "created_by": "admin",
                "created_at": "2026-03-17T17:00:00Z",
                "next_run": "2026-03-17T18:00:00Z"
            }
        }
        
        responses.add(
            responses.PUT,
            f"{self.base_url}/sessions/scheduledtasks",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.create_scheduled_task(
            self.base_url,
            self.token,
            task_json_str
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == 'TASK_004'
        assert response.json()['data']['task_name'] == 'Hourly Sync'
        assert response.json()['data']['task_type'] == 'sync'
        assert response.json()['data']['session_name'] == 'TEST_SESSION_01'
        assert response.json()['data']['command'] == 'Start Session'
        assert response.json()['data']['enabled'] is True
        assert response.json()['data']['schedule']['frequency'] == 'hourly'
        assert response.json()['data']['schedule']['minute'] == 0
        assert response.json()['data']['notification_email'] == 'admin@example.com'
        assert 'next_run' in response.json()['data']
        assert 'created_at' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_enable_scheduled_task_success(self):
        """Test successful enabling of a scheduled task"""
        task_id = "TASK_003"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task enabled successfully",
            "data": {
                "task_id": task_id,
                "task_name": "Monthly Report",
                "enabled": True,
                "next_run": "2026-04-01T00:00:00Z"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/enable/{task_id}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = schedule_service.enable_scheduled_task(
            self.base_url,
            self.token,
            task_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['enabled'] is True
        assert len(responses.calls) == 1

    @responses.activate
    def test_disable_scheduled_task_success(self):
        """Test successful disabling of a scheduled task"""
        task_id = "TASK_001"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task disabled successfully",
            "data": {
                "task_id": task_id,
                "task_name": "Daily Backup",
                "enabled": False
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/disable/{task_id}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = schedule_service.disable_scheduled_task(
            self.base_url,
            self.token,
            task_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['enabled'] is False
        assert len(responses.calls) == 1

    @responses.activate
    def test_run_scheduled_task_success(self):
        """Test successful synchronous execution of a scheduled task"""
        task_id = "TASK_002"
        synchronous = True
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task completed successfully",
            "data": {
                "task_id": task_id,
                "execution_mode": "synchronous",
                "status": "completed"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/{task_id}/{synchronous}",
            json=mock_response,
            status=HTTPStatus.OK.value
        )
        
        response = schedule_service.run_scheduled_task(
            self.base_url,
            self.token,
            task_id,
            synchronous
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['execution_mode'] == 'synchronous'
        assert response.json()['data']['status'] == 'completed'
        assert len(responses.calls) == 1



    @responses.activate
    def test_delete_task_success(self):
        """Test successful deletion of a scheduled task"""
        task_id = "TASK_003"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task deleted successfully",
            "data": {
                "task_id": task_id,
                "task_name": "Monthly Report",
                "deleted": True
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/delete/{task_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.delete_task(
            self.base_url,
            self.token,
            task_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == task_id
        assert response.json()['data']['deleted'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_cancel_task_success(self):
        """Test successful cancellation of a running scheduled task"""
        task_id = "TASK_001"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task cancelled successfully",
            "data": {
                "task_id": task_id,
                "task_name": "Daily Backup",
                "status": "cancelled",
                "was_running": True,
                "cancelled_at": "2026-03-26T05:45:00Z"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/cancel/{task_id}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.cancel_task(
            self.base_url,
            self.token,
            task_id
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == task_id
        assert response.json()['data']['status'] == 'cancelled'
        assert response.json()['data']['was_running'] is True
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_run_task_now_success(self):
        """Test successful execution of a scheduled task at a specific step"""
        task_id = "TASK_002"
        synchronous = True
        step = 2
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task started successfully at step 2",
            "data": {
                "task_id": task_id,
                "task_name": "Weekly Sync Check",
                "execution_mode": "synchronous",
                "starting_step": step,
                "status": "running",
                "started_at": "2026-03-26T05:45:00Z"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/scheduledtasks/{task_id}/{str(synchronous).lower()}/step/{step}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.run_task_now(
            self.base_url,
            self.token,
            task_id,
            synchronous,
            step
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == task_id
        assert response.json()['data']['execution_mode'] == 'synchronous'
        assert response.json()['data']['starting_step'] == step
        assert response.json()['data']['status'] == 'running'
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/json"


if __name__ == '__main__':
    unittest.main()

# Made with Bob

    @responses.activate
    def test_enable_scheduled_task_at_time_success(self):
        """Test successful enabling of a scheduled task at a specific time"""
        task_id = "TASK_003"
        start_time = "2026-03-19T08-00"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task will be enabled at specified time",
            "data": {
                "task_id": task_id,
                "task_name": "Monthly Report",
                "enabled": False,
                "scheduled_enable_time": "2026-03-19T08:00:00Z",
                "current_status": "pending_enable",
                "will_enable_at": "2026-03-19T08:00:00Z"
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/enable/{task_id}/{start_time}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.enable_scheduled_task_at_time(
            self.base_url,
            self.token,
            task_id,
            start_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == task_id
        assert response.json()['data']['current_status'] == 'pending_enable'
        assert 'scheduled_enable_time' in response.json()['data']
        assert 'will_enable_at' in response.json()['data']
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_run_scheduled_task_at_time_success(self):
        """Test successful scheduling of a task to run at a specific time"""
        task_id = "TASK_001"
        start_time = "2026-03-19T03-30"
        
        mock_response = {
            "status": "I",
            "message": "Scheduled task will run at specified time",
            "data": {
                "task_id": task_id,
                "task_name": "Daily Backup",
                "scheduled_run_time": "2026-03-19T03:30:00Z",
                "current_status": "scheduled",
                "execution_mode": "one_time",
                "will_run_at": "2026-03-19T03:30:00Z",
                "estimated_duration_minutes": 15
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/scheduledtasks/{task_id}/runat/{start_time}",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = schedule_service.run_scheduled_task_at_time(
            self.base_url,
            self.token,
            task_id,
            start_time
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['task_id'] == task_id
        assert response.json()['data']['current_status'] == 'scheduled'
        assert response.json()['data']['execution_mode'] == 'one_time'
        assert 'scheduled_run_time' in response.json()['data']
        assert 'will_run_at' in response.json()['data']
        assert response.json()['data']['estimated_duration_minutes'] == 15
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"
