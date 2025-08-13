import pytest
from unittest.mock import Mock
from HammerSDK.hammer_client import HammerClient

@pytest.fixture
def mock_connection(monkeypatch):
    """Mock the Connection class to avoid real HTTP calls"""
    mock_conn = Mock()
    monkeypatch.setattr("HammerSDK.lib.request.Connection", mock_conn)
    return mock_conn

@pytest.fixture
def hammer_client(mock_connection):
    """Pre-configured HammerClient instance"""
    client = HammerClient("test.example.com")
    client.conninfo = mock_connection.return_value  # Inject mock
    return client
