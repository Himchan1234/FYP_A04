import boto3

def lambda_handler(event, context):
    client = boto3.client('dynamodb')

    response = client.put_item(
        TableName = 'raspi_Data_v1',
        Item = {
            'timestamp': {'S': event['timestamp']},
            'clientid': {'N': str(event['clientid'])},
            'alcohol value': {'S': event['alcohol value']},
            'gas value': {'S': event['gas value']}
        }
    )

    return 0