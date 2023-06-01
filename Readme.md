# IOT Smart Warehouse

Welcome to the IOT Smart Warehouse project! This project aims to develop a smart warehouse system using Python, Flask, MQTT, React-JS and MongoDB. The system will enable real-time monitoring and control of various warehouse operations.

## Getting Started

To set up the project on your local machine, follow the instructions below.

### Prerequisites

- Python installed on your system
- MongoDB installed and running
- Up and running Redis client

### Installation

1. Clone the repository:
    
    https://github.com/wahomins/SmartWarehouse


2. Navigate to the project directory:

    for the backend 

    `cd BackEnd`

    If you want to install redis via docker
    ```sh
    $ docker run -d --name="SmartWareHouse-redis" -p 6379:6379 redis
    ```

3. Create a virtual environment (optional but recommended):

    ```sh
    python -m venv env
    ```

Activate the virtual environment:

- For macOS and Linux:

  ```
  source env/bin/activate
  ```

- For Windows:

  ```
  env\Scripts\activate
  ```

4. Install the dependencies:

    ```
    pip install -r requirements.txt 
    ```

### Configuration
- There are 3 configurations `development`, `staging` and `production` in `config.py`. Default is `development`
- Create a `.env` file from `.env.example` and set appropriate environment variables before running the project

- Replace `<your-mongodb-uri>` with the connection URI for your MongoDB database. Set `<mqtt-broker-url>`, `<mqtt-username>`, and `<mqtt-password>` with the appropriate MQTT broker details.

### Starting the Server

To start the server, run the following command:

`python server.py`

The server will start running on the default port. You can modify the port number in the `server.py` file if needed.

#
- Logs would be generated under `log` folder

### Running celery workers

- Run redis locally before running celery worker
- Celery worker can be started with following command
```sh
# run following command in a separate terminal
$ celery -A celery_worker.celery worker --loglevel='INFO'
# (append `--pool=solo` for windows)
```


# Preconfigured Packages
Includes preconfigured packages to kick start flask app by just setting appropriate configuration.

| Package 	| Usage 	|
|-----	|-----	|
| [celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) 	| Running background tasks 	|
| [redis](https://redislabs.com/lp/python-redis/) 	| A Python Redis client for caching 	|
| [flask-cors](https://flask-cors.readthedocs.io/) 	| Configuring CORS 	|
| [python-dotenv](https://pypi.org/project/python-dotenv/) 	| Reads the key-value pair from .env file and adds them to environment variable. 	|
| [marshmallow](https://marshmallow.readthedocs.io/en/stable/) 	| A package for creating Schema, serialization, deserialization 	|
| [webargs](https://webargs.readthedocs.io/) 	| A Python library for parsing and validating HTTP request objects 	|

`autopep8` & `flake8` as `dev` packages for `linting and formatting`

# Test
  Test if this app has been installed correctly and it is working via following curl commands (or use in Postman)
- Check if the app is running via `status` API
```shell
$ curl --location --request GET 'http://localhost:5000/status'
```
- Check if core app API and celery task is working via
```shell
$ curl --location --request GET 'http://localhost:5000/api/core/test'
```
- Check if authorization is working via (change `API Key` as per you `.env`)
```shell
$ curl --location --request GET 'http://localhost:5000/api/core/restricted' --header 'x-api-key: 436236939443955C11494D448451F'
```

## Contact

If you have any questions or need further assistance, feel free to contact us at [smart warehouses](wahomins@gmail.com).

## License

This project is licensed under the [MIT License](LICENSE).
