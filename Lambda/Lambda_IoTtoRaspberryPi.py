import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        client = boto3.client('iot-data', region_name='us-east-1')
        
        payload = {
            "speech_message": event['speech_message']
        }
        
        response = client.publish(
            topic='raspberrypi/jsondata',
            qos=0,
            payload=json.dumps(payload)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent to AWS IoT Core!')
        }
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise