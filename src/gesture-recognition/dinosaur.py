import selenium
import mediapipe as mp
import cv2
# from pynput.keyboard import Key, Controller
import pyautogui as ui
from selenium import webdriver

# def detectHand(img):
#     mpHands = mp.solutions.hands
#     hands = mpHands.Hands(mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5)
#     mpDraw = mp.solutions.drawing_utils

#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(img)

#     if results.multi_hand_landmarks:
#         for i in results.multi_hand_landmarks:
#             mpDraw.draw_landmarks(img, i, mpHands.HAND_CONNECTIONS)
    
#     return img
path = 'chromedriver'
driver = webdriver.Chrome(path)
driver.get('https://offline-dino-game.firebaseapp.com/')
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# For webcam input:
cap = cv2.VideoCapture(1)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    h, w, _ = image.shape
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        if (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * h) < int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * h) 
            or int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * h) < int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * h) 
            or int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * h) < int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * h)):
          ui.press('space')
        else:
          pass
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
