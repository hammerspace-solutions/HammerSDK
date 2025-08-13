def test_client_initialization(hammer_client, mock_connection):
    assert hammer_client.port == 8443
    mock_connection.return_value.open.assert_called_once()
