#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/daemon/virtual_mouse.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/daemon
Created Date: Tuesday, March 28th 2023, 1:40:34 pm
Author: tiendat

Copyright (c) 2023 Your Company
'''
from __future__ import division, absolute_import

import sys
import copy
import cv2 as cv #type: ignore
import pyautogui #type: ignore
from pathlib import Path
from typing import List, Deque
from loguru import logger  # type: ignore 


sys.path.append(str(Path(__file__).parent))  # daemon folder
from handGesture_recognition import HandGesture_recognition


class VirtualControl(HandGesture_recognition):
    def __init__(self):
        super().__init__()
        self.using_mouse = True
        self.using_keyboard = False
        self.stop_thread = False
    

    def is_HiFive_gesture(self, hand_landmarks: List):
        handLandmarks_forOneHand = hand_landmarks[0] #use only 1 hand for detect

        def comparing_Yvalue(list_indexes: tuple):
            if len(list_indexes) == 4:
                a, b, c, d = list_indexes
                return handLandmarks_forOneHand[a][1] > handLandmarks_forOneHand[b][1] > handLandmarks_forOneHand[c][1] > handLandmarks_forOneHand[d][1]

        if len(handLandmarks_forOneHand) == 21:
            conditions = [
                comparing_Yvalue((1,  2,  3,  4)),
                comparing_Yvalue((5,  6,  7,  8)),
                comparing_Yvalue((9,  10, 11, 12)),
                comparing_Yvalue((13, 14, 15, 16)),
                comparing_Yvalue((17, 18, 19, 20))
            ]

            if all(conditions):
                return True

        return False
    

    def is_click_action(self, hand_landmarks: List) -> bool:

        def checking_validDeque(sequence_deque: Deque) -> bool:
            if len(sequence_deque) > 2:  #for prevent out of index
                if sequence_deque[-1] == [0, 0] and not sequence_deque[-2] == [0, 0]:
                    return True
            
            return False

        #check hi-five gesture
        if self.is_HiFive_gesture(hand_landmarks=hand_landmarks):
            #TODO: change to other method
            first_key = next(iter(self.point_history))

            #check valid deque
            if checking_validDeque(sequence_deque=self.point_history[first_key]):
                return True
        
        return False
    

    def clicking_mouse(self, 
                       width_ratio: float, 
                       height_ratio: float, 
                       hand_landmarks: List):        

        if self.is_click_action(hand_landmarks=hand_landmarks):
            first_key = next(iter(self.point_history))
            if len(self.point_history[first_key]) == 0: #for prevent out of index
                return
            
            pointX, pointY = self.point_history[first_key][self.history_length - 2] #before hi-five gestures
            newX = round(pointX * width_ratio)
            newY = round(pointY * height_ratio)
            pyautogui.click(newX, newY)
            
            logger.debug("Clicked")

    
    def moving_mouse(self, 
                    width_ratio: float, 
                    height_ratio: float):
        first_key = next(iter(self.point_history))
        pointX, pointY = self.point_history[first_key][-1]
        
        if pointX == 0 and pointY == 0: #for prevent move to edge of screen
            return
        
        newX = round(pointX * width_ratio)
        newY = round(pointY * height_ratio)

        pyautogui.moveTo(newX, newY)

        
    def run(self):
        #setup camera ###############################################################
        self.cap = cv.VideoCapture(self.device)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        
        #params #######################################################################
        mode = 0
        auto = False
        prev_number = -1
        image = None

        screenWidth, screenHeight = pyautogui.size()
        is_hiFiveGesture_happened = False
        previous_hiFiveGesture_status = False
        width_ratio = float(screenWidth / self.width)
        height_ratio = float(screenHeight / self.height)
        window_name = 'Hand Gesture Recognition'

        while not self.stop_thread:
            fps = self.cvFpsCalc.get()

            key = cv.waitKey(1) if not self.use_static_image_mode \
                                else cv.waitKey(0) if image is not None and self.use_static_image_mode \
                                                   else cv.waitKey(1)
            if key == 27:  # ESC
                break
            number, mode, auto, prev_number = self._select_mode(key, mode, auto, prev_number)

            # camera capture #####################################################
            ret, image = self.cap.read()
            if not ret:
                break

            image = image if self.disable_image_flip else cv.flip(image, 1) # mirror display
            debug_image = copy.deepcopy(image)

            # detection #################################################
            cropted_rotated_hands_images, rects, palm_trackid_box_x1y1s, not_rotate_rects= self._palm_detection(image=image, debug_image=debug_image)

            hand_landmarks = self._hand_landmark(cropted_rotated_hands_images=cropted_rotated_hands_images,
                                rects=rects,
                                debug_image=debug_image,
                                palm_trackid_box_x1y1s=palm_trackid_box_x1y1s,
                                not_rotate_rects=not_rotate_rects)
            
            debug_image = self._draw_point_history(debug_image, self.point_history)
            debug_image = self._draw_info(debug_image, fps, mode, number, auto)

            if hand_landmarks is not None and len(hand_landmarks) > 0:
                previous_hiFiveGesture_status = is_hiFiveGesture_happened
                is_hiFiveGesture_happened = self.is_HiFive_gesture(hand_landmarks=hand_landmarks)

                #control mouse
                if self.using_mouse:
                    if len(self.point_history) > 0: #key-point gesture
                        if not is_hiFiveGesture_happened: #prevent mouse move when use hiFiveGesture 
                            self.moving_mouse(width_ratio=width_ratio, height_ratio=height_ratio)

                        if not previous_hiFiveGesture_status and is_hiFiveGesture_happened: #prevent duplicate click
                            logger.info("Virtual clicking...")
                            self.clicking_mouse(width_ratio=width_ratio,
                                                height_ratio=height_ratio,
                                                hand_landmarks=hand_landmarks) 
            
                #control keyboard
                if self.using_keyboard:
                    if is_hiFiveGesture_happened:
                        pyautogui.press('backspace')
                        logger.debug("Virtual backspace")
            
            # screen showing #############################################################
            cv.namedWindow(window_name)
            cv.moveWindow(window_name, 0, 0)
            cv.imshow(window_name, debug_image)
            
        if self.cap:
            self.cap.release()
        cv.destroyAllWindows()

    def on_exit(self):
        self.stop_thread = True
        self.cap.release()
        cv.destroyAllWindows()

if __name__ == '__main__':
    virtualControl = VirtualControl()
    virtualControl.run() 
