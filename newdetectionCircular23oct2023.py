from djitellopy import tello
import cv2
from time import sleep
import time
import numpy as np

print("Initializing Path and variables")

circuit = ["O", "Y", "R", "Y", "R", "Y", "R", "Y"]
mileStone = ["N", "N", "N", "N", "N", "N", "N", "N"]
directionGuide = ["M", "M", "M", "M", "M", "M", "M", "M"]
targetAchieved = 0

# initialize and connect with drone
print("Initializing and connecting to drone")
Drone = tello.Tello()
Drone.connect()

# Starting activity
print("starting the activity")

# image resolution
width = 960
height = 720

centerX = int(width / 2)
centerY = int(height / 2)

# check battery
print("battery information :")
print(Drone.get_battery())


def findRingPosition(img):

    speed = 30
    global targetAchieved
    global mileStone
    # image processing for red circles
    if circuit[targetAchieved] == 'R':
        imageHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([30, 150, 50], dtype="uint8")
        upper = np.array([255, 255, 180], dtype="uint8")
        gray = cv2.inRange(imageHSV, lower, upper)

    # image processing for yellow circles
    elif circuit[targetAchieved] == 'Y':
        imageHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([22, 93, 0], dtype="uint8")
        upper = np.array([45, 255, 255], dtype="uint8")
        gray = cv2.inRange(imageHSV, lower, upper)

    # image processing for others
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # identify circles
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
            cv2.circle(img, (largest_circle[0], largest_circle[1]), largest_circle[2], (0, 255, 0), 5)
            cv2.circle(img, (largest_circle[0], largest_circle[1]), 5, (0, 255, 0), 5)

            radiusSquare = ((largest_circle[0]-centerX)*(largest_circle[0]-centerX) +
                            (largest_circle[1]-centerY)*(largest_circle[1]-centerY))
            angle = 0

            # if distance between center of identified circle is within 200px from center of frame
            if radiusSquare <= 40000:

                # if identified circle engulfs the benchmark circle and has radius twice the benchmark circle radius
                if largest_circle[2] >= 350: # 400

                    # move through the target
                    timeLapsed = 0
                    while timeLapsed <= 1.5:
                        Drone.send_rc_control(0, 50, 0, 0)
                        sleep(0.25)
                        timeLapsed = timeLapsed + 0.25
                    mileStone[targetAchieved] = "Y"
                    targetAchieved = targetAchieved + 1

                # moving forward in the line
                else:
                    cv2.putText(img, 'Ring Found - move forward ' + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [0, speed, 0, 0]

            else:
                # if circle center in quadrant A
                if (largest_circle[0]-centerX) > 0 and (largest_circle[1]-centerY > 0):
                    cv2.putText(img, "Ring Found - Section A " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(largest_circle[1]-centerY, (largest_circle[0]-centerX))
                    xSpeed = 1*np.cos(angle)*speed
                    ySpeed = -1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant B
                elif (largest_circle[0]-centerX) > 0 and (largest_circle[1]-centerY < 0):
                    cv2.putText(img, "Ring Found - Section B " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(centerY-largest_circle[1], (largest_circle[0]-centerX))
                    xSpeed = 1*np.cos(angle)*speed
                    ySpeed = 1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant C
                elif (largest_circle[0]-centerX) < 0 and (largest_circle[1]-centerY < 0):
                    cv2.putText(img, "Ring Found - Section C " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(centerY-largest_circle[1], (centerX-largest_circle[0]))
                    xSpeed = -1*np.cos(angle)*speed
                    ySpeed = 1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant D
                elif (largest_circle[0]-centerX) < 0 and (largest_circle[1]-centerY > 0):
                    cv2.putText(img, "Ring Found - Section D " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(largest_circle[1]-centerY, (centerX-largest_circle[0]))
                    xSpeed = -1*np.cos(angle)*speed
                    ySpeed = -1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                else:
                    cv2.putText(img, "Ring Found - Section unidentified " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [0, -1*speed, 0, 0]
        else:
            cv2.putText(img, "Largest circle not found - move back", (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1, cv2.LINE_AA, False)
            return [0, -1*speed, 0, 0]
    else:
        cv2.putText(img, "Ring not found - move back", (00, 185), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 1, cv2.LINE_AA, False)
    return [0, -1*speed, 0, 0]

# Start the video stream
print("starting streaming")
Drone.streamon()
img = Drone.get_frame_read().frame

# step 1 Take off
Drone.takeoff()

# step 2 Ascend to a height
timeLapsed = 0
targetTime = 2 if (circuit[targetAchieved] == 'R') else 1
while timeLapsed <= targetTime:
    Drone.send_rc_control(0,0,50,0)
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25

# Step 3 - 1st target
x = 0
while mileStone[0] == 'N':

    img = Drone.get_frame_read().frame
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.waitKey(1)
    values = findRingPosition(img)

    # Draw benchmark circles
    cv2.imwrite(f'Resources/Images/circle/CircleOriginal{str(x)}.jpg', img)
    cv2.circle(img, (int(width/2), int(height/2)), int(width/2), (0, 255, 0), 2)
    cv2.circle(img, (int(width / 2), int(height / 2)), int(height / 2), (0, 255, 0), 2)
    cv2.circle(img, (int(width / 2), int(height / 2)), 200, (0, 255, 0), 2)
    cv2.circle(img, (int(width / 2), int(height / 2)), 100, (0, 255, 0), 2)
    cv2.line(img, (centerX,0), (centerX,centerY*2), (0, 255, 0), 2)
    cv2.line(img, (0,centerY), (2*centerX,centerY), (0, 255, 0), 2)
    cv2.putText(img, "Identifying Target:"+str(targetAchieved)+" - Speed "+str(values), (00, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.imshow("Circle Detection", img)
    cv2.imwrite(f'Resources/Images/circle/Circle{str(x)}.jpg', img)

    Drone.send_rc_control(values[0], values[1], values[2], values[3])
    x = x + 1
    sleep(0.04)
    # sleep(0.05)

Drone.land()

