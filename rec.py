import cv2
import mediapipe as mp

hands = mp.solutions.hands.Hands()
draw = mp.solutions.drawing_utils

cam = cv2.VideoCapture(0)
while True:
    _, img = cam.read()

    out = hands.process(img)
    landmarks = out.multi_hand_landmarks
    if landmarks:
      for lm in landmarks:
        draw.draw_landmarks(img, lm)

    cv2.imshow("Controle de volume por gestos", img)

    key = cv2.waitKey(10)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()