import json
from HammerSDK.hammer_client import HammerClient

def test_list_nodes(hammer_client, mock_connection):
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": "node1", "status": "online"},
        {"id": "node2", "status": "offline"}
    ]
    mock_connection.return_value.request.return_value = mock_response

    # Test API call
    nodes = hammer_client.nodes.list_nodes()
    assert len(nodes) == 2
    assert nodes[0]["id"] == "node1"
    
    # Verify URI construction
    mock_connection.return_value.request.assert_called_once_with(
        "GET", "/mgmt/v1.2/rest/nodes",
        body=None,
        request_content_type=None,
        headers={'Accept': 'application/json'}
    )

def test_get_node(hammer_client, mock_connection):
    mock_response = Mock()
    mock_response.json.return_value = {"id": "node1", "swVersion": "5.1.18"}
    mock_connection.return_value.request.return_value = mock_response

    node = hammer_client.nodes.get_node("node1")
    assert node["swVersion"] == "5.1.18"
    mock_connection.return_value.request.assert_called_once_with(
        "GET", "/mgmt/v1.2/rest/nodes/node1",
        body=None,
        request_content_type=None,
        headers={'Accept': 'application/json'}
    )
