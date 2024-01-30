from Function.raspberrypi import *
from Function.vertex_ai import *

for i in range(10):
    flie_path, img_name = CaptureImage()
    print(flie_path)
    print(img_name)
    question1 = "any person here?"
    question2 = "is person wearing a head hat"
    ans1 = vertax_api(flie_path, question1)
    if ans1 == "yes":
        ans2 = vertax_api(flie_path, question2)
        print(os.path.basename(flie_path), "wear hat", ans2)
    else:
        print(os.path.basename(flie_path), ans1)