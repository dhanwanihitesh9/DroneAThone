import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
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
                cv2.circle(image,(cx,cy), 15 , (255,0,255), cv2.FILLED)

        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    tracker = handTracker()

    while True:
        success,image = cap.read()
        flippedImage = cv2.flip(image, 1)
        flippedImage = tracker.handsFinder(flippedImage)
        lmList = tracker.positionFinder(flippedImage)
        if len(lmList) != 0:
            print(lmList[4])

        cv2.imshow("Video",flippedImage)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()