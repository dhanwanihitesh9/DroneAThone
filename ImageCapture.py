from djitellopy import tello
import cv2

Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())

Drone.streamon()
while True:
    img = Drone.get_frame_read().frame
    img = cv2.resize(img,(360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)


