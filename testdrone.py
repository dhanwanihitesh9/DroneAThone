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

# velocity of movement
lrSpeed = 20
fbSpeed = 20
udSpeed = 20
yawSpeed = 20

# Array to define color of ring in the lap possible values are RED & YELLOW
lapColor = ["RED", "RED", "RED", "RED", "RED", "RED", "RED", "RED"]

# Array to define direction of ring in the lap possible values are R, L , M
lapDirection = ["R", "R", "R", "R", "R", "R", "R", "R"]

# check battery
print("battery information :")
print(Drone.get_battery())

# Start the video stream
print("starting streaming")
Drone.streamon()

# function to return co-ordinate of center of ring
def findRingPosition(img):
    # Convert to grayscale
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

        if largest_circle is not None:
            # Draw the largest circle on the image
            return [largest_circle[0], largest_circle[1], largest_circle[1]]
        else:
            print("no circle found")
            return [0, 0, 0]
    else:
        print("no circle found")
    return [0, 0, 0]

# function to identify RED Rings
def findNearestRing(x) :
    print("adjusting altitude")
    if lapColor == "RED":
        print("Ascend as per red ring")
    else:
        print("Ascend as per yellow ring")
    ringFound = False
    while ringFound == False:
        img = Drone.get_frame_read().frame
        ringPosition = findRingPosition(img)
        if ringPosition[0] == 0:
            print("ring not found")
            cv2.putText(img, "Ring not found", (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1, cv2.LINE_AA, False)
            # move in the configured direction
            if lapDirection[x] == "R":
                print("move right")
            elif lapDirection[x] == "L":
                print("move left")
            else:
                print("move back")
        else:
            print("ring found")
            cv2.circle(img, (ringPosition[0], ringPosition[1]), ringPosition[2], (0, 255, 0), 2)
            if ringPosition[0] < width/2-20:
                print("move right")
            elif ringPosition[0] > width/2+20:
                print("move left")
            else:
                print("X axis within range")
                if ringPosition[1] < height/2-20:
                    print("move up")
                elif ringPosition[1] > height/2+20:
                    print("move down")
                else:
                    print("Y Axis within range. Target found")
                    if ringPosition[2] <= 720-100:
                        print("move forward gently")
                    else:
                        print("move through")
                    ringFound = True
        cv2.imshow("Ring Scanner ", img)
        cv2.waitKey(1)
        # identify rings in img
    return

x = 0

while x < len(lapColor):
    findNearestRing(x)
    x = x+1