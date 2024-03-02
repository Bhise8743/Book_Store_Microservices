def test_user_registration(client, user_data):
    response = client.post('/register', json=user_data)
    assert response.status_code == 201


def test_user_login(client, user_data, user_login):
    response = client.post('/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/login', json=user_login)
    assert response.status_code == 200


def test_not_valid_user(client, not_valid_user_data):  # pydantic data is not valid
    response = client.post('/register', json=not_valid_user_data)
    assert response.status_code == 422


def test_login_error(client, user_data, login_error):
    response = client.post('/register', json=user_data)
    assert response.status_code == 201

    response = client.post('/login', json=login_error)
    assert response.status_code == 400
