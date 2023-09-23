from djitellopy import tello
from time import sleep

Drone = tello.Tello()
Drone.connect()
print(Drone.get_battery())
Drone.takeoff()
Drone.send_rc_control(0,50,0,0)
sleep(1)
Drone.send_rc_control(0,0,0,0)
Drone.land()