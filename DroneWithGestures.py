import cv2
import mediapipe as mp
from djitellopy import tello
from time import sleep

# initialize and connect with drone
print("Initializing and connecting to drone")
Drone = tello.Tello()
Drone.connect()

# Starting activity
print("starting the activity")

# check battery
print("battery information :")
print(Drone.get_battery())

# Define mediapipe settings
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Define the font settings
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.4
font_color = (255, 255, 255)  # Color in BGR format
font_thickness = 2

class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5,modelComplexity=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self,image,draw=True):

        # change hue offset
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        # shift the hue
        # 0 is no change; 0<=huechange<=180
        hueNew = cv2.add(h, 80)

        # combine new hue with s and v
        hsvNew = cv2.merge([hueNew, s, v])

        # convert from HSV to BGR
        convertedImage = cv2.cvtColor(hsvNew, cv2.COLOR_HSV2BGR)

        imageRGB = cv2.cvtColor(convertedImage,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:

                if draw:
                    # self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
                    self.mpDraw.draw_landmarks(
                        image,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
        return image

    def positionFinder(self,image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h,w,c = image.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
            if draw:
                cv2.circle(image,(cx,cy), 5 , (255,0,255), cv2.FILLED)

        return lmlist

# signals
takingOff = 0
landing = 0
def navigateDrone(lmList):

    global takingOff
    global landing

    # sortedListx = evaluateFingers(lmList, "x")
    sortedListy = evaluateFingers(lmList, "y")

    if len(lmList) == 21:

        if sortedListy[0][0] == 4 and takingOff == 0:
            print('taking off')
            takingOff = 1
            landing = 0
            Drone.takeoff()
            # Drone.send_rc_control(0, 0, 25, 0)
            # sleep(1.5)

        elif sortedListy[20][0] == 4 and landing == 0:
            print('landing')
            takingOff = 0
            landing = 1
            Drone.land()

        # elif sortedListy[0][0] == 8 and takingOff == 1:
        #     print('move up / ascend')
        #     Drone.send_rc_control(0,0,50,0)
        #
        # elif sortedListy[20][0] == 8 and takingOff == 1:
        #     print('move down / descend')
        #     Drone.send_rc_control(0,0,50,0)

        else:
            print('no gesture identified')

    else :
        print('No hand signal identified')

    return ""

def evaluateFingers(lmList, axisInfo):

    if axisInfo == 'x':
        itemIndex = 1
    else:
        itemIndex = 2
    # Sort the multi-dimensional array based on the second element of each sub-list
    sorted_array = sorted(lmList, key=lambda x: x[itemIndex])

    return sorted_array
def main():

    # Start the video stream
    print("starting streaming")
    Drone.streamon()

    # cap = cv2.VideoCapture(0)
    tracker = handTracker()

    while True:
        # success,image = cap.read()
        image = Drone.get_frame_read().frame
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        flippedImage = cv2.flip(image, 1)
        flippedImage = tracker.handsFinder(flippedImage)
        lmList = tracker.positionFinder(flippedImage)
        print(lmList)
        if len(lmList) != 0:

            thumbTip = lmList[4]
            cv2.putText(flippedImage, str(lmList[4]), (lmList[4][1],lmList[4][2]), font, font_scale, font_color, font_thickness)

            indexTip = lmList[8]
            cv2.putText(flippedImage, str(lmList[8]), (lmList[8][1],lmList[8][2]), font, font_scale, font_color, font_thickness)

            middleTip = lmList[12]
            cv2.putText(flippedImage, str(lmList[12]), (lmList[12][1],lmList[12][2]), font, font_scale, font_color, font_thickness)

            ringTip = lmList[16]
            cv2.putText(flippedImage, str(lmList[16]), (lmList[16][1],lmList[16][2]), font, font_scale, font_color, font_thickness)

            pinkyTip = lmList[20]
            cv2.putText(flippedImage, str(lmList[20]), (lmList[20][1],lmList[20][2]), font, font_scale, font_color, font_thickness)
        cv2.imshow("Video",flippedImage)
        navigateDrone(lmList)
        sleep(0.25)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()