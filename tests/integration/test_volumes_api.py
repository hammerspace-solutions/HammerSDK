def test_delete_volume(hammer_client, mock_connection):
    mock_response = Mock()
    mock_response.status_code = 204
    mock_connection.return_value.request.return_value = mock_response

    response = hammer_client.logical_volumes.delete_logical_volume("vol123")
    assert response.status_code == 204
    mock_connection.return_value.request.assert_called_once_with(
        "DELETE", "/mgmt/v1.2/rest/logical-volumes/vol123",
        body=None,
        request_content_type=None,
        headers={'Accept': 'application/json'}
    )
