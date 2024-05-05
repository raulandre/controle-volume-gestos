import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sm

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)
draw = mp.solutions.drawing_utils

machine = sm.VolumeStateMachine()

cam = cv2.VideoCapture(0)
while True:
    _, img = cam.read()
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

    recognition_result = recognizer.recognize(mp_img)
    landmarks = recognition_result.hand_landmarks

    if machine.current_state.initial:
        if recognition_result.gestures:
            gesture = recognition_result.gestures[0][0].category_name
            if gesture == "Open_Palm":
                machine.send("enter_change_volume")

    if machine.current_state.value == "changing_volume":
        # TODO: volume control logic goes here
        pass

    cv2.putText(img, machine.current_state.name, (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Controle de volume por gestos", img)

    key = cv2.waitKey(10)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()