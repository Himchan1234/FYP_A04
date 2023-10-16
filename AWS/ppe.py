# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import sys
sys.path.append("")
from config import AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, \
    AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN

def detect_ppe(photo, bucket):

    session = boto3.Session(
        region_name="us-east-1",
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        aws_session_token = AWS_SESSION_TOKEN
        )

    client = session.client('rekognition')

    response = client.detect_protective_equipment(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                                  SummarizationAttributes={'MinConfidence': 80,
                                                                           'RequiredEquipmentTypes': ['FACE_COVER',
                                                                                                      'HAND_COVER',
                                                                                                      'HEAD_COVER']})

    print('Detected PPE for people in image ' + photo)
    print('\nDetected people\n---------------')
    for person in response['Persons']:

        print('Person ID: ' + str(person['Id']))
        print('Body Parts\n----------')
        body_parts = person['BodyParts']
        if len(body_parts) == 0:
            print('No body parts found')
        else:
            for body_part in body_parts:
                print('\t' + body_part['Name'] + '\n\t\tConfidence: ' + str(body_part['Confidence']))
                print('\n\t\tDetected PPE\n\t\t------------')
                ppe_items = body_part['EquipmentDetections']
                if len(ppe_items) == 0:
                    print('\t\tNo PPE detected on ' + body_part['Name'])
                else:
                    for ppe_item in ppe_items:
                        print('\t\t' + ppe_item['Type'] + '\n\t\t\tConfidence: ' + str(ppe_item['Confidence']))
                        print('\t\tCovers body part: ' + str(
                            ppe_item['CoversBodyPart']['Value']) + '\n\t\t\tConfidence: ' + str(
                            ppe_item['CoversBodyPart']['Confidence']))
                        print('\t\tBounding Box:')
                        print('\t\t\tTop: ' + str(ppe_item['BoundingBox']['Top']))
                        print('\t\t\tLeft: ' + str(ppe_item['BoundingBox']['Left']))
                        print('\t\t\tWidth: ' + str(ppe_item['BoundingBox']['Width']))
                        print('\t\t\tHeight: ' + str(ppe_item['BoundingBox']['Height']))
                        print('\t\t\tConfidence: ' + str(ppe_item['Confidence']))
            print()
        print()

    print('Person ID Summary\n----------------')
    display_summary('With required equipment', response['Summary']['PersonsWithRequiredEquipment'])
    display_summary('Without required equipment', response['Summary']['PersonsWithoutRequiredEquipment'])
    display_summary('Indeterminate', response['Summary']['PersonsIndeterminate'])

    if len(response['Summary']['PersonsWithoutRequiredEquipment']) == 0:
        IsNoHelma = False
    else:
        IsNoHelma = True
    print()
    return len(response['Persons']), IsNoHelma

# Display summary information for supplied summary.
def display_summary(summary_type, summary):
    print(summary_type + '\n\tIDs: ', end='')
    if (len(summary) == 0):
        print('None')
    else:
        for num, id in enumerate(summary, start=0):
            if num == len(summary) - 1:
                print(id)
            else:
                print(str(id) + ', ', end='')

def move_file(bucket_name, source_key, destination_key):
    
    session = boto3.Session(
        region_name="us-east-1",
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        aws_session_token = AWS_SESSION_TOKEN
        )
    s3_client = session.client('s3')

    # Copy the object to the new location
    copy_source = {
        'Bucket': bucket_name,
        'Key': source_key
    }
    s3_client.copy_object(
        CopySource=copy_source,
        Bucket=bucket_name,
        Key=destination_key
    )

    # Delete the object from the old location
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=source_key
    )

    print(f'Moved {bucket_name}/{source_key} to {bucket_name}/{destination_key}')

def main():
    photo = '20231016.jpg'
    photo_path = f"temp/{photo}"
    bucket = AWS_S3_BUCKET
    person_count, NoHelmaImage = detect_ppe(photo_path, bucket)
    print("Persons detected: " + str(person_count))
    print(NoHelmaImage)
    if NoHelmaImage == True:
        move_file(bucket, f"temp/{photo}", f"NoHelmaImage/{photo}")


if __name__ == "__main__":
    main()
