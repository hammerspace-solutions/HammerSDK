import pytest
import requests
from unittest.mock import Mock, patch
from HammerSDK.lib.request import Connection, LOGIN_ERROR

@pytest.fixture
def mock_session():
    """Fixture to mock requests.Session"""
    with patch('requests.Session') as mock_session:
        yield mock_session
        
def test_connection_initialization():
    conn = Connection("api.example.com", 8443)
    assert conn.host == "api.example.com"
    assert conn.port == 8443
    assert conn.session is None

def test_open_connection():
    conn = Connection("api.example.com", 8443)
    conn.open()
    assert conn.session is not None
    assert isinstance(conn.session, requests.Session)

def test_request_authentication_failure():
    conn = Connection("api.example.com", 8443)
    with pytest.raises(requests.ConnectionError, match=LOGIN_ERROR):
        conn.request("GET", "/test")

@patch('requests.Session.send')
def test_successful_request(mock_send):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "success"}
    mock_send.return_value = mock_response

    conn = Connection("api.example.com", 8443)
    conn.open()
    response = conn.request("GET", "/test")
    
    assert response.json() == {"data": "success"}
    mock_send.assert_called_once()

@patch('requests.Session.send')
def test_task_polling_handling(mock_send):
    conn = Connection("api.example.com", 8443)
    conn.open()

    # Mock initial 202 response with Location header
    task_response = Mock()
    task_response.status_code = 202
    task_response.headers = {"Location": "https://api.example.com/task/123"}
    
    # Mock final completed response
    completed_response = Mock()
    completed_response.status_code = 200
    completed_response.json.return_value = {"status": "COMPLETED"}
    
    mock_send.side_effect = [task_response, completed_response]

    response = conn.request("GET", "/mgmt/v1.2/rest/async-op")
    assert response.json()["status"] == "COMPLETED"
    assert mock_send.call_count == 2
    
