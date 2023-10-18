# Import boto3 library for interacting with AWS services
import os
import boto3
import sys
sys.path.append("")
from config import AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN

def upload_to_s3(image_name, local_file_path):
    bucket_name = AWS_S3_BUCKET

    session = boto3.Session(
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        aws_session_token = AWS_SESSION_TOKEN
    )
    try:
        # Create a client object for S3 service
        s3_client = session.client('s3')

        # Upload the photo to S3 bucket using the client object
        s3_client.upload_file(local_file_path, bucket_name, image_name)

        # Print a success message
        print('Photo uploaded successfully to S3 bucket.')
    except Exception as e:
        print("An error occurred:", str(e))
        
if __name__ == "__main__":
    upload_to_s3("NoHelmaImage/20231016.jpg","img/no hat.jpg")