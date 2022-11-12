import paho.mqtt.client as mqtt
import time

TOPIC = "isima/G4/led" #"isima/G4/bouton"
BROKER_IP = "localhost" # "172.16.32.7"
PORT = 3000 # 5204
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

client = mqtt.Client()
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
        client.subscribe('#', qos=0)
        client.loop_start()

        while True:
            # (rc, mid) = client.publish(topic=TOPIC, payload="TEST_G4", qos=0)
            # print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
            time.sleep(5)

    except KeyboardInterrupt:
        client.loop_stop()
        client.unsubscribe(TOPIC)
        client.disconnect()
        print("Done.")
except:
    print("Connection Failed")

    