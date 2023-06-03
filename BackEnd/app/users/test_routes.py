import json
import pytest
from app import create_app
import random
import string


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app


@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def new_user():
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(4))
    return {
            'username': f'testuser1-{name}',
            'password': 'testP@ssword1',
            'email': f'test@example{name}.com',
            'full_name': 'Test User',
            'role': 'user'
        }


@pytest.fixture(scope='function')
def registered_user(client, new_user):
        response = client.post('/api/users', json=new_user, follow_redirects=True)
        print(f'Test users {response}')
        assert response.status_code == 201
        response_data = response.get_json()
        assert 'user_id' in response_data
        # Add more assertions to validate the response data

        return response_data['user_id']

@pytest.fixture(scope='function')
def access_token(client, registered_user, new_user):
    login_payload = {
        "username": new_user['username'],
        "password": new_user['password']
    }

    response = client.post('/api/users/login', json=login_payload)
    assert response.status_code == 200
    response_data = response.get_json()
    return response_data


def test_login(client, registered_user, new_user):
    # Prepare the test data
    data = {
        'username': new_user['username'],
        'password': new_user['password']
    }

    # Send a POST request to the /login route
    response = client.post('/api/users/login', json=data)

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    response_data = json.loads(response.data)
    assert 'token' in response_data
    assert 'user_id' in response_data
    assert 'email' in response_data
    assert 'full_name' in response_data


def test_login_invalid_credentials(client):
        response = client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        # Assert that the response is as expected for invalid credentials
        assert response.status_code == 401
        # Add more assertions to validate the response data

def test_add_user(client, access_token):
    # Prepare the test data
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(4))
    jwt = access_token['token']
    data = {
        'email': f'test{name}@example.com',
        'username': f'test{name}',
        'full_name': 'John Doe',
        'role': 'staff'
    }

    response = client.post('/api/users/add_user',
        json=data,
        headers={'Authorization':  f'Bearer {jwt}'}
    )

    assert response.status_code == 201
    response_data = response.get_json()
    assert 'message' in response_data
    assert 'user_id' in response_data
