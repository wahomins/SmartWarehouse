import json
import pytest
from app import create_app
from werkzeug.local import LocalProxy


logger = LocalProxy(lambda: current_app.logger)


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        yield client

# @pytest.fixture(scope='function')
# def registered_user(app):
#     with app.test_client() as client:
#         response = client.post('/api/users', json={
#             'username': 'testuser',
#             'password': 'testpassword',
#             'email': 'test@example.com',
#             'full_name': 'Test User',
#             'role': 'user'
#         })

#         # Assert that the response is as expected for a successful registration
#         assert response.status_code == 201
#         # Add more assertions to validate the response data

#         # Return the created user for further testing
#         return response.json['user']

@pytest.fixture(scope='function')
def registered_user(app):
    with app as client:
        response = client.post('/api/users', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'full_name': 'Test User',
            'role': 'user'
        }, follow_redirects=True)

        assert response.status_code == 200
        response_data = response.get_json()
        assert 'user' in response_data
        # Add more assertions to validate the response data

        return response_data['user']



def test_login(app):
    # Prepare the test data
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    # logger.debug(f'Running Login Test: {data}')

    # Send a POST request to the /login route
    response = app.post('/api/users/login', json=data)

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    response_data = json.loads(response.data)
    assert 'token' in response_data
    assert 'user_id' in response_data
    assert 'email' in response_data
    assert 'full_name' in response_data

def test_login_successful(app, registered_user):
    # logger.debug(f'Running Login Test Successful: {registered_user}')

    with app as client:
        response = client.post('/api/users/login', json={
            'username': registered_user['username'],
            'password': 'testpassword'
        }, follow_redirects=True)

        # Assert that the response is as expected for a successful login
        assert response.status_code == 200
        # Add more assertions to validate the response data

def test_login_invalid_credentials(app):
    # logger.debug(f'Running Login Test INalid Creds: ')
    with app as client:
        response = client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        # Assert that the response is as expected for invalid credentials
        assert response.status_code == 401
        # Add more assertions to validate the response data
