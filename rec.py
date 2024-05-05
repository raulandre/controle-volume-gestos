import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sm, vol

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)
hands_recognizer = mp.solutions.hands.Hands()       
draw = mp.solutions.drawing_utils

x1 = y1 = x2 = y2 = 0

machine = sm.VolumeStateMachine()

cam = cv2.VideoCapture(0)
while True:
    _, img = cam.read()

    if machine.current_state.initial:
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        recognition_result = recognizer.recognize(mp_img)

        if recognition_result.gestures:
            gesture = recognition_result.gestures[0][0].category_name
            if gesture == "Open_Palm":
                machine.send("enter_change_volume")
            if gesture == "Closed_Fist" and machine.current_state.value != "pause_timeout":
                machine.send("enter_pause_timeout")
                vol.send_key(vol.VK_MEDIA_PLAY_PAUSE)
            if gesture == "Thumb_Up" and machine.current_state.value != "pause_timeout":
                machine.send("enter_pause_timeout")
                vol.send_key(vol.VK_MEDIA_NEXT_TRACK)
            if gesture == "Thumb_Down" and machine.current_state.value != "pause_timeout":
                machine.send("enter_pause_timeout")
                vol.send_key(vol.VK_MEDIA_PREV_TRACK)
    else:
        if machine.current_state.value == "changing_volume":
            out = hands_recognizer.process(img)
            hands = out.multi_hand_landmarks
            if hands:
                for hand in hands:
                    draw.draw_landmarks(img, hand)
                    landmarks = hand.landmark

                    for id, landmark in enumerate(landmarks):
                        f_width, f_height, _ = img.shape
                        x = int(landmark.x * f_width)
                        y = int(landmark.y * f_height)
                        if id == 8:
                            x1, y1 = x, y
                        if id == 4:
                            x2, y2 = x, y
                        
            dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
            cv2.putText(img, f"Dist: {dist}", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            if(dist > 50):
                vol.send_key(vol.VK_VOLUME_UP)
            else:
                vol.send_key(vol.VK_VOLUME_DOWN)

    cv2.putText(img, machine.current_state.name, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Controle de volume por gestos", img)

    key = cv2.waitKey(10)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()