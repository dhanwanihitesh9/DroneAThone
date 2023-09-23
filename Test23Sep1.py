from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 25


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Create pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 50)

    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                frame_read.stop()
                break
            self.screen.fill([0, 0, 0])

            # processing
            # notes: frame is frame_read.frame

            # print(type(frame_read.frame))
            # cv2.imshow('Video View', frame_read.frame)

            net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
            # print(OPENCV_DNN_CUDA)
            # net.setPreferableTarget(OPENCV_DNN_CUDA)
            classes = []
            with open("coco.names", "r") as f:
                classes = [line.strip() for line in f.readlines()]

            layer_names = net.getLayerNames()
            outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            colors = np.random.uniform(0, 255, size=(len(classes), 3))
            font = cv2.FONT_HERSHEY_PLAIN

            height, width, channels = frame_read.frame.shape
            blob = cv2.dnn.blobFromImage(frame_read.frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

            net.setInput(blob)
            outs = net.forward(outputlayers)

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.3:
                        # onject detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                        # rectangle co-ordinaters
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                        boxes.append([x, y, w, h])  # put all rectangle areas
                        confidences.append(
                            float(confidence))  # how confidence was that object detected and show that percentage
                        class_ids.append(class_id)  # name of the object tha was detected

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    cv2.rectangle(frame_read.frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame_read.frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1,
                                (255, 255, 255), 2)

            # elapsed_time = time.time() - starting_time
            # fps=frame_id/elapsed_time
            # cv2.putText(frame_read.frame,"FPS:"+str(round(fps,2)),(10,50),font,2,(0,0,0),1)

            # cv2.imshow("Image",frame_read.frame)
            # key = cv2.waitKey(1) #wait 1ms the loop will start again and we will process the next frame

            # if key == 27: #esc key stops the process
            #     break;

            # cap.release()
            # cv2.destroyAllWindows()

            # processing ends!
            frame = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)

            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()