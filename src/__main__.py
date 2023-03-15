#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/__main__.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src
Created Date: Thursday, March 9th 2023, 1:32:43 pm

Copyright (c) 2023 ICSLab
'''

from .gesture_recognition.play_game_dinosaur import PlayGameDinosaur

from .speech2image.recording import recording
from .speech2image.speechToViet import SpeechToViet
from .speech2image.vietToEng import VietToEng
from .speech2image.engToImage import EngToImage

class Backend:
    def __init__(self):
        pass

    def __call__(self, mode: int = 0):
        if mode == 1:
            self.__playGameDinosaur()

        elif mode == 2:
            self.__speech2image()

        elif mode == 3:
            self.__styleTransfer()
        
        else:
            return

    def __playGameDinosaur(self):
        self.backend = PlayGameDinosaur()
        self.backend()

    def __speech2image(self):
        self.backend = recording()

    def __styleTransfer(self):
        return

