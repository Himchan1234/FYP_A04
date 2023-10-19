import os
from Google_Cloud.Vertex_AI.vertex_ai_with_raspberrypi_camera import CaptureImage
from AWS.upload_to_s3_v1 import upload_to_s3
from AWS.ppe import detect_ppe, move_file
from config import AWS_S3_BUCKET

def main():
    try:
        os.system("python ./AWS/sensor_with_IoT_Core_v2.py")
        while True:
            temp_img, img_name = CaptureImage()
            print(temp_img)
            print(img_name)
            S3FilePath = "temp/"
            upload_to_s3(S3FilePath + img_name, temp_img)
            detect_ppe(S3FilePath + img_name)
            person_count, NoHelmaImage = detect_ppe(temp_img, bucket)
            print("Persons detected: " + str(person_count))
            if NoHelmaImage == True:
                move_file(AWS_S3_BUCKET, f"temp/{temp_img}", f"NoHelmaImage/{temp_img}")

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()