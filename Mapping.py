from djitellopy import tello
from time import sleep
import KeyPressModule as kp
import cv2
import time
import numpy as np
import math
##Parameters
fSpeed = 117/10 #Forward speed in cm/s
aSpeed = 360/10 # Angular Speed / s
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval

##########
x, y = 500, 500
a = 0
yaw = 0

kp.init()
Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())
#Drone.enable_mission_pads()

def getKeyBoardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    d=0
    global a, yaw
    global x, y

    if kp.getKey("RIGHT"):
        lr = speed
        d = dInterval
        a = 180

    elif kp.getKey("LEFT"):
        lr = -speed
        d = -dInterval
        a = -180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -speed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = speed
        yaw += aInterval

    if kp.getKey("q"):
        Drone.land()

    if kp.getKey("e"):
        Drone.takeoff()

    a += yaw
    x += int(d+math.cos(math.radians(a)))
    y += int(d + math.sin(math.radians(a)))

    if kp.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        sleep(1)

    return [lr, fb, ud, yv, x, y]

def drawPoints(img1, x, y ):
    cv2.circle(img1,(x,y), 5, (0,0,255))

Drone.streamon()

img1 = np.zeros((1000, 1000, 3), np.uint8)
while True:
    img = Drone.get_frame_read().frame
    #img = cv2.resize(img,(360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    values = getKeyBoardInput()
    Drone.send_rc_control(values[0],values[1],values[2],values[3])
    drawPoints(img1,values[4], values[5] )
    cv2.imshow("Output", img1)
    cv2.waitKey(1)


