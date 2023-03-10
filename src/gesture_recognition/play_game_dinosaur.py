#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/gesture-recognition/play_game_dinosaur.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/gesture-recognition
Created Date: Saturday, March 4th 2023, 6:06:37 pm

Copyright (c) 2023 ICSLab
'''
from __future__ import absolute_import, division, print_function

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import cv2
import mediapipe as mp
import pyautogui as ui
from selenium import webdriver

from _config import load_config


class PlayGameDinosaur:
    def __init__(self):
        PARENT_PATH = Path(__file__).parent
        self.DRIVER_PATH = PARENT_PATH.joinpath("chromedriver")

        # read config file
        self.config = load_config()

    def __call__(self):
        driver = webdriver.Chrome(self.DRIVER_PATH)
        driver.get(self.config["url-game"])

        self.__play_game()

    def __play_game(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands

        # For webcam input:
        cap = cv2.VideoCapture(1)
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as hands:
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
                        if (
                            int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                                ].y
                                * h
                            )
                            < int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.INDEX_FINGER_DIP
                                ].y
                                * h
                            )
                            or int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP
                                ].y
                                * h
                            )
                            < int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.INDEX_FINGER_DIP
                                ].y
                                * h
                            )
                            or int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.RING_FINGER_TIP
                                ].y
                                * h
                            )
                            < int(
                                hand_landmarks.landmark[
                                    mp_hands.HandLandmark.RING_FINGER_DIP
                                ].y
                                * h
                            )
                        ):
                            ui.press("space")
                        else:
                            pass
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style(),
                        )
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
