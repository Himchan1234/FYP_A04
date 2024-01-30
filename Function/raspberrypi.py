from .system import check_system
import datetime, os, time

SYSTEM_TYPE = check_system()

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory) 

image_directory = os.path.join(os.getcwd(), "images")
create_directory_if_not_exists(image_directory)

def CaptureImage():
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(image_directory, f"{timestamp_str}.jpg")
    img_name = f"{timestamp_str}.jpg"

    if check_system == "Linux":
        from picamera2 import Picamera2
        picam2 = Picamera2()
        picam2.start()
        time.sleep(2)
        picam2.close()
        return filepath, img_name

    else:
        return "image/worker.jpg", "worker.jpg"
    