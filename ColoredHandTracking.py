import cv2
import mediapipe as mp
from time import sleep



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

window_title = 'Recognition result'
trackbar_title = 'Hue offset'


class HueHelper:
    def __init__(self):
        self.mp_hands = mp_hands.Hands(static_image_mode=True,
                                       max_num_hands=2,
                                       min_detection_confidence=0.5)
        self.img_bgr = None

    def apply_hue_offset(self, image, hue_offset):  # 0 is no change; 0<=huechange<=180
        # convert img to hsv
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h = img_hsv[:, :, 0]
        s = img_hsv[:, :, 1]
        v = img_hsv[:, :, 2]
        # shift the hue
        # cv2 will clip automatically to avoid color wrap-around
        img_hsv = cv2.add(h, hue_offset)
        # combine new hue with s and v
        img_hsv = cv2.merge([img_hsv, s, v])
        # convert from HSV to BGR
        return cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)

    def on_trackbar_change(self, trackbar_hue_offset):
        img_bgr_modified = self.recognize(self.img_bgr.copy(), trackbar_hue_offset)
        cv2.imshow(window_title, img_bgr_modified)

    def recognize(self, img_bgr, hue_offset):
        img_bgr = self.apply_hue_offset(img_bgr, hue_offset)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img_bgr,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        else:
            print('no hands were found')
        return img_bgr

    def run(self, image):
        self.img_bgr = image
        if self.img_bgr is None: print('Image was not found!')
        self.on_trackbar_change(0)
        # Hue range is 0-179: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
        cv2.createTrackbar(trackbar_title, window_title, 0, 179, self.on_trackbar_change)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    sleep(5);
    while True:
        success,image = cap.read()
        h = HueHelper()
        h.run(image)

if __name__ == "__main__":
    main()