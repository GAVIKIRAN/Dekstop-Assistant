import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np
import time
import mouse
from screeninfo import get_monitors

frameR = 100
cam_w, cam_h = 640, 480

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

cap.set(3, cam_w)
cap.set(4, cam_h)

detector = HandDetector(detectionCon=0.9, maxHands=1)

monitor = get_monitors()[0]  # Assuming we have one monitor
screen_width, screen_height = monitor.width, monitor.height
print(f"Screen resolution: {screen_width}x{screen_height}")

def hand_tracking():
    """Perform hand gesture operations."""
    last_left_click = 0
    last_right_click = 0
    last_double_click = 0
    delay_time = 1
    double_delay_time = 2
    is_clicking = False
    last_vol_dist = None
    volume_threshold = 50

    while True:
        success, img = cap.read()

        if not success:
            print("Failed to grab frame")
            break

        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        cv2.rectangle(img, (frameR, frameR), (cam_w - frameR, cam_h - frameR), (255, 0, 255), 2)

        if hands:
            lmlist = hands[0]['lmList']

            if len(lmlist) > 12:
                ind_x, ind_y = lmlist[8][0], lmlist[8][1]
                mid_x, mid_y = lmlist[12][0], lmlist[12][1]
                thumb_x, thumb_y = lmlist[4][0], lmlist[4][1]
                pinky_x, pinky_y = lmlist[20][0], lmlist[20][1]

                dist = np.linalg.norm(np.array([ind_x, ind_y]) - np.array([mid_x, mid_y]))
                fingers = detector.fingersUp(hands[0])

                if fingers == [0, 1, 1, 1, 0]:
                    pyautogui.press("volumeup")
                    print("Volume Up")
                    last_vol_dist = time.time()

                thumb_index_dist = np.linalg.norm(np.array([thumb_x, thumb_y]) - np.array([ind_x, ind_y]))

                if fingers == [0, 0, 1, 1, 1] and thumb_index_dist < 30:
                    pyautogui.press("volumedown")
                    print("Volume Down")
                    last_vol_dist = time.time()

                if not is_clicking:
                    if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 1:
                        conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0, screen_width)))
                        conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0, screen_height)))
                        mouse.move(conv_x, conv_y)

                    if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                        if abs(ind_x - mid_x) < 25 and fingers[4] == 0 and time.time() - last_left_click > delay_time:
                            mouse.click(button="left")
                            last_left_click = time.time()
                            is_clicking = True
                            time.sleep(0.5)
                            is_clicking = False

                    if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                        if abs(ind_x - mid_x) < 25 and fingers[4] == 1 and time.time() - last_right_click > delay_time:
                            mouse.click(button="right")
                            last_right_click = time.time()
                            is_clicking = True
                            time.sleep(0.5)
                            is_clicking = False

                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 0:
                    if abs(ind_x - mid_x) < 25:
                        mouse.wheel(delta=-1)
                        print("Scrolling Down")

                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0 and fingers[4] == 1:
                    if abs(ind_x - mid_x) < 25:
                        mouse.wheel(delta=1)
                        print("Scrolling Up")

        cv2.imshow("Hand Gesture Control", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    hand_tracking()
