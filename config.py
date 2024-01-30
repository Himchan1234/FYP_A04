from key.key import *
import configparser

GOOGLE_CLOUD_API_KEY_PATH = key["google_api_key"]
GOOGLE_API_PROJECT_ID = value["google_api_project_id"]
GOOGLE_SERVICE_ACCOUNT_PATH = './key/google_service_account.json'

AWS_IOT_PRIVATE_KEY_PATH = "./key/IoT_private.pem.key"
AWS_IOT_PUBLIC_KEY_PATH = "./key/IoT_public.pem.key"
AWS_IOT_ROOT_KEY_PATH = "./key/IoT_rootCA.pem"
AWS_IOT_CERT_KEY_PATH = "./key/IoT_certificate.pem.crt"
AWS_IOT_CLIENT_ENDPOINT = value["aws_iot_client_endpoint"]
AWS_S3_BUCKET = value['aws_s3_bucket']

config = configparser.ConfigParser()
config.read('aws_credentials.ini')

AWS_ACCESS_KEY_ID = config.get('default', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config.get('default', 'aws_secret_access_key')
AWS_SESSION_TOKEN = config.get('default', 'aws_session_token')