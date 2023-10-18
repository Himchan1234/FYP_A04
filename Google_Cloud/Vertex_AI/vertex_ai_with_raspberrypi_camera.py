import requests
# Import the base64 encoding library.
import base64
import os
import datetime
import time
from picamera2 import Picamera2, Preview
import sys
sys.path.append("")
from config import GOOGLE_API_PROJECT_ID, GOOGLE_SERVICE_ACCOUNT_PATH
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Pass the image data to an encoding function.
def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def vertax_api(img, question):
    creds = Credentials.from_service_account_file(
        GOOGLE_SERVICE_ACCOUNT_PATH,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    creds.refresh(Request())

    access_token = creds.token
    project_id = GOOGLE_API_PROJECT_ID
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
    img_name = f"{timestamp_str}.jpg"
    return filepath, img_name


def Vertex_main():
    capimg, img_name = CaptureImage()
    capimg = "img/hat (2).jpg"
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