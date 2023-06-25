# IOT Smart Warehouse

Welcome to the IOT Smart Warehouse project! This project aims to develop a smart warehouse system using Python, Flask, MQTT, React-JS and MongoDB. The system will enable real-time monitoring and control of various warehouse operations.

## Getting Started

To set up the project on your local machine, follow the instructions below.

### Prerequisites

- Python installed on your system
- MongoDB installed and running
- Up and running Redis client
- Docker installed and running on your system

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
- There are 4 configurations `development`, `test`, `staging` and `production` in `config.py`. Default is `development`
- Create a `.env` file from `.env.example` and set appropriate environment variables before running the project

- Replace `<your-mongodb-uri>` with the connection URI for your MongoDB database. Set `<mqtt-broker-url>`, `<mqtt-username>`, and `<mqtt-password>` with the appropriate MQTT broker details.

### Managing Eclipse MQTT Broker using Docker

#### Prerequisites

- Docker installed and running on your system

#### Configuring the MQTT Broker

1. To configure the MQTT broker, update the configuration file located at `broker/config/mosquitto.conf` with the desired settings.

2. The folder `broker/keys` contains the certificates and a script for generating the certificates. 
There is a `config.ini` file with setting `COMMON_NAME` for mqtt host name keys setting, the default is `localhost`
To generate the certificates execute the following command in the `broker/keys` directory
    ```
    bash make_keys.sh
    ```

3. Start the MQTT broker container with the updated configuration:

    ```
    docker-compose -f broker/docker-compose.yml up -d
    ```
   Or navigate to broker/ 

    ```
    docker compose up -d
    ```

#### Updating MQTT Broker Credentials

1. To change the broker username and password
    ```
     docker-compose exec mosquitto mosquitto_passwd -c /broker/config/mosquitto.passwd <username>
    ```
    replace the variable `<username>` with a new username. Then enter the password twice.

2. Restart the MQTT broker container for the changes to take effect:

    ```
    docker-compose -f broker/docker-compose.yml restart
    ```


#### Starting the MQTT Broker

1. Build and start the Docker container with the provided docker-compose.yml file:

    ```
    docker-compose -f broker/docker-compose.yml up -d
    ```

   This command starts the MQTT broker container and maps port 1883 (unencrypted) and 8883 (encrypted).

   The default username is `mosquitto`, the default password is `mosquitto`

#### Stopping the MQTT Broker

1. To stop the MQTT broker container, use the following command:
    ```
    docker-compose -f broker/docker-compose.yml down
    ```

## Configuring the MQTT Client

1. From the keys the generated on broker config,`ca.cert`,`client.crt` and `client.key`, copy the files to the `app/mqtt/certs` directory.

2. Change the configs for the broker connection in the .env file


## MQTT Message Structure

- There are three main topics: TO_HOST, TO_DEVICE, and CLIENT_CONNECTIONS.

#### TO_HOST
The `TO_HOST` topic is used for messages being sent from devices to the server.

Topic format: `TO_HOST/<device_group>/<device_subgroup>/<device_id>`

| Key | Description |
| --- | --- |
| data | The payload to be processed by the server. |

Example message:
```json
{
  "data": {
    "name": "John",
    "status": "active",
    "ip": "192.168.0.1"
  }
}
```
#### TO_DEVICE
The `TO_DEVICE` topic is used for messages being sent from the server to the devices.

Topic format: `TO_DEVICE/<device_group>/<device_subgroup>/<device_id>`

| Key | Description |
| --- | --- |
| data | The payload for the device to process. |

Example message:
```json
{
  "data": {
    "command": "start",
    "duration": 10
  }
}
```
#### CLIENT_CONNECTIONS
The `CLIENT_CONNECTIONS` topic is used for logging device connections to the MQTT broker.

Topic: `CLIENT_CONNECTIONS` 

Topic format: `CLIENT_CONNECTIONS/<device_id>`

| Key | Description |
| --- | --- |
| data | Information about the connected device. |

Example message:
```json
{
  "data": {
    "name": "Device1",
    "status": "connected",
    "ip": "192.168.0.2"
  }
}
```


Devices can also log actions happening on them in this topic.

Topic format: `CLIENT_CONNECTIONS/activity/<device_id>`

Example message:
```json
{
  "data": {
    "name": "main_door",
    "action": "opened",
    "meta_data": {
        "user_id": "2g36y489derty87",
        "timestamp": "2023-05-14 12:12"
    }
  }
}
```

These are the main topics and message structures used in the MQTT communication. Devices publish to the `TO_HOST` topic and subscribe to the `TO_DEVICE` topic based on their device group, subgroup, and ID. The `CLIENT_CONNECTIONS` topic is used to log device connections to the MQTT broker.


### Starting the Server

To start the server, run the following command:

`python server.py`

To start in production, run:

`gunicorn -c gunicorn_config.py server:server`

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
## Contact

If you have any questions or need further assistance, feel free to contact us at [smart warehouses](wahomins@gmail.com).
