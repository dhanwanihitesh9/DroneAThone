from djitellopy import tello
import cv2
from time import sleep
import time
import numpy as np

# initialize and connect with drone
print("Initializing and connecting to drone")
Drone = tello.Tello()
Drone.connect()
Drone.takeoff()
timeLapsed = 0
# while(Drone.get_height()<=40):
#     print(Drone.send_rc_control(0, 0, 50, 0))

# red height
while timeLapsed <= 3 :
    print(Drone.send_rc_control(0,0,50,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25
print(timeLapsed)
print("height : ")
print(Drone.get_height())
timeLapsed = 0

# forward
while timeLapsed <= 8 :
    print(Drone.send_rc_control(0,50,0,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25


# stabilisation
while timeLapsed <= 1 :
    print(Drone.send_rc_control(0,0,0,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25

# Descend
while timeLapsed <= 5 :
    print(Drone.send_rc_control(0,0,-100,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25

# move forward
while timeLapsed <= 2 :
    print(Drone.send_rc_control(0,50,0,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25

# red height
while timeLapsed <= 1.75 :
    print(Drone.send_rc_control(0,0,50,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25
print(timeLapsed)

# move forward
while timeLapsed <= 2 :
    print(Drone.send_rc_control(0,50,0,0))
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25

Drone.land()
print(timeLapsed)
Drone.end()
