#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/sota-fusion/ui/speech2image.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Friday, March 3rd 2023, 4:22:07 pm
Author: tiendat

Copyright (c) 2023 ICSLab
"""
from __future__ import absolute_import, division, print_function

from pathlib import Path

# Explicit imports to satisfy Flake8
from tkinter import Canvas, PhotoImage, Tk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.joinpath("assets")


class Speech2Image(object):
    def __init__(self):
        # replace current window with new window
        pass

    def __call__(self):
        # initial static GUI
        window = Tk()

        window.geometry("862x519")
        window.configure(bg="#0F1A2C")

        # image button deactive and active
        self.img_btnGenerate = PhotoImage(
            file=self.__relative_to_assets("btn_generate.png")
        )
        self.img_btnGenerate_enabled = PhotoImage(
            file=self.__relative_to_assets("btn_generate_enabled.png")
        )
        self.img_btnGenerate_loading = PhotoImage(
            file=self.__relative_to_assets("btn_generate_loadingbg.png")
        )

        self.img_btnDelete = PhotoImage(
            file=self.__relative_to_assets("speech2image", "btn_delete.png")
        )
        self.img_btnDelete_enabled = PhotoImage(
            file=self.__relative_to_assets(
                "speech2image", "btn_delete_enabled.png"
            )
        )

        self.img_btnBack = PhotoImage(
            file=self.__relative_to_assets("btn_back.png")
        )
        self.img_btnBack_enabled = PhotoImage(
            file=self.__relative_to_assets("btn_back_enabled.png")
        )

        img_result = PhotoImage(
            file=self.__relative_to_assets("speech2image", "init_result.png")
        )
        img_btn_record = PhotoImage(
            file=self.__relative_to_assets("speech2image", "btn_record.png")
        )

        # frames of loading gif
        frame_count = 8  # magic number
        self.loading_frames = [
            PhotoImage(
                file=self.__relative_to_assets("loading_animation.gif"),
                format="gif -index %i" % (i),
            )
            for i in range(frame_count)
        ]

        self.canvas = Canvas(
            window,
            bg="#0F1A2C",
            height=519,
            width=862,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        # create canvas object
        self.buttonBack_canvas = self.canvas.create_image(
            750.0, 448.0, image=self.img_btnBack
        )

        self.buttonGenerate_canvas = self.canvas.create_image(
            532.0, 448.0, image=self.img_btnGenerate
        )
        self.loadingAnimation_canvas = self.canvas.create_image(
            532.0, 448.0, image=self.loading_frames[0]
        )

        image_result_canvas = self.canvas.create_image(
            618.0, 215.0, image=img_result
        )

        btn_record_canvas = self.canvas.create_image(
            208.0, 102.0, image=img_btn_record
        )

        self.btnDelete_canvas = self.canvas.create_image(
            332.0, 215.0, image=self.img_btnDelete
        )

        # initialize updating the loading animation
        self.canvas.after(0, self.__update_animation, 0)

        # hidden loading animation
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="hidden")

        # binding event for button
        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Button-1>",
            lambda event: self.__get_click_event(ID=0, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=0, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=0, event=str(event)),
        )

        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Button-1>",
            lambda event: self.__get_click_event(ID=1, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
        )

        self.canvas.tag_bind(
            self.btnDelete_canvas,
            "<Button-1>",
            lambda event: self.__get_click_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btnDelete_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btnDelete_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )

        # create window
        window.resizable(False, False)
        window.mainloop()

    def __update_animation(self, idx: int):
        current_frame = self.loading_frames[idx]
        idx = idx + 1
        if idx >= len(self.loading_frames):
            idx = 0

        self.canvas.itemconfig(
            self.loadingAnimation_canvas, image=current_frame
        )
        self.canvas.after(100, self.__update_animation, idx)

    def __relative_to_assets(self, *args: str) -> Path:
        RELATIVE_PATH = None

        for arg in args:
            if RELATIVE_PATH is None:
                RELATIVE_PATH = Path(arg)
            else:
                RELATIVE_PATH = RELATIVE_PATH / Path(arg)

        return ASSETS_PATH / Path(RELATIVE_PATH)

    def __get_moveOver_event(self, ID: int, event: str):
        if ID == 0:
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.buttonGenerate_canvas,
                    image=self.img_btnGenerate_enabled,
                )

            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.buttonGenerate_canvas, image=self.img_btnGenerate
                )

            else:
                return

        elif ID == 1:
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.buttonBack_canvas, image=self.img_btnBack_enabled
                )

            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.buttonBack_canvas, image=self.img_btnBack
                )

            else:
                return

        elif ID == 2:
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.btnDelete_canvas, image=self.img_btnDelete_enabled
                )

            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.btnDelete_canvas, image=self.img_btnDelete
                )

            else:
                return

        else:
            return

    # the function to call when button clicked
    def __get_click_event(self, ID: int, event=None):
        if ID == 0:
            self.canvas.itemconfig(
                self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
            )
            # unhidden loadding animation
            self.canvas.itemconfig(
                self.loadingAnimation_canvas, state="normal"
            )

        print("clicked")
        return


def main():
    speech2Image_window = Speech2Image()
    speech2Image_window()


if __name__ == "__main__":
    main()
