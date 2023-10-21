from djitellopy import tello
import cv2
from time import sleep
import time
import numpy as np

# initialize and connect with drone
print("Initializing and connecting to drone")
Drone = tello.Tello()
Drone.connect()

# Starting activity
print("starting the activity")

# image resolution
width = 960
height = 720

# check battery
print("battery information :")
print(Drone.get_battery())

def findRingPosition(img):
    # Convert to grayscale
    speed = 30
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1,  # Inverse ratio of accumulator resolution
        minDist=110,  # Minimum distance between detected centers
        param1=100,  # Upper threshold for the internal Canny edge detector
        param2=80,  # Threshold for center detection
        minRadius=10,  # Minimum radius
        maxRadius=1000  # Maximum radius
    )
    print("identify circles")
    if circles is not None:
        circles = np.uint16(np.around(circles))
        largest_circle = None
        largest_radius = 0

        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            radius = circle[2]

            # Check if the current circle has a larger radius
            if radius > largest_radius:
                largest_radius = radius
                largest_circle = circle
        print("identify largest circle")
        if largest_circle is not None:
            print("largest circle found")
            print(largest_circle)
            # Draw the largest circle on the image
            cv2.circle(img, (largest_circle[0], largest_circle[1]), largest_circle[2], (0, 255, 0), 2)
            cv2.circle(img, (largest_circle[0], largest_circle[1]), 2, (0, 255, 0), 2)

            if largest_circle[0] >= 380 and largest_circle[0] <= 580:
                print("X in range")
                if largest_circle[1] >= 260 and largest_circle[1] <= 460:

                    # verify proximity
                    if(largest_circle[2] >= 300) :
                        print("move forward - ring is near")
                        cv2.putText(img, 'Ring Found - move forward Ring is near '+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 1, cv2.LINE_AA, False)
                        # move forward
                        while timeLapsed <= 2:
                            print(Drone.send_rc_control(0, 50, 0, 0))
                            sleep(0.25)
                            timeLapsed = timeLapsed + 0.25
                        return[0,0,0,0]
                    else:
                        print("move forward")
                        cv2.putText(img, 'Ring Found - move forward '+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 1, cv2.LINE_AA, False)
                        return [0, speed, 0, 0]
                else:
                    if largest_circle[1] > 460:
                        print("move down")
                        cv2.putText(img, "Ring Found - move down "+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 1, cv2.LINE_AA, False)
                        return [0, 0, -1*speed, 0]
                    else:
                        print("move up")
                        cv2.putText(img, "Ring Found - move up "+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 255, 0), 1, cv2.LINE_AA, False)
                        return [0, 0, speed, 0]
            else:
                print("x co-ordinate not in range")
                if largest_circle[0] < 380:
                    print("move left")
                    cv2.putText(img, "Ring Found - move left "+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [-1*speed, 0, 0, 0]
                else:
                    print("move right")
                    cv2.putText(img, "Ring Found - move right "+str(largest_circle[2]), (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [speed, 0, 0, 0]
        else:
            print("no largest circle found")
            cv2.putText(img, "Ring not found - move back", (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1, cv2.LINE_AA, False)
            return [0, -1*speed, 0, 0]
    else:
        print("no circle found")
        cv2.putText(img, "Ring not found - move back", (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 1, cv2.LINE_AA, False)
    return [0, -1*speed, 0, 0]

# Start the video stream
print("starting streaming")
Drone.streamon()
sleep(1)

# step 1 Take off
Drone.takeoff()

# step 2 Ascend to a height
timeLapsed = 0
# # while(Drone.get_height()<=40):
# #     print(Drone.send_rc_control(0, 0, 50, 0))
while timeLapsed <= 1 :
    Drone.send_rc_control(0,0,50,0)
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25
#
# # step 3 Land
# Drone.land()

x=0
while True:

    img = Drone.get_frame_read().frame
    cv2.waitKey(1)
    values = findRingPosition(img)
    cv2.imshow("Circle Detection", img)
    cv2.putText(img, "Speed "+str(values), (00, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.imwrite(f'Resources/Images/circle/Circle{str(x)}.jpg', img)
    print(values)
    Drone.send_rc_control(values[0],values[1],values[2],values[3])
    x=x+1
    # sleep(0.1) worked fine
    sleep(0.05)