from flask import jsonify
from . import app, mongodb

# Define API endpoint to retrieve warehouse information
@app.route("/api/warehouse", methods=["GET"])
def get_warehouse_info():
    # Get the warehouse collection
    warehouse_collection = mongodb.get_collection("warehouse")
    
    # Retrieve data from the warehouse collection
    warehouse_data = warehouse_collection.find_one()
    
    # Process the data as needed
    # ...
    
    # Return the response
    return jsonify(warehouse_data), 200
