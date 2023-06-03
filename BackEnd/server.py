from app import create_app
from flask import jsonify, request
from app.core.tasks import seed_task
from app.dbSeed import run_seed
from app import mqtt_init
app = create_app()


@app.before_request
def log_request_data():
    # Log the request data
    # app.logger.info('Request: %s %s %s', request.headers)
    app.logger.info('Request: %s %s %s', request.method, request.path,
                    request.data.decode('utf-8').replace('\r\n', '').replace(' ', ''))


@app.after_request
def log_response_data(response):
    # Log the response status and request method
    app.logger.info('Response: %s %s %s', response.status, request.method, request.path)

    return response


@app.errorhandler(Exception)
def handle_internal_error(e):
    # Log the error (optional)
    app.logger.exception('Unhandled Exception')

    # Return a JSON response with the error message
    response = {
        'message': 'Something went wrong',
    }
    return jsonify(response), 500


@app.errorhandler(404)
def handle_not_found_error(e):
    # Return a JSON response for 404 errors
    response = {
        'message': 'Not Found',
    }
    return jsonify(response), 404


@app.errorhandler(405)
def handle_not_found_error(e):
    # Return a JSON response for 405 errors
    response = {
        'message': 'Method not allowed for this route',
    }
    return jsonify(response), 405


@app.route('/status', methods=['GET'])
def status():
    return 'Running!'

# @app.route('/api/seed_task', methods=['POST'])
# def seed():
#     # Trigger the seed execution task
#     result = seed_task.apply_async()
#     return jsonify({'message': 'Seed process started.'}), 200


@app.route('/api/seed', methods=['POST'])
def seed():
    # Trigger the seed execution task
    run_seed()
    return jsonify({'message': 'Seed process started.'}), 200




if __name__ == '__main__':
    mqtt_init.init_mqtt()  # Call the init_mqtt function
    app.run()
