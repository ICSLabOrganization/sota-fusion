#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/sota-fusion/ui/backend.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Saturday, March 4th 2023, 9:49:11 pm
Author: tiendat

Copyright (c) 2023 ICSLab
"""
from __future__ import absolute_import, division, print_function

import queue
import sys
import threading
import tkinter
from multiprocessing import Process
from pathlib import Path
from threading import Thread
from tkinter import Image, Tk

from loguru import logger  # type: ignore
from PIL import Image, ImageTk  # noqa: F811

sys.path.append(str(Path(__file__).parent.parent))  # root directory

from mainWindow import MainWindow  # noqa: E402
from speech2image import Speech2Image_window  # noqa: E402
from style_transfer import StyleTransfer_window  # noqa: E402

from src import (  # noqa: E402
    EngToImage,
    SpeechToViet,
    VietToEng,
    VirtualControl,
    recording,
)

# create lock for prevent race condition
lock = threading.Lock()

# create a long-term running task queue for output
result_queue = queue.Queue()


class Process_virtualControlTask(Process):
    def __init__(self):
        super().__init__()
        self.virtualControl = VirtualControl()

    def run(self):
        self.virtualControl.run()


class Process_mainTask(Process):
    def __init__(self):
        super().__init__()

    def run(self):
        root = Tk()
        # send window to front of all windows
        root.attributes("-topmost", True)

        mainWindow = Client(root)
        root.protocol("WM_DELETE_WINDOW", mainWindow.on_exit)
        root.mainloop()


class Thread_text2image(Thread):
    def __init__(self, input_text):
        super().__init__()

        self.input_text = input_text

    def run(self):
        engToImage = EngToImage()
        result_img = engToImage(en_inputText=self.input_text)

        # put to queue
        with lock:
            result_queue.put(result_img)


class Thread_recording(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        resultRecord_path = recording()

        # put to queue
        with lock:
            result_queue.put(resultRecord_path)


class Thread_speech2text(Thread):
    def __init__(self, resultRecord_path):
        super().__init__()

        self.resultRecord_path = resultRecord_path
        self.speech2viet = SpeechToViet()
        self.viet2eng = VietToEng()

    def run(self):
        vi_resultText = str(
            self.speech2viet(audio_path=self.resultRecord_path)
        )
        logger.debug("Vietnamese output text: " + vi_resultText)

        en_resultText = self.viet2eng(vi_inputText=vi_resultText)
        logger.debug("English output text: " + en_resultText)
        # put to queue
        with lock:
            result_queue.put(en_resultText)


class Client(MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.binding_button_click()

    def binding_button_click(self):
        self.canvas.tag_bind(
            self.btn_playDinosaurGame,
            "<Button-1>",
            lambda _: self.get_click_event(ID=1),
        )

        self.canvas.tag_bind(
            self.btn_styleTransfer,
            "<Button-1>",
            lambda _: self.get_click_event(ID=2),
        )

        self.canvas.tag_bind(
            self.btn_speech2image,
            "<Button-1>",
            lambda _: self.get_click_event(ID=3),
        )

    # the function to call when button clicked
    def get_click_event(self, ID: int, event=None):
        logger.debug("ID of click event: " + str(ID))

        self.window.withdraw()
        # open another window
        if ID == 2:  # style transfer button
            self.sub_window = StyleTransfer_extend(self.window)

        elif ID == 3:  # speech2image button
            self.sub_window = Speech2Image_extend(self.window)

    def on_exit(self):
        self.window.destroy()


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
        logger.debug("ID of click event: " + str(ID))

        if ID == 0:
            self.window.destroy()
            # restore the main window
            self.master.deiconify()

        elif ID == 1:
            self.canvas.itemconfig(
                self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
            )
            # unhidden loading animation
            self.canvas.itemconfig(
                self.loadingAnimation_canvas, state="normal"
            )


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

        self.canvas.tag_bind(
            self.btn_record_canvas,
            "<Button-1>",
            lambda event: self.get_click_event(ID=3, event=str(event)),
        )

    # the function to call when button clicked
    def get_click_event(self, ID: int, event=None):
        logger.debug("ID of click event: " + str(ID))

        if ID == 0:  # back button
            self.window.destroy()
            # restore the main window
            self.master.deiconify()

        elif ID == 1:  # generate button
            if self.loading_state is False:
                self.enter_loading_status()

                # create thread for generate image (long-term task) and for getting value from queue
                en_inputText = self.entry.get()

                generateImg_thread = Thread_text2image(input_text=en_inputText)
                # generateImg_thread = AsyncTask_test()
                generateImg_thread.start()

                self.monitor_gettingImage(generateImg_thread)

        elif ID == 2:  # delete button
            if self.loading_state is False:
                self.entry.delete(0, tkinter.END)

        elif ID == 3:  # record button
            if self.loading_state is False:
                self.enter_loading_status(mode="recording")

                recoding_thread = Thread_recording()
                recoding_thread.start()

                self.monitor_recording(recoding_thread)

    def monitor_gettingImage(self, thread: Thread):
        if thread.is_alive():
            # check the thread every 100ms
            logger.info("Still get image...")
            self.window.after(100, lambda: self.monitor_gettingImage(thread))
        else:
            logger.info("Thread done!!")
            new_resultImage = result_queue.get()

            # exit updating status for GUI
            self.exit_loading_status()

            if new_resultImage is None:
                logger.info("Image not found")

            else:
                # resize result image
                (w, h) = (self.img_result.width(), self.img_result.height())

                # MUST USE GLOBAL VARIABLES
                self.new_resultImage = new_resultImage.resize((w, h), Image.Resampling.LANCZOS)  # type: ignore

                self.new_resultImage = ImageTk.PhotoImage(self.new_resultImage)

                self.canvas.itemconfig(
                    self.image_result_canvas, image=self.new_resultImage  # type: ignore
                )

                logger.debug("Image updated")

    def monitor_recording(self, thread: Thread):
        if thread.is_alive():
            # check the thread every 100ms
            logger.info("Still recording...")
            self.window.after(100, lambda: self.monitor_recording(thread))

        else:
            logger.info("Thread done!!")
            resultRecord_path = result_queue.get()

            # exit updating status for GUI
            # self.exit_loading_status()

            if resultRecord_path is None:
                logger.info("Path not found")

            else:
                # update status recording for GUI
                self.canvas.itemconfig(
                    self.btn_record_canvas, image=self.img_btnRecord_enabled
                )

                self.enter_loading_status()  # for loading animation

                # start speech2text thread
                speech2text_thread = Thread_speech2text(
                    resultRecord_path=resultRecord_path
                )
                speech2text_thread.start()

                self.monitor_gettingText(speech2text_thread)

    def monitor_gettingText(self, thread: Thread):
        if thread.is_alive():
            # check the thread every 100ms
            logger.info("Still getting text...")
            self.window.after(100, lambda: self.monitor_gettingText(thread))

        else:
            logger.info("Thread done!!")
            new_resultText = result_queue.get()

            # exit updating status for GUI
            self.exit_loading_status()

            if new_resultText is None:
                logger.info("Text not found")

            else:
                self.entry.delete(0, tkinter.END)
                self.entry.insert(0, new_resultText)

                logger.debug("Text updated")


if __name__ == "__main__":
    process_virtualControlTask = Process_virtualControlTask()
    process_mainTask = Process_mainTask()

    # start two processes
    process_virtualControlTask.start()
    process_mainTask.start()

    # wait for process to finish
    process_virtualControlTask.join()
    process_mainTask.join()
