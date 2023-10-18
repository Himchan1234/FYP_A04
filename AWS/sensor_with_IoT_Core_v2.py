from serial.tools import list_ports
import serial
import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import datetime
import sys
sys.path.append("")
from config import AWS_IOT_CERT_KEY_PATH, AWS_IOT_PRIVATE_KEY_PATH, \
                AWS_IOT_CLIENT_ENDPOINT, AWS_IOT_ROOT_KEY_PATH
from Google_Cloud.text_to_speech.gcp_text_to_speech import text_to_speech

test_mode = False

def connect_to_arduino(): 
    while True:
        try:
            # Identify the correct port
            ports = list(list_ports.comports())
            for port in ports:
                print(port)
                print(port.description)
                if "USB Serial" in port:
                    # Open the serial com
                    serialCom = serial.Serial(port.device, 9600)
                    print(f"Using port: {port.device}")
                    break
            # Toggle DTR to reset the Arduino
            serialCom.setDTR(False)
            time.sleep(1)
            serialCom.flushInput()
            serialCom.setDTR(True)
            print("Serial communication established.")
            time.sleep(10)
            return serialCom
        except:
            print("No suitable serial port found.")
            time.sleep(10)

def read_data(serialCom):
    try:
        # Read the line
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
        print("---")
        #print(decoded_bytes)
        return decoded_bytes
    except:
        print("Error encountered, line was not recorded.")

def on_connect(client, userdata, flags, rc):
    print("Connected to AWS IoT: " + str(rc))
    client.subscribe("raspberrypi/jsondata")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {str(msg.payload)}")
    msg_value = json.loads(msg.payload.decode('utf-8'))
    speech_msg = msg_value.get('speech_message', 'No message field')
    if speech_msg != 'No message field':
        print(speech_msg)
        text_to_speech(speech_msg)


def publishData(client, txt):
    print(txt)
    while True:
        if test_mode == False:
            serialCom = connect_to_arduino()
            data = read_data(serialCom)
        else:
            data = "123 443"
        #print(data)
        values = data.split()
        #print(values)
        if len(values) == 2:
            #print('json')
            jsonmsg = {
                "timestamp": datetime.datetime.now().strftime("%Y%m%d, %H:%M:%S"),
                "clientid": 1,
                "alcohol value": str(values[0]),
                "gas value": str(values[1])
            }
            client.publish("raspberrypi/data", payload=json.dumps(jsonmsg), qos=0, retain=False)
        else:
            print("Data output does not contain two values.")
        time.sleep(5)


def IoTmain():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(ca_certs=AWS_IOT_ROOT_KEY_PATH, 
                    certfile=AWS_IOT_CERT_KEY_PATH,
                    keyfile=AWS_IOT_PRIVATE_KEY_PATH, 
                    tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(True)
    client.connect(AWS_IOT_CLIENT_ENDPOINT, 8883, 60)

    _thread.start_new_thread(publishData, (client, "Spin-up new Thread...",))

    client.loop_forever()

if __name__ == "__main__":
    test_mode = True
    IoTmain()
