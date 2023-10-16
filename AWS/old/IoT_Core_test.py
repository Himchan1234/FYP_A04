
import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import sys
sys.path.append("")
from config import AWS_IOT_CERT_KEY_PATH, AWS_IOT_PRIVATE_KEY_PATH, \
                AWS_IOT_CLIENT_ENDPOINT, AWS_IOT_ROOT_KEY_PATH

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

def publishData(client, txt):
    print(txt)
    ctr = 1
    while (True):
        msg = "Testing" + str(ctr)
        print(msg)
        client.publish("raspberrypi/data", payload=json.dumps({"msg": msg}), qos=0, retain=False)
        ctr = ctr + 1

        time.sleep(5)
def IoTmain():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.tls_set(ca_certs=AWS_IOT_ROOT_KEY_PATH, 
                certfile=AWS_IOT_CERT_KEY_PATH, 
                keyfile=AWS_IOT_PRIVATE_KEY_PATH, 
                tls_version=ssl.PROTOCOL_SSLv23)
    client.tls_insecure_set(True)
    client.connect(AWS_IOT_CLIENT_ENDPOINT, 8883, 60)
            
    _thread.start_new_thread(publishData,(client,("Spin-up new Thread...",)))

    client.loop_forever()

if __name__ == "__main__":
    IoTmain()