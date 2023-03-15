#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/sota-fusion/ui/backend.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Saturday, March 4th 2023, 9:49:11 pm
Author: tiendat

Copyright (c) 2023 ICSLab
'''
from __future__ import absolute_import, division, print_function

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent)) #sota-fusion folder

from src import Backend

from tkinter import Tk
from .mainWindow import MainWindow


root = Tk()
mainWindow = MainWindow(root)
root.mainloop()
