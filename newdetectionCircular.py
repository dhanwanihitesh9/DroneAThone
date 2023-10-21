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

centerX = int(width / 2)
centerY = int(height / 2)

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
            radiusSquare = ((largest_circle[0]-centerX)*(largest_circle[0]-centerX) +
                            (largest_circle[1]-centerY)*(largest_circle[1]-centerY))
            angle = 0
            if radiusSquare <= 40000:
                if largest_circle[2] >= 400:
                    # move forward
                    timeLapsed = 0
                    while timeLapsed <= 1:
                        print(Drone.send_rc_control(0, 50, 0, 0))
                        sleep(0.25)
                        timeLapsed = timeLapsed + 0.25
                    Drone.land();
                else:
                    print("move forward")
                    cv2.putText(img, 'Ring Found - move forward ' + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [0, speed, 0, 0]
            else:
                # if circle center in quadrant A
                if (largest_circle[0]-centerX) > 0 and (largest_circle[1]-centerY > 0):
                    print('section A')
                    cv2.putText(img, "Ring Found - Section A " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(largest_circle[1]-centerY, (largest_circle[0]-centerX))
                    print(angle)
                    print(np.cos(angle))
                    print(np.sin(angle))
                    xSpeed = 1*np.cos(angle)*speed
                    ySpeed = -1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant B
                elif (largest_circle[0]-centerX) > 0 and (largest_circle[1]-centerY < 0):
                    print('section B')
                    cv2.putText(img, "Ring Found - Section B " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(centerY-largest_circle[1], (largest_circle[0]-centerX))
                    print(angle)
                    print(np.cos(angle))
                    print(np.sin(angle))
                    xSpeed = 1*np.cos(angle)*speed
                    ySpeed = 1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant C
                elif (largest_circle[0]-centerX) < 0 and (largest_circle[1]-centerY < 0):
                    print('section C')
                    cv2.putText(img, "Ring Found - Section C " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(centerY-largest_circle[1], (centerX-largest_circle[0]))
                    print(angle)
                    print(np.cos(angle))
                    print(np.sin(angle))
                    xSpeed = -1*np.cos(angle)*speed
                    ySpeed = 1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                # if circle center in quadrant D
                elif (largest_circle[0]-centerX) < 0 and (largest_circle[1]-centerY > 0):
                    print('section D')
                    cv2.putText(img, "Ring Found - Section D " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    angle = np.arctan2(largest_circle[1]-centerY, (centerX-largest_circle[0]))
                    print(angle)
                    print(np.cos(angle))
                    print(np.sin(angle))
                    xSpeed = -1*np.cos(angle)*speed
                    ySpeed = -1*np.sin(angle)*speed
                    return[int(xSpeed),0,int(ySpeed),0]

                else:
                    print('section Unidentified')
                    cv2.putText(img, "Ring Found - Section unidentified " + str(largest_circle[2]), (00, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 255, 0), 1, cv2.LINE_AA, False)
                    return [0, -1*speed, 0, 0]
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
img = Drone.get_frame_read().frame
sleep(1)

# step 1 Take off
Drone.takeoff()

# step 2 Ascend to a height
timeLapsed = 0
# # # while(Drone.get_height()<=40):
# # #     print(Drone.send_rc_control(0, 0, 50, 0))
while timeLapsed <= 1:
    Drone.send_rc_control(0,0,50,0)
    sleep(0.25)
    timeLapsed = timeLapsed + 0.25
#
# # # step 3 Land
# # Drone.land()

x = 0
while True:

    img = Drone.get_frame_read().frame
    cv2.waitKey(1)
    values = findRingPosition(img)
    cv2.circle(img, (int(width/2), int(height/2)), int(width/2), (0, 255, 0), 2)
    cv2.circle(img, (int(width / 2), int(height / 2)), int(height / 2), (0, 255, 0), 2)
    cv2.circle(img, (int(width / 2), int(height / 2)), 200, (0, 255, 0), 2)
    cv2.putText(img, "Speed "+str(values), (00, 20), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255), 1, cv2.LINE_AA, False)
    cv2.imshow("Circle Detection", img)
    cv2.imwrite(f'Resources/Images/circle/Circle{str(x)}.jpg', img)
    print(values)
    Drone.send_rc_control(values[0],values[1],values[2],values[3])
    x = x + 1
    sleep(0.04)
    # sleep(0.05)

