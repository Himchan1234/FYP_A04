import base64
import requests
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from config import GOOGLE_API_PROJECT_ID, GOOGLE_SERVICE_ACCOUNT_PATH


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
    if response.status_code == 401 or response.status_code == 403:
        return (response.json())
    else:
        return (response.json()['predictions'][0])