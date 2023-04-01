#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/daemon/virtual_mouse.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/daemon
Created Date: Tuesday, March 28th 2023, 1:40:34 pm
Author: tiendat

Copyright (c) 2023 Your Company
'''
from __future__ import division, absolute_import

import copy
import cv2 as cv

from handGesture_recognition import HandGesture_regcognition


class VirtualControlTask(HandGesture_regcognition):
    def __init__(self):
        super().__init__()
    
    def is_pressKeyboard_action(self) -> bool:
        return False
    
    def is_click_action(self) -> bool:
        return False
    
    def run(self):
        #setup camera ###############################################################
        cap = cv.VideoCapture(self.device)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)
        # cap_fps = cap.get(cv.CAP_PROP_FPS)
        
        #  #######################################################################
        mode = 0

        auto = False
        prev_number = -1
        image = None

        while True:
            fps = self.cvFpsCalc.get()

            key = cv.waitKey(1) if not self.use_static_image_mode \
                                else cv.waitKey(0) if image is not None and self.use_static_image_mode \
                                                   else cv.waitKey(1)
            if key == 27:  # ESC
                break
            number, mode, auto, prev_number = self._select_mode(key, mode, auto, prev_number)

            # camera capture #####################################################
            ret, image = cap.read()
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
                                not_rotate_rects=not_rotate_rects,
                                #  number=number,
                                #  mode=mode
                                )
            
            debug_image = self._draw_point_history(debug_image, self.point_history)
            debug_image = self._draw_info(debug_image, fps, mode, number, auto)

            # print(self.point_history)
            # print(hand_landmarks)
            
            # screen showing #############################################################
            cv.imshow('Hand Gesture Recognition', debug_image)

        if cap:
            cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    virtualControlTask = VirtualControlTask()
    virtualControlTask.run() 
