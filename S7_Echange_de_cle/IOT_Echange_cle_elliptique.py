from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import paho.mqtt.client as mqtt
import time


# Generate a private key for use in the exchange.
IOT_private_key = X25519PrivateKey.generate()

# Convert into bytes
IOT_private_bytes = IOT_private_key.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())

# Generate the public keys
IOT_public_key = IOT_private_key.public_key()

# Convert into bytes
IOT_public_bytes = IOT_public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)


TOPIC_IOP_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyIoT"
TOPIC_Serveur_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyServer"


BROKER_IP = "localhost"
PORT = 1884
USER = "username"
PASSWORD = "password"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => "+mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("\nReceived message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

def on_publish(client, userdata, mid):
    print("--on_publish callback --mid: " + str(mid) )

client = mqtt.Client(client_id="IOT04")
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.on_connect = on_connect

try:
    # client.username_pw_set(username=USER, password=PASSWORD)
    client.connect(BROKER_IP, PORT) # groupes 1 à 4
    #client.connect("m21.cloudmqtt.com", 13197) # groupes 5 à 8
    #client.connect("m21.cloudmqtt.com", 16511) # groupes 9 à 12
    #client.connect("m21.cloudmqtt.com", 10318) # groupes 13 à 16
    try:
        client.subscribe(TOPIC_Serveur_public_key, qos=0)
        client.loop_start()

        while True:
            (rc, mid) = client.publish(topic=TOPIC_IOP_public_key, payload=IOT_public_bytes, qos=0)
            print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
            time.sleep(5)

    except KeyboardInterrupt:
        client.loop_stop()
        client.unsubscribe()
        client.disconnect()
        print("Done.")
except:
    print("Connection Failed")

    

# A completer
# # shared keys
# # Must be equals (here we give public_key for each others)
# shared_IOT = IOT_private_key.exchange(Server_public_key)
