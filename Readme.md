# IOT Smart Warehouse

Welcome to the IOT Smart Warehouse project! This project aims to develop a smart warehouse system using Python, Flask, MQTT, and MongoDB. The system will enable real-time monitoring and control of various warehouse operations.

## Getting Started

To set up the project on your local machine, follow the instructions below.

### Prerequisites

- Python installed on your system
- MongoDB installed and running

### Installation

1. Clone the repository:
    
    https://github.com/wahomins/SmartWarehouse


2. Navigate to the project directory:


3. Create a virtual environment (optional but recommended):

    ```
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

1. Create a `.env` file in the root directory.

2. Define the following environment variables in the `.env` file:

    ```
    MONGODB_URI=<your-mongodb-uri>
    MQTT_BROKER=<mqtt-broker-url>
    MQTT_USERNAME=<mqtt-username>
    MQTT_PASSWORD=<mqtt-password>
    PORT=5550
    ```


Replace `<your-mongodb-uri>` with the connection URI for your MongoDB database. Set `<mqtt-broker-url>`, `<mqtt-username>`, and `<mqtt-password>` with the appropriate MQTT broker details.

### Starting the Server

To start the server, run the following command:

`python server.py`

The server will start running on the default port. You can modify the port number in the `server.py` file if needed.

## API Endpoints

- `GET /api/warehouse`: Retrieve information about the warehouse status.
- `POST /api/warehouse`: Update the warehouse status.
- Add more endpoints as needed for your specific requirements.

## Contributing

Contributions to the IOT Smart Warehouse project are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes and test thoroughly.
4. Commit your changes and push the branch to your forked repository.
5. Submit a pull request describing your changes.

Please adhere to the coding conventions and commit message guidelines in this project.

## Contact

If you have any questions or need further assistance, feel free to contact us at [smart warehouses](wahomins@gmail.com).

## License

This project is licensed under the [MIT License](LICENSE).
