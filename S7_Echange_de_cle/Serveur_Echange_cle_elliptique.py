from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import paho.mqtt.client as mqtt
import time



# Generate a private key for use in the exchange.
Serveur_private_key = X25519PrivateKey.generate()

# Convert into bytes
Serveur_private_bytes = Serveur_private_key.private_bytes(encoding=serialization.Encoding.Raw, format=serialization.PrivateFormat.Raw, encryption_algorithm=serialization.NoEncryption())

# Generate the public keys
Serveur_public_key = Serveur_private_key.public_key()

# Convert into bytes
Serveur_public_bytes = Serveur_public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)


TOPIC_IOT_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyIoT"
TOPIC_Serveur_public_key = "/ISIMA/S7_DH/GROUPE_4/PublicKeyServer"





BROKER_IP = "localhost"
PORT = 3000 # 1884
USER = "username"
PASSWORD = "password"

Exchange_key_from_IOT = b''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => "+mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("\nReceived message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

    # On affiche la clé publique:
    if len(msg.payload) == 32: 
        print("Public key from IOT: " + str(msg.payload))
        Exchange_key_from_IOT = msg.payload

        shared_Serveur = Serveur_private_key.exchange( X25519PublicKey.from_public_bytes(Exchange_key_from_IOT) )
        print("La clé d'echange calculée est:" + str(shared_Serveur))

def on_publish(client, userdata, mid):
    print("--on_publish callback --mid: " + str(mid) )

client = mqtt.Client(client_id="Serveur04")
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.on_connect = on_connect

# Message retenu => on ne publie qu'une seule fois et on s'abonne pour récupérer la clé q'une suele fois sans spam
# Pour être spur qu'il est correcte on augmente donc la qualité de service

try:
    # client.username_pw_set(username=USER, password=PASSWORD)
    client.connect(BROKER_IP, PORT)# groupes 1 Ãƒ  4
    #client.connect("m21.cloudmqtt.com", 13197) # groupes 5 Ãƒ  8
    #client.connect("m21.cloudmqtt.com", 16511) # groupes 9 Ãƒ  12
    #client.connect("m21.cloudmqtt.com", 10318) # groupes 13 Ãƒ  16
    
    try:
        # On envoie notre clé sur le broker
        (rc, mid) = client.publish(topic=TOPIC_Serveur_public_key, payload=Serveur_public_bytes, qos=1, retain=True)
        print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))

        #On s'abonne pour récupérer la clé du serveur
        client.subscribe(TOPIC_IOT_public_key, qos=1)
        client.loop_start()

        # On a pas besoin de spam le message car il est retenu
        while True:
            # (rc, mid) = client.publish(topic=TOPIC_Serveur_public_key, payload=Serveur_public_bytes, qos=0)
            # print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
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


# A completer
# # shared keys
# # Must be equals (here we give public_key for each others)
# shared_Serveur = Serveur_private_key.exchange(Server_public_key)