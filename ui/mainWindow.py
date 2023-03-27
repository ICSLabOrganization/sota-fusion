#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/sota-fusion/ui/mainWindow.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Friday, March 3rd 2023, 4:22:07 pm
Author: tiendat

Copyright (c) 2023 ICSLab
"""
from __future__ import absolute_import, division, print_function

from pathlib import Path
from tkinter import Canvas, PhotoImage, Tk

from style_transfer import StyleTransfer_window
from speech2image import Speech2Image_window

class MainWindow:
    def __init__(self, master: Tk):
        self.window = master
        self.window.resizable(False, False)

        # replace current window with new window
        PARENT_PATH = Path(__file__).parent
        self.ASSETS_PATH = PARENT_PATH.joinpath(*["assets", "mainWindow"])
        
        self.__static_ui()
        self.__binding_button_moveOver()

    def __static_ui(self):
        _introduction_font = "Caladea"
        _introduction_fontSize = 20

        # initial static GUI
        self.window.geometry("862x519")
        self.window.configure(bg="#3A7FF6")

        # image background
        _img_bg = self.__relative_to_assets("bg.png")
        _img_bg_playDinosaurGame = self.__relative_to_assets("bg_play-dinosaur-game.png")
        _img_bg_styleTransfer = self.__relative_to_assets("bg_style-transfer.png")
        _img_bg_speech2image = self.__relative_to_assets("bg_speech2image.png")

        # image button deactive
        _img_btn_playDinosaurGame = self.__relative_to_assets("btn_play-dinosaur-game.png")
        _img_btn_styleTransfer = self.__relative_to_assets("btn_style-transfer.png")
        _img_btn_speech2image = self.__relative_to_assets("btn_speech2image.png")

        # image button active
        _img_btn_playDinosaurGame_enabled = self.__relative_to_assets(
            "btn_play-dinosaur-game_enabled.png"
        )
        _img_btn_styleTransfer_enabled = self.__relative_to_assets(
            "btn_style-transfer_enabled.png"
        )
        _img_btn_speech2image_enabled = self.__relative_to_assets(
            "btn_speech2image_enabled.png"
        )

        self.canvas = Canvas(
            self.window,
            bg="#3A7FF6",
            height=519,
            width=862,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        self.bg = self.canvas.create_image(646.0, 259.0, image=_img_bg)

        self.btn_speech2image = self.canvas.create_image(
            646.0, 423.0, image=_img_btn_speech2image
        )

        self.btn_styleTransfer = self.canvas.create_image(
            646.0, 312.0, image=_img_btn_styleTransfer
        )

        self.btn_playDinosaurGame = self.canvas.create_image(
            646.0, 201.0, image=_img_btn_playDinosaurGame
        )

        self.canvas.create_text(
            40.0,
            127.0,
            anchor="nw",
            text="Welcome to sota-fusion",
            fill="#FCFCFC",
            font=("Roboto Medium", 24 * -1),
        )

        self.canvas.create_text(
            541.0,
            87.0,
            anchor="nw",
            text="Please select mode",
            fill="#505485",
            font=("Roboto Medium", 24 * -1),
        )

        self.canvas.create_rectangle(40.0, 160.0, 100.0, 165.0, fill="#FCFCFC", outline="")

        self.canvas.create_text(
            40.0,
            335.0,
            anchor="nw",
            text="one. ",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.canvas.create_text(
            40.0,
            302.0,
            anchor="nw",
            text="technologies into only ",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.canvas.create_text(
            40.0,
            269.0,
            anchor="nw",
            text="computer vision ",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.canvas.create_text(
            40.0,
            236.0,
            anchor="nw",
            text="many state-of-the-art",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.canvas.create_text(
            40.0,
            203.0,
            anchor="nw",
            text="application combining",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.canvas.create_text(
            40.0,
            170.0,
            anchor="nw",
            text="sota-fusion is an",
            fill="#FCFCFC",
            font=(_introduction_font, _introduction_fontSize * -1),
        )

        self.switcher = {
            0: {
                "background_img": _img_bg,
                "button_img": [
                    _img_btn_playDinosaurGame,
                    _img_btn_styleTransfer,
                    _img_btn_speech2image,
                ],
            },
            1: {
                "btn_obj": self.btn_playDinosaurGame,
                "background_img": _img_bg_playDinosaurGame,
                "button_img": _img_btn_playDinosaurGame_enabled,
            },
            2: {
                "btn_obj": self.btn_styleTransfer,
                "background_img": _img_bg_styleTransfer,
                "button_img": _img_btn_styleTransfer_enabled,
            },
            3: {
                "btn_obj": self.btn_speech2image,
                "background_img": _img_bg_speech2image,
                "button_img": _img_btn_speech2image_enabled,
            },
        }

    def __binding_button_moveOver(self):
        # binding event for button
        self.canvas.tag_bind(
            self.btn_playDinosaurGame,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btn_playDinosaurGame,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
        )

        self.canvas.tag_bind(
            self.btn_styleTransfer,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btn_styleTransfer,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )

        self.canvas.tag_bind(
            self.btn_speech2image,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btn_speech2image,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
        )

    def __relative_to_assets(self, *args: str) -> Path:
        RELATIVE_PATH = None

        for arg in args:
            if RELATIVE_PATH is None:
                RELATIVE_PATH = Path(arg)
            else:
                RELATIVE_PATH = RELATIVE_PATH / Path(arg)

        return PhotoImage(file=self.ASSETS_PATH / Path(RELATIVE_PATH))

    def __get_moveOver_event(self, ID: int, event: str):
        if "Enter" in event:
            self.canvas.itemconfig(self.bg, image=self.switcher[ID]["background_img"])
            self.canvas.itemconfig(
                self.switcher[ID]["btn_obj"], image=self.switcher[ID]["button_img"]
            )
            
        
        elif "Leave" in event:
            self.canvas.itemconfig(self.bg, image=self.switcher[0]["background_img"])
            self.canvas.itemconfig(
                self.switcher[ID]["btn_obj"], image=self.switcher[0]["button_img"][ID - 1]
            )
            
def main():
    root = Tk()
    _ = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()








