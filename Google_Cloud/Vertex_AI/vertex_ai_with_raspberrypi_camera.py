import requests
# Import the base64 encoding library.
import base64
import os
import datetime
import time
from picamera2 import Picamera2, Preview
import sys
sys.path.append("")
from config import GOOGLE_PROJECT_ID, GOOGLE_CLOUD_API_KEY_PATH

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Pass the image data to an encoding function.
def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def read_key_from_file():
    key_file_path = GOOGLE_CLOUD_API_KEY_PATH  # Generate the path to key.txt

    with open(key_file_path, 'r') as f:
        return f.read().strip()  # Read key and strip whitespace

def vertax_api(img, question):
    access_token = read_key_from_file()
    project_id = GOOGLE_PROJECT_ID
    api_url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{project_id}/locations/us-central1/publishers/google/models/imagetext:predict"
    headers = {
        # access key from ##gcloud auth application-default print-access-token
        'Authorization': f'Bearer {access_token}',
    }
    base64img = encode_image(img)
    json_payload = {
        "instances": [
            {
                "prompt": question,
                "image": {
                    "bytesBase64Encoded": base64img
                }
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    
    response = requests.post(api_url, json=json_payload, headers=headers)
    if response.status_code == 401:
        return (response.json())
    else:
        return (response.json()['predictions'][0])

def CaptureImage():
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_directory = os.path.join('img', 'test')
    filepath = os.path.join(image_directory, f"{timestamp_str}.jpg")
    create_directory_if_not_exists(image_directory)
    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(main={"size": (800, 600)})
    picam2.configure(preview_config)
    picam2.start()
    time.sleep(2)
    metadata = picam2.capture_file(filepath)
    print(metadata)
    picam2.close()
    return filepath


def Vertex_main():
    capimg = CaptureImage()
    question1 = "any person here?"
    question2 = "is person wearing a head hat"
    ans1 = vertax_api(capimg, question1)
    if ans1 == "yes":
        ans2 = vertax_api(capimg, question2)
        print(os.path.basename(capimg), "wear hat", ans2)
    else:
        print(os.path.basename(capimg), ans1)

if __name__ == "__main__":
    Vertex_main()