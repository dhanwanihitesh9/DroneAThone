from djitellopy import tello
from time import sleep
import KeyPressModule as kp
import cv2

kp.init()
Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())

def getKeyBoardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("RIGHT"):
        lr = speed
    elif kp.getKey("LEFT"):
        lr = -speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yve = -speed

    if kp.getKey("q"):
        Drone.land()

    if kp.getKey("e"):
        Drone.takeoff()

    return [lr, fb, ud, yv]

Drone.streamon()

while True:
    img = Drone.get_frame_read().frame
    #img = cv2.resize(img,(360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    values = getKeyBoardInput()
    Drone.send_rc_control(values[0],values[1],values[2],values[3])


