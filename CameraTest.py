import cv2
from datetime import datetime

camera = cv2.VideoCapture(0)
print("Camera initialised")

camera.set(3, 320)
camera.set(4, 240)

t = datetime.now()

for i in range(10):
    return_value, image = camera.read()
    print(image.shape)
    dt = datetime.now()-t
    print(f"Image {i} read in {dt}s")
    t = datetime.now()
    cv2.imwrite(f"testimage_{i}.png", image)
    dt = datetime.now()-t
    print(f"image {i} written in {dt}s")
    t = datetime.now()
del(camera)