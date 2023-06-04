from flask import Blueprint, request, jsonify, current_app
from app.utils.auth import authenticate, authorize_role
from app.utils.validation import validate_request
from flask_pydantic import validate
from .models import Warehouse, get_warehouse_by_id, get_all_warehouses, create_warehouse, update_warehouse, delete_warehouse, format_response
from .validations import CreateWarehouseModel, UpdateWarehouseModel

warehouses_bp = Blueprint('warehouses', __name__)


@warehouses_bp.route('/', methods=['GET'])
@authenticate
def get_warehouses_route(decoded_token):
    warehouses = get_all_warehouses()
    return jsonify(warehouses), 200

@warehouses_bp.route('/warehouse/', methods=['GET'])
def get_warehouse_by_name_and_town():
    name = request.args.get('name')
    town = request.args.get('town')

    try:
        warehouse = Warehouse.objects.get(name=name, town=town)
        return jsonify(format_response(warehouse))
    except Warehouse.DoesNotExist:
        return jsonify({'message': 'Warehouse not found'}), 404


@warehouses_bp.route('/<warehouse_id>', methods=['GET'])
@authenticate
def get_warehouse_route(decoded_token, warehouse_id):
    warehouse = get_warehouse_by_id(warehouse_id)
    if warehouse:
        return jsonify(warehouse), 200
    else:
        return jsonify({'message': 'Warehouse not found'}), 404

@warehouses_bp.route('/', methods=['POST'])
@authenticate
@authorize_role(['admin'])  # Check if user has 'admin' role
@validate(body=CreateWarehouseModel)
# @validate_request(warehouse_create_schema)
def create_warehouse_route(decoded_token):
    data = request.json
    data['created_by'] = decoded_token['user_id']
    warehouse = create_warehouse(data)
    return jsonify(warehouse), 201

@warehouses_bp.route('/<warehouse_id>', methods=['PUT'])
@authenticate
@authorize_role(['admin', 'manager'])  # Check if user has 'admin' role
@validate(body=UpdateWarehouseModel)
def update_warehouse_route(decoded_token, warehouse_id):
    data = request.json
    data['updated_by'] = decoded_token['user_id']
    warehouse = get_warehouse_by_id(warehouse_id)
    if warehouse:
        warehouse = update_warehouse(warehouse_id, data)
        return jsonify(warehouse), 200
    else:
        return jsonify({'message': 'Warehouse not found'}), 404


@warehouses_bp.route('/<warehouse_id>', methods=['DELETE'])
@authenticate
@authorize_role(['admin'])  # Check if user has 'admin' role
def delete_warehouse_route(decoded_token, warehouse_id):
        deleted = delete_warehouse(warehouse_id)
        return (jsonify({'message': 'Warehouse deleted successfully'}), 200) if deleted else (jsonify({'message': 'Warehouse not found'}), 404)
