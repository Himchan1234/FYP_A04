import requests
# Import the base64 encoding library.
import base64
import os
import datetime
#from google.cloud import storage
from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow
#from google.oauth2 import service_account
#from google.cloud import aiplatform


dirname = os.path.dirname(__file__)
key_file_path = os.path.join(dirname, '..', 'key', 'service_account_key.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path

'''

def get_access_token():
    key_file = 'key/service_account_key.json'  # Update with your service account key
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    credentials = service_account.Credentials.from_service_account_file(
        key_file, scopes=scopes)*

    
    return credentials.token

def upload_file_to_bucket(bucket_name: str, path_name: str, source_file_name: str, content_type: str = "image/jpeg"):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(path_name)
    blob.upload_from_filename(source_file_name, content_type)
'''
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Pass the image data to an encoding function.
def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def read_key_from_file():
    dirname = os.path.dirname(__file__)  # Get the directory where the script is located
    key_file_path = os.path.join(dirname, '..', 'key', 'key.txt')  # Generate the path to key.txt

    with open(key_file_path, 'r') as f:
        return f.read().strip()  # Read key and strip whitespace

def vertax_api(img, question):
    access_token = read_key_from_file()
    project_id = "crafty-willow-399607"
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
# https://www.geeksforgeeks.org/how-to-capture-a-image-from-webcam-in-python/
def CaptureImage():
    cam_port = 0
    cam = VideoCapture(cam_port)
    result, image = cam.read()
    if result:
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_directory = os.path.join('img', 'test')
        filepath = os.path.join(image_directory, f"{timestamp_str}.jpg")
        create_directory_if_not_exists(image_directory)
        imwrite(filepath, image)
        return filepath
    
    else:
        print("No image detected. Please! try again")

def CaptureImage2():
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_directory = os.path.join('img', 'test')
        filenmae = os.path.join(image_directory, f"{timestamp_str}.jpg")
        create_directory_if_not_exists(image_directory)

def main2():
    capimg = CaptureImage()
    question1 = "any person here?"
    question2 = "is person wearing a head hat"
    ans1 = vertax_api(capimg, question1)
    if ans1 == "yes":
        ans2 = vertax_api(capimg, question2)
        print(os.path.basename(capimg), "wear hat", ans2)
    else:
        print(os.path.basename(capimg), ans1)

def main1():
    question1 = "any person here?"
    question2 = "is person wearing a head hat"
    image_directory = "./img"
    for filename in os.listdir(image_directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            full_image_path = os.path.join(image_directory, filename)
            ans1 = vertax_api(full_image_path, question1)
            if ans1 == "yes":
                ans2 = vertax_api(full_image_path, question2)
                print(filename, "wear hat", ans2)
            else:
                print(filename, ans1)


if __name__ == "__main__":
    main2()