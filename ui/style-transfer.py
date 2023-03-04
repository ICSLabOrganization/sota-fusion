#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/sota-fusion/ui/style-transfer.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Friday, March 3rd 2023, 4:22:07 pm
Author: tiendat

Copyright (c) 2023 Your Company
"""
from __future__ import absolute_import, division, print_function

from pathlib import Path

# Explicit imports to satisfy Flake8
from tkinter import Canvas, PhotoImage, Tk

from PIL import Image, ImageEnhance, ImageTk

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.joinpath("assets")


class StyleTransfer:
    def __init__(self):
        # replace current window with new window

        # content, style and result image
        self.img_content_PIL = Image.open(
            self.__relative_to_assets("style-transfer", "init_content.png")
        )
        self.img_style_PIL = Image.open(
            self.__relative_to_assets("style-transfer", "init_style.png")
        )

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

        self.img_btnBack = PhotoImage(
            file=self.__relative_to_assets("btn_back.png")
        )
        self.img_btnBack_enabled = PhotoImage(
            file=self.__relative_to_assets("btn_back_enabled.png")
        )

        # content, style and result image
        self.img_result = PhotoImage(
            file=self.__relative_to_assets("style-transfer", "init_result.png")
        )
        self.img_content = ImageTk.PhotoImage(self.img_content_PIL)
        self.img_style = ImageTk.PhotoImage(self.img_style_PIL)

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
        self.image_content_canvas = self.canvas.create_image(
            205.0, 136.0, image=self.img_content
        )

        self.text_contentImg_canvas = self.canvas.create_text(
            133.0,
            129.0,
            anchor="nw",
            text="Change content image",
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 13 * -1),
        )

        self.image_style_canvas = self.canvas.create_image(
            205.0, 368.0, image=self.img_style
        )

        self.text_styleImg_canvas = self.canvas.create_text(
            142.0,
            361.0,
            anchor="nw",
            text="Change style image",
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 13 * -1),
        )

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
            618.0, 215.0, image=self.img_result
        )

        # initialize updating the loading animation
        self.canvas.after(0, self.__update_animation, 0)

        # Hidden text and loading animation
        self.canvas.itemconfig(self.text_contentImg_canvas, state="hidden")
        self.canvas.itemconfig(self.text_styleImg_canvas, state="hidden")
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
            self.image_content_canvas,
            "<Button-1>",
            lambda event: self.__get_click_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_content_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_content_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=2, event=str(event)),
        )

        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Button-1>",
            lambda event: self.__get_click_event(ID=3, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
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
        # use new_content_image, new_style_image as global variables
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
            self.new_content_image = self.__get_movingOver_image(
                image_PIL=self.img_content_PIL,
                text_canvasItem=self.text_contentImg_canvas,
                event=event,
            )
            self.new_content_image = ImageTk.PhotoImage(self.new_content_image)
            self.canvas.itemconfig(
                self.image_content_canvas, image=self.new_content_image
            )
            return

        elif ID == 3:
            self.new_style_image = self.__get_movingOver_image(
                image_PIL=self.img_style_PIL,
                text_canvasItem=self.text_styleImg_canvas,
                event=event,
            )
            self.new_style_image = ImageTk.PhotoImage(self.new_style_image)
            self.canvas.itemconfig(
                self.image_style_canvas, image=self.new_style_image
            )
            return

        else:
            return

    def __get_movingOver_image(
        self, image_PIL: Image, text_canvasItem: int, event: str
    ):
        if "Enter" in event:
            enhancer = ImageEnhance.Brightness(image_PIL)
            new_image_PIL = enhancer.enhance(0.5)
            self.canvas.itemconfig(text_canvasItem, state="normal")

        elif "Leave" in event:
            self.canvas.itemconfig(text_canvasItem, state="hidden")
            new_image_PIL = image_PIL

        else:
            return

        return new_image_PIL

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
    styleTransfer_window = StyleTransfer()
    styleTransfer_window()


if __name__ == "__main__":
    main()
