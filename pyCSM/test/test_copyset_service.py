# Copyright (C) 2022 IBM CORPORATION
# Apache License, Version 2.0 (see https://opensource.org/licenses/Apache-2.0)

import unittest
from unittest.mock import Mock, patch, MagicMock
from http import HTTPStatus

import responses

from pyCSM.services.session_service import copyset_service


class TestCopysetService(unittest.TestCase):
    """Test cases for copyset service methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.base_url = "https://testserver:8088/CSM/web"
        self.token = "test_token_12345"
        
        # Reset properties to default before each test
        copyset_service.properties = {
            "language": "en-US",
            "verify": False,
            "cert": None
        }

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()

    """COPYSET MANAGEMENT"""

    @responses.activate
    def test_get_copysets_success(self):
        """Test successful retrieval of copysets"""
        session_name = "PROD_SESSION_01"
        
        mock_response = {
            "status": "I",
            "message": "Copysets retrieved successfully",
            "data": {
                "session_name": session_name,
                "total_copysets": 3,
                "copysets": [
                    {
                        "copyset_id": "COPYSET_001",
                        "copyset_name": "COPYSET_001",
                        "state": "Synchronized",
                        "source_volume": "DS8000:2107.ABC12:VOL:0001",
                        "target_volume": "DS8000:2107.DEF34:VOL:0001",
                        "size_gb": 100.0,
                        "sync_percentage": 100.0,
                        "consistency_group": "CG01"
                    },
                    {
                        "copyset_id": "COPYSET_002",
                        "copyset_name": "COPYSET_002",
                        "state": "Synchronized",
                        "source_volume": "DS8000:2107.ABC12:VOL:0002",
                        "target_volume": "DS8000:2107.DEF34:VOL:0002",
                        "size_gb": 150.0,
                        "sync_percentage": 100.0,
                        "consistency_group": "CG01"
                    },
                    {
                        "copyset_id": "COPYSET_003",
                        "copyset_name": "COPYSET_003",
                        "state": "Copying",
                        "source_volume": "DS8000:2107.ABC12:VOL:0003",
                        "target_volume": "DS8000:2107.DEF34:VOL:0003",
                        "size_gb": 200.0,
                        "sync_percentage": 75.5,
                        "consistency_group": "CG02"
                    }
                ]
            }
        }
        
        responses.add(
            responses.GET,
            f"{self.base_url}/sessions/{session_name}/copysets",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = copyset_service.get_copysets(
            self.base_url,
            self.token,
            session_name
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['total_copysets'] == 3
        assert len(response.json()['data']['copysets']) == 3
        assert response.json()['data']['copysets'][0]['copyset_id'] == 'COPYSET_001'
        assert response.json()['data']['copysets'][0]['state'] == 'Synchronized'
        assert response.json()['data']['copysets'][0]['sync_percentage'] == 100.0
        assert response.json()['data']['copysets'][2]['state'] == 'Copying'
        assert response.json()['data']['copysets'][2]['sync_percentage'] == 75.5
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'

    @responses.activate
    def test_add_copysets_success(self):
        """Test successful addition of copysets to a session"""
        session_name = "PROD_SESSION_01"
        copysets = [
            ["DS8000:2107.ABC12:VOL:0004", "DS8000:2107.DEF34:VOL:0004"],
            ["DS8000:2107.ABC12:VOL:0005", "DS8000:2107.DEF34:VOL:0005"]
        ]
        roleorder = ["source", "target"]
        
        mock_response = {
            "status": "I",
            "message": "Copysets added successfully",
            "data": {
                "session_name": session_name,
                "copysets_added": 2,
                "added_copysets": [
                    {
                        "copyset_id": "COPYSET_004",
                        "copyset_name": "COPYSET_004",
                        "source_volume": "DS8000:2107.ABC12:VOL:0004",
                        "target_volume": "DS8000:2107.DEF34:VOL:0004",
                        "state": "Inactive",
                        "size_gb": 100.0
                    },
                    {
                        "copyset_id": "COPYSET_005",
                        "copyset_name": "COPYSET_005",
                        "source_volume": "DS8000:2107.ABC12:VOL:0005",
                        "target_volume": "DS8000:2107.DEF34:VOL:0005",
                        "state": "Inactive",
                        "size_gb": 150.0
                    }
                ],
                "total_copysets_in_session": 5
            }
        }
        
        responses.add(
            responses.POST,
            f"{self.base_url}/sessions/{session_name}/copysets",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = copyset_service.add_copysets(
            self.base_url,
            self.token,
            session_name,
            copysets,
            roleorder
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['copysets_added'] == 2
        assert len(response.json()['data']['added_copysets']) == 2
        assert response.json()['data']['added_copysets'][0]['copyset_id'] == 'COPYSET_004'
        assert response.json()['data']['added_copysets'][0]['state'] == 'Inactive'
        assert response.json()['data']['added_copysets'][1]['copyset_id'] == 'COPYSET_005'
        assert response.json()['data']['total_copysets_in_session'] == 5
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"

    @responses.activate
    def test_remove_copysets_success(self):
        """Test successful removal of copysets from a session"""
        session_name = "PROD_SESSION_01"
        copysets = ["DS8000:2107.ABC12:VOL:0003"]
        force = False
        soft = False
        
        mock_response = {
            "status": "I",
            "message": "Copysets removed successfully",
            "data": {
                "session_name": session_name,
                "copysets_removed": 1,
                "removed_copysets": [
                    {
                        "copyset_id": "COPYSET_003",
                        "source_volume": "DS8000:2107.ABC12:VOL:0003",
                        "target_volume": "DS8000:2107.DEF34:VOL:0003",
                        "removal_status": "success"
                    }
                ],
                "total_copysets_in_session": 2
            }
        }
        
        responses.add(
            responses.DELETE,
            f"{self.base_url}/sessions/{session_name}/{force}/{soft}/copysets",
            json=mock_response,
            status=HTTPStatus.OK.value,
            content_type='application/json'
        )
        
        response = copyset_service.remove_copysets(
            self.base_url,
            self.token,
            session_name,
            copysets,
            force,
            soft
        )
        
        assert response.status_code == HTTPStatus.OK.value
        assert response.json()['status'] == 'I'
        assert response.json()['data']['session_name'] == session_name
        assert response.json()['data']['copysets_removed'] == 1
        assert len(response.json()['data']['removed_copysets']) == 1
        assert response.json()['data']['removed_copysets'][0]['copyset_id'] == 'COPYSET_003'
        assert response.json()['data']['removed_copysets'][0]['removal_status'] == 'success'
        assert response.json()['data']['total_copysets_in_session'] == 2
        assert len(responses.calls) == 1
        assert responses.calls[0].request.headers['X-Auth-Token'] == self.token
        assert responses.calls[0].request.headers['Accept-Language'] == 'en-US'
        assert responses.calls[0].request.headers['Content-Type'] == "application/x-www-form-urlencoded"



if __name__ == '__main__':
    unittest.main()

# Made with Bob