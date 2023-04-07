#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/sota-fusion/ui/style-transfer.py
Path: /home/tiendat/Workspace/sota-fusion/ui
Created Date: Friday, March 3rd 2023, 4:22:07 pm
Author: tiendat

Copyright (c) 2023 Your Company
"""
from __future__ import absolute_import, division, print_function

import sys
from pathlib import Path
from tkinter import Canvas, PhotoImage, Tk, Toplevel

from PIL import Image, ImageEnhance, ImageTk

sys.path.append(str(Path(__file__).parents[1]))  # root folder
from src._config import load_config  # noqa: E402


class StyleTransfer_window:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(self.master)
        self.window.resizable(False, False)

        # get close event
        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)

        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH.joinpath("assets")

        # content, style and result image
        self.CONTENT_IMAGES = self.ASSETS_PATH.joinpath(
            *["style-transfer", "contents"]
        )
        self.STYLE_IMAGES = self.ASSETS_PATH.joinpath(
            *["style-transfer", "styles"]
        )

        # update contents and styles
        self.content_paths = sorted(Path.iterdir(self.CONTENT_IMAGES))
        self.style_paths = sorted(Path.iterdir(self.STYLE_IMAGES))

        # load size of images
        config = load_config(mode="style-transfer")
        self.w_inputSize, self.h_inputSize = config["input_size"]
        self.w_resultSize, self.h_resultSize = config["result_size"]

        # initialize
        self.content_idx, self.style_idx = 0, 0
        self.img_content_PIL = self.resize_PIL_image(PIL_image=Image.open(self.content_paths[self.content_idx]))  # type: ignore
        self.img_style_PIL = self.resize_PIL_image(PIL_image=Image.open(self.style_paths[self.style_idx]))  # type: ignore

        # setup for loading state
        self.loading_state = False

        self.__static_ui()
        self._binding_button_moveOver()

    def __on_closing(self):
        self.master.destroy()

    def resize_PIL_image(self, PIL_image: Image, is_input: bool = True):
        if is_input:
            return PIL_image.resize((self.w_inputSize, self.h_inputSize), Image.Resampling.LANCZOS)  # type: ignore

        else:
            return PIL_image.resize((self.w_resultSize, self.h_resultSize), Image.Resampling.LANCZOS)  # type: ignore

    def __static_ui(self):
        # initial static GUI
        self.window.geometry("862x519")
        self.window.configure(bg="#0F1A2C")

        # image button deactive and active
        self.img_btnGenerate = PhotoImage(
            file=self._relative_to_assets("btn_generate.png")
        )
        self.img_btnGenerate_enabled = PhotoImage(
            file=self._relative_to_assets("btn_generate_enabled.png")
        )
        self.img_btnGenerate_loading = PhotoImage(
            file=self._relative_to_assets("btn_generate_loadingBg.png")
        )

        self.img_btnBack = PhotoImage(
            file=self._relative_to_assets("btn_back.png")
        )
        self.img_btnBack_enabled = PhotoImage(
            file=self._relative_to_assets("btn_back_enabled.png")
        )

        # content, style and result image
        self.img_result = PhotoImage(
            file=self._relative_to_assets("style-transfer", "init_result.png")
        )
        self.img_content = ImageTk.PhotoImage(self.img_content_PIL)
        self.img_style = ImageTk.PhotoImage(self.img_style_PIL)

        # frames of loading gif
        _frame_count = 8  # magic number
        self.loading_frames = [
            PhotoImage(
                file=self._relative_to_assets("loading_animation.gif"),
                format="gif -index %i" % (i),
            )
            for i in range(_frame_count)
        ]

        self.canvas = Canvas(
            self.window,
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

        self.image_result_canvas = self.canvas.create_image(
            618.0, 215.0, image=self.img_result
        )

        # initialize updating the loading animation
        self.canvas.after(0, self._update_animation, 0)

        # Hidden text and loading animation
        self.canvas.itemconfig(self.text_contentImg_canvas, state="hidden")
        self.canvas.itemconfig(self.text_styleImg_canvas, state="hidden")
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="hidden")

    def _binding_button_moveOver(self):
        # binding event for button
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Enter>",
            lambda event: self.get_moveOver_event(ID=0, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Leave>",
            lambda event: self.get_moveOver_event(ID=0, event=str(event)),
        )

        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Enter>",
            lambda event: self.get_moveOver_event(ID=1, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Leave>",
            lambda event: self.get_moveOver_event(ID=1, event=str(event)),
        )

        self.canvas.tag_bind(
            self.image_content_canvas,
            "<Enter>",
            lambda event: self.get_moveOver_event(ID=2, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_content_canvas,
            "<Leave>",
            lambda event: self.get_moveOver_event(ID=2, event=str(event)),
        )

        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Enter>",
            lambda event: self.get_moveOver_event(ID=3, event=str(event)),
        )
        self.canvas.tag_bind(
            self.image_style_canvas,
            "<Leave>",
            lambda event: self.get_moveOver_event(ID=3, event=str(event)),
        )

    def _update_animation(self, idx: int):
        current_frame = self.loading_frames[idx]
        idx = idx + 1
        if idx >= len(self.loading_frames):
            idx = 0

        self.canvas.itemconfig(
            self.loadingAnimation_canvas, image=current_frame
        )
        self.canvas.after(100, self._update_animation, idx)

    def _relative_to_assets(self, *args: str) -> Path:
        RELATIVE_PATH = None

        for arg in args:
            if RELATIVE_PATH is None:
                RELATIVE_PATH = Path(arg)
            else:
                RELATIVE_PATH = RELATIVE_PATH / Path(arg)

        return self.ASSETS_PATH / Path(RELATIVE_PATH)  # type: ignore

    def get_moveOver_event(self, ID: int, event: str):
        # use new_content_image, new_style_image as GLOBAL VARIABLES
        if ID == 0:  # back button
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.buttonBack_canvas, image=self.img_btnBack_enabled
                )
            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.buttonBack_canvas, image=self.img_btnBack
                )

        elif ID == 1:  # generate button
            if not self.loading_state:
                if "Enter" in event:
                    self.canvas.itemconfig(
                        self.buttonGenerate_canvas,
                        image=self.img_btnGenerate_enabled,
                    )
                elif "Leave" in event:
                    self.canvas.itemconfig(
                        self.buttonGenerate_canvas, image=self.img_btnGenerate
                    )

        elif ID == 2:  # change content image button
            self.new_content_image = self._get_movingOver_image(
                image_PIL=self.img_content_PIL,  # type: ignore
                text_canvasItem=self.text_contentImg_canvas,
                event=event,
            )
            self.new_content_image = ImageTk.PhotoImage(self.new_content_image)  # type: ignore
            self.canvas.itemconfig(
                self.image_content_canvas, image=self.new_content_image
            )

        elif ID == 3:  # change style image button
            self.new_style_image = self._get_movingOver_image(
                image_PIL=self.img_style_PIL,  # type: ignore
                text_canvasItem=self.text_styleImg_canvas,
                event=event,
            )
            self.new_style_image = ImageTk.PhotoImage(self.new_style_image)  # type: ignore
            self.canvas.itemconfig(
                self.image_style_canvas, image=self.new_style_image
            )

    def _get_movingOver_image(
        self, image_PIL: Image, text_canvasItem: int, event: str  # type: ignore
    ):
        if "Enter" in event:
            enhancer = ImageEnhance.Brightness(image_PIL)  # type: ignore
            new_image_PIL = enhancer.enhance(0.5)
            self.canvas.itemconfig(text_canvasItem, state="normal")

        elif "Leave" in event:
            self.canvas.itemconfig(text_canvasItem, state="hidden")
            new_image_PIL = image_PIL

        return new_image_PIL

    def enter_loading_status(self):
        self.loading_state = True

        # unhidden loading animation
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="normal")

        self.canvas.itemconfig(
            self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
        )

    def exit_loading_status(self):
        self.loading_state = False

        # hidden loading animation
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="hidden")

        # restore status for generate button
        self.canvas.itemconfig(
            self.buttonGenerate_canvas, image=self.img_btnGenerate_enabled
        )


def main():
    root = Tk()
    root.withdraw()
    _ = StyleTransfer_window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
