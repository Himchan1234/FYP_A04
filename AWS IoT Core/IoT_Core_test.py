
import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./AWS IoT Core/rootCA.pem', certfile='./AWS IoT Core/certificate.pem.crt', keyfile='./AWS IoT Core/private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a202h15648vyzh-ats.iot.us-east-1.amazonaws.com", 8883, 60)

def publishData(txt):
    print(txt)
    ctr = 1
    while (True):
        msg = "Testing" + str(ctr)
        print(msg)
        client.publish("raspberrypi/data", payload=json.dumps({"msg": msg}), qos=0, retain=False)
        ctr = ctr + 1

        time.sleep(5)
        
_thread.start_new_thread(publishData,("Spin-up new Thread...",))

client.loop_forever()