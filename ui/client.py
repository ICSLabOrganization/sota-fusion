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

import queue
import logging
import threading
from tkinter import Tk

# from src import PlayGameDinosaur, \
#                 recording, \
#                 SpeechToViet, \
#                 VietToEng, \
#                 EngToImage


from mainWindow import MainWindow
from speech2image import Speech2Image_window
from style_transfer import StyleTransfer_window

#create a long-term running task queue for output
result_queue = queue.Queue()


class Client(MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.binding_button_click()
        
    def binding_button_click(self):
        self.canvas.tag_bind(
            self.btn_playDinosaurGame, "<Button-1>", lambda _: self.get_click_event(ID=1)
        )

        self.canvas.tag_bind(
            self.btn_styleTransfer, "<Button-1>", lambda _: self.get_click_event(ID=2)
        )

        self.canvas.tag_bind(
            self.btn_speech2image, "<Button-1>", lambda _: self.get_click_event(ID=3)
        )

    # the function to call when button clicked
    def get_click_event(self, ID: int, event=None):
        self.window.withdraw()
        #open another window
        if ID == 2: #style transfer button
            self.sub_window = StyleTransfer_extend(self.window)

        elif ID == 3: #speech2image button
            self.sub_window = Speech2Image_extend(self.window)
            
        print(ID)
        

class StyleTransfer_extend(StyleTransfer_window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binding_button_click()
        
    def binding_button_click(self):
        # binding event for button
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=0, event=str(event)),
        )

        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=1, event=str(event)),
        )

        self.canvas.tag_bind(
            self.image_content_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=2, event=str(event)),
        )

        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=3, event=str(event)),
        )

    # the function to call when button clicked
    def get_click_event(self, ID: int, event=None):
        if ID == 0:
            self.window.destroy()
            # restore the main window
            self.master.deiconify()

        elif ID == 1:
            self.canvas.itemconfig(
                self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
            )
            # unhidden loadding animation
            self.canvas.itemconfig(
                self.loadingAnimation_canvas, state="normal"
            )
            
        print(ID)


class Speech2Image_extend(Speech2Image_window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binding_button_click()
        
    def binding_button_click(self):
        # binding event for button
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=0, event=str(event)),
        )

        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=1, event=str(event)),
        )

        self.canvas.tag_bind(
            self.btnDelete_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=2, event=str(event)),
        )

    # the function to call when button clicked
    def get_click_event(self, ID: int, event=None):
        if ID == 0: #back button
            self.window.destroy()
            # restore the main window
            self.master.deiconify()

            #stop long-term execution thread
            StoppableThread(target=self.threadTarget_update).stop() 
            
            #put None in queue to stop update thread
            result_queue.put(None)

        elif ID == 1: #generate button
            self.loading_state = True
            
            self.canvas.itemconfig(
                self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
            )
            # unhidden loadding animation
            self.canvas.itemconfig(
                self.loadingAnimation_canvas, state="normal"
            )

            #create thread for generate image (long-term task) and for getting value from queue
            threading.Thread(target=self.threadTarget_text2image).start()
            
        elif ID == 2: #delete button
            pass

        elif ID == 3: #record button
            pass
        
        print(ID)

    def threadTarget_text2image(self):
        en_inputText = self.canvas.itemcget(self.textResult, 'text')

        engToImage = EngToImage()
        result_img = engToImage(en_inputText=en_inputText)
        
        #put to queue
        result_queue.put(result_img)
    
    def threadTarget_update(self):
        while True:
            longterm_result = result_queue.get()
            if longterm_result is None:
                print("thread_target: got None, exiting...")
                
                #update Gui from thread
                
                
                return

            else:
                try:
                    pass
                except:
                    pass
                finally:
                    #update GUI from thread
                    pass
    
root = Tk()
mainWindow = Client(root)
root.mainloop()

# #put None in queue to stop thread
# result_queue.put(None)
