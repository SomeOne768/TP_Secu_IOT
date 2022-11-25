# -nNvXxA
# "C:\\Users\\regiraudon\\AppData\\Local\\Arduino15\\packages\\Intel\\tools\\arc-elf32\\1.6.9+1.0.1/bin/arc-elf32-objcopy" -I ihex "C:\\Users\\regiraudon\\zz2\\original.hex" -O binary "C:\\Users\\regiraudon\\zz2\\original.bin"

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => "+mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

def on_publish(client, userdata, mid):
    print("--on_publish callback --mid: " + str(mid) )

client = mqtt.Client("GROUPE_04p")
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

client.on_connect = on_connect

try:

    #tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    #tls_version=ssl.PROTOCOL_TLS, ciphers=None)


    #tls_set("mosquitto.org", "client.crt", "client.key", cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    client.tls_set("mosquitto.org.crt" ,certfile="client.crt", keyfile = "client.key")
    client.tls_insecure_set(True)
    client.connect(host= "test.mosquitto.org", port = 8884, keepalive= 60) 
    
except:
    print("Connection Failed")

try:
    #client.subscribe("isima/GYass/#", qos=0)
    client.subscribe("#", qos=0)
    client.loop_start()

    while True:

        (rc, mid) = client.publish(topic="/ISIMA/TP_5/GROUPE_03p", payload="ON", qos=0)

        print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
        time.sleep(5)

except KeyboardInterrupt:
    client.loop_stop()
    client.unsubscribe("/ISIMA/#")
    client.disconnect()
    print("Done.")