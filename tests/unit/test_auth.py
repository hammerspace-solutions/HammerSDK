from HammerSDK.rest.auth import login

def test_login_success(mock_connection):
    # Setup mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"session": "valid"}
    mock_connection.return_value.request.return_value = mock_response

    # Test
    response = login(mock_connection.return_value, "user", "pass")
    assert response.json()["session"] == "valid"
    mock_connection.return_value.request.assert_called_once()
