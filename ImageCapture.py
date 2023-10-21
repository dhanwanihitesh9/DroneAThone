from djitellopy import tello
import cv2
from time import sleep
import time

Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())

Drone.streamon()
while True:
    img = Drone.get_frame_read().frame
    cv2.imshow("Image", img)
    cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
    cv2.waitKey(1)
    sleep(4)