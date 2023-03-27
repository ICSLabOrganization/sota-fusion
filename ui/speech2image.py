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
from tkinter import Canvas, PhotoImage, Tk, Toplevel


class Speech2Image_window:
    def __init__(self, master: Tk):
        self.master = master
        self.window = Toplevel(self.master)
        self.window.resizable(False, False)

        # get close event
        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)

        # replace current window with new window
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH.joinpath("assets")

        self.__static_ui()
        self.__binding_button_moveOver()

        # setup for loading state
        self.loading_state = False

    def __on_closing(self):
        self.master.destroy()

    def __static_ui(self):
        # initial static GUI
        self.window.geometry("862x519")
        self.window.configure(bg="#0F1A2C")

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

        self.img_btnRecord = PhotoImage(
            file=self.__relative_to_assets("speech2image", "btn_record.png")
        )
        self.img_btnRecord_enabled = PhotoImage(
            file=self.__relative_to_assets(
                "speech2image", "btn_record_enabled.png"
            )
        )
        self.img_btnRecord_running = PhotoImage(
            file=self.__relative_to_assets(
                "speech2image", "btn_record_running.png"
            )
        )

        self.img_result = PhotoImage(
            file=self.__relative_to_assets("speech2image", "init_result.png")
        )
        # self.img_result = PhotoImage(
        #     file="/home/tiendat/Workspace/Building_app/sota-fusion/src/speech2image/assets/output-images/output1.png"
        # )
        # frames of loading gif
        _frame_count = 8  # magic number
        self.loading_frames = [
            PhotoImage(
                file=self.__relative_to_assets("loading_animation.gif"),
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

        self.btn_record_canvas = self.canvas.create_image(
            208.0, 102.0, image=self.img_btnRecord
        )

        self.btnDelete_canvas = self.canvas.create_image(
            332.0, 215.0, image=self.img_btnDelete
        )

        self.textResult_canvas = self.canvas.create_text(
            47.0,
            94.0,
            anchor="nw",
            text="Two cute cats dancing",
            fill="#000000",
            font=("Caladea", 15 * -1),
        )

        # initialize updating the loading animation
        self.canvas.after(0, self.__update_animation, 0)

        # hidden loading animation
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="hidden")

    def __binding_button_moveOver(self):
        # binding event for button
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=0, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonBack_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=0, event=str(event)),
        )

        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
        )
        self.canvas.tag_bind(
            self.buttonGenerate_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=1, event=str(event)),
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

        self.canvas.tag_bind(
            self.btn_record_canvas,
            "<Enter>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
        )
        self.canvas.tag_bind(
            self.btn_record_canvas,
            "<Leave>",
            lambda event: self.__get_moveOver_event(ID=3, event=str(event)),
        )

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

        return self.ASSETS_PATH / Path(RELATIVE_PATH)  # type: ignore

    def __get_moveOver_event(self, ID: int, event: str):
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
            if not self.loading_state:  # default is true
                if "Enter" in event:
                    self.canvas.itemconfig(
                        self.buttonGenerate_canvas,
                        image=self.img_btnGenerate_enabled,
                    )

                elif "Leave" in event:
                    self.canvas.itemconfig(
                        self.buttonGenerate_canvas, image=self.img_btnGenerate
                    )

        elif ID == 2:  # delete button
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.btnDelete_canvas, image=self.img_btnDelete_enabled
                )

            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.btnDelete_canvas, image=self.img_btnDelete
                )

        elif ID == 3:  # recording button
            if "Enter" in event:
                self.canvas.itemconfig(
                    self.btn_record_canvas, image=self.img_btnRecord_enabled
                )

            elif "Leave" in event:
                self.canvas.itemconfig(
                    self.btn_record_canvas, image=self.img_btnRecord
                )

    def enter_loading_status(self, mode: str = None):  # type: ignore
        self.loading_state = True

        if mode == "recording":
            # update status recording button
            self.canvas.itemconfig(
                self.btn_record_canvas, image=self.img_btnRecord_running
            )

        else:
            # unhidden loadding animation
            self.canvas.itemconfig(
                self.loadingAnimation_canvas, state="normal"
            )

            self.canvas.itemconfig(
                self.buttonGenerate_canvas, image=self.img_btnGenerate_loading
            )

    def exit_loading_status(self):
        self.loading_state = False

        # hidden loadding animation
        self.canvas.itemconfig(self.loadingAnimation_canvas, state="hidden")

        # restore status for generate button
        self.canvas.itemconfig(
            self.buttonGenerate_canvas, image=self.img_btnGenerate_enabled
        )

        # restore status for record button
        self.canvas.itemconfig(
            self.btn_record_canvas, image=self.img_btnRecord_enabled
        )


def main():
    root = Tk()
    root.withdraw()
    _ = Speech2Image_window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
