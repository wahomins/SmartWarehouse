import pytest
from flask import json
from app import create_app
from bson.objectid import ObjectId
from werkzeug.local import LocalProxy
from flask import current_app
import random
import string


logger = LocalProxy(lambda: current_app.logger)

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
def warehouse_user():
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(4))
    return {
            'username': f'testuser_warehouses {name}',
            'password': 'testP@ssword1',
            'email': f'test_warehouses{name}@example.com',
            'full_name': 'Test User',
            'role': 'admin'
        }


@pytest.fixture(scope='function')
def registered_user(client, warehouse_user):
    response = client.post('/api/users', json= warehouse_user, follow_redirects=True)

    assert response.status_code == 201
    response_data = response.get_json()
    assert 'user_id' in response_data

    return response_data['user_id']


@pytest.fixture(scope='function')
def access_token(client, registered_user, warehouse_user):
    login_payload = {
        "username": warehouse_user['username'],
        "password": warehouse_user['password']
    }

    response = client.post('/api/users/login', json=login_payload)
    assert response.status_code == 200
    response_data = response.get_json()
    return response_data


@pytest.fixture(scope='function')
def warehouse_data():
    
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(4))
    return {
        'name': f'Warehouse {name}',
        'latitude': 51.1234,
        'longitude': 0.5678,
        'close_land_mark': 'ABC',
        'town': 'Test Town',
        'description': 'Test Description',
        'manager_id': ObjectId(),
        'created_by': ObjectId(),
    }


@pytest.fixture(scope='function')
def create_warehouse(client, warehouse_data, access_token):
    warehouse_data['created_by'] = access_token['user_id']
    warehouse_data['manager_id'] = access_token['user_id']
    jwt = access_token['token']
    response = client.post(
        '/api/warehouses/',
        json=warehouse_data,
        headers={'Authorization':  f'Bearer {jwt}'}
    )
    print(response)
    assert response.status_code == 201
    response_data = response.get_json()
    assert '_id' in response_data
    return response_data

# def test_registered_user(client, warehouse_user):
#         response = client.post('/api/users', json= {
#             'username': 'testuser_warehouses',
#             'password': 'testP@ssword1',
#             'email': 'test_warehouses@example.com',
#             'full_name': 'Test User',
#             'role': 'admin'
#         }, follow_redirects=True)

#         assert response.status_code == 201
#         response_data = response.get_json()
#         assert 'user_id' in response_data

#         return response_data['user_id']

def test_get_warehouses(client, access_token):
    jwt = access_token['token']
    response = client.get(
        '/api/warehouses/',
        headers={'Authorization':  f'Bearer {jwt}'}
    )
    assert response.status_code == 200


def test_create_warehouse(create_warehouse, warehouse_data):
    assert 'name' in create_warehouse
    assert create_warehouse['name'] == warehouse_data['name']


def test_get_warehouse(client, create_warehouse, access_token, warehouse_data):
    warehouse_id = create_warehouse['_id']    
    jwt = access_token['token']
    response = client.get(
        f'/api/warehouses/{warehouse_id}',
        headers={'Authorization':  f'Bearer {jwt}'}
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'name' in response_data
    assert response_data['name'] == warehouse_data['name']

def test_update_warehouse(client, create_warehouse, access_token):
    warehouse_id = create_warehouse['_id']
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for _ in range(4))
    jwt = access_token['token']
    response = client.put(
        f'/api/warehouses/{warehouse_id}',
        json={'name': f'Updated Warehouse-{name}'},
        headers={'Authorization':  f'Bearer {jwt}'}
    )
    assert response.status_code == 200
    response_data = response.get_json()
    assert 'name' in response_data
    assert response_data['name'] == f'Updated Warehouse-{name}'


def test_delete_warehouse(client, create_warehouse, access_token):
    warehouse_id = create_warehouse['_id']
    jwt = access_token['token']
    response = client.delete(
        f'/api/warehouses/{warehouse_id}',
        headers={'Authorization':  f'Bearer {jwt}'}
    )
    assert response.status_code == 200
    assert response.json['message']
