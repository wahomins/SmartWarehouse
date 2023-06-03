import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

    # Subscribe to topics
    client.subscribe("topic1")
    client.subscribe("topic2")
    # Add more subscriptions as needed

def on_message(client, userdata, msg):
    print("Received message: ", msg.topic, msg.payload.decode())

def init_mqtt():
    # Create a new MQTT client
    client = mqtt.Client()

    # Set the MQTT client callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Configure connection parameters (broker address, port, etc.)
    client.connect("mqtt.example.com", 1883, 60)

    # Start the MQTT client loop in a separate thread
    client.loop_start()
