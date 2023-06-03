import pytest
from flask import json
from app import create_app
from bson.objectid import ObjectId

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
    return {
            'username': 'testuser_warehouses',
            'password': 'testP@ssword1',
            'email': 'test_warehouses@example.com',
            'full_name': 'Test User',
            'role': 'admin'
        }


@pytest.fixture(scope='function')
def registered_user(app, warehouse_user):
    with app as client:
        response = client.post('/api/users', json=warehouse_user, follow_redirects=True)

        assert response.status_code == 200
        response_data = response.get_json()
        assert 'user' in response_data

        return response_data['user']


@pytest.fixture(scope='function')
def access_token(client, warehouse_user):
    login_payload = {
        "username": warehouse_user['username'],
        "password": warehouse_user['password']
    }

    response = client.post('/api/users/login', json=login_payload)
    assert response.status_code == 200

    return json.loads(response.data)['token']


@pytest.fixture(scope='function')
def warehouse_data():
    return {
        'name': 'Warehouse A',
        'latitude': 51.1234,
        'longitude': 0.5678,
        'close_land_mark': 'ABC',
        'town': 'Test Town',
        'description': 'Test Description',
        'manager_id': ObjectId(),
        'created_by': ObjectId(),
    }


@pytest.fixture(scope='function')
def create_warehouse(client, warehouse_data, authenticated_user):
    warehouse_data['created_by'] = authenticated_user['user_id']
    response = client.post(
        '/api/warehouses/',
        json=warehouse_data,
        headers={'Authorization': authenticated_user['token']}
    )
    return response


@pytest.fixture(scope='function')
def update_warehouse(client, create_warehouse, authenticated_user):
    warehouse_id = create_warehouse.json['_id']
    response = client.put(
        f'/api/warehouses/{warehouse_id}',
        json={'name': 'Updated Warehouse'},
        headers={'Authorization': authenticated_user['token']}
    )
    return response


def test_get_warehouses(client, authenticated_user):
    response = client.get(
        '/api/warehouses/',
        headers={'Authorization': authenticated_user['token']}
    )
    assert response.status_code == 200


def test_create_warehouse(create_warehouse):
    assert create_warehouse.status_code == 201
    assert 'name' in create_warehouse.json
    assert create_warehouse.json['name'] == 'Warehouse A'


def test_get_warehouse(client, create_warehouse, authenticated_user):
    warehouse_id = create_warehouse.json['_id']
    response = client.get(
        f'/api/warehouses/{warehouse_id}',
        headers={'Authorization': authenticated_user['token']}
    )
    assert response.status_code == 200
    assert 'name' in response.json
    assert response.json['name'] == 'Warehouse A'


def test_update_warehouse(update_warehouse):
    assert update_warehouse.status_code == 200
    assert 'name' in update_warehouse.json
    assert update_warehouse.json['name'] == 'Updated Warehouse'


def test_delete_warehouse(client, create_warehouse, authenticated_user):
    warehouse_id = create_warehouse.json['_id']
    response = client.delete(
        f'/api/warehouses/{warehouse_id}',
        headers={'Authorization': authenticated_user['token']}
    )
    assert response.status_code == 200
    assert response.json['message']
