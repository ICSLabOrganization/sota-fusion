#!/usr/bin/env python

from pathlib import Path

import PySimpleGUI as sg
import yaml
from main_window import convert_to_bytes

"""
Filename: /home/tiendat/Workspace/SOTA_CV-App/ui/Speech2Image_window.py
Path: /home/tiendat/Workspace/SOTA_CV-App/ui
Created Date: Wednesday, February 1st 2023, 6:12:13 pm
Author: tiendat

Copyright (c) 2023 ICSLab
"""

CONFIG_PATH = Path(__file__).parent.absolute().joinpath("config.yml")
# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

# get current file path
DIR_PATH = Path(__file__).parent.absolute().joinpath("assets")

SAMPLE_IMG = DIR_PATH.joinpath("speech2image_mode.png")

QUIT_BTN = DIR_PATH.joinpath("quit_button.png")
RECORD_BTN = DIR_PATH.joinpath("record_button.png")
DELETE_BTN = DIR_PATH.joinpath("delete_button.png")


def make_Speech2Image_window():
    layout = [
        [sg.Button(key="-EXIT-")],
        [sg.Multiline(s=(30, 3), expand_x=True)],
        [
            sg.Button(key="-RECORD-"),
            sg.Button(key="-DELETE-"),
        ],
        [sg.Image(key="-RESULT_IMAGE-")],
    ]

    return sg.Window(
        "Speech to image mode", layout, finalize=True, size=(1000, 500)
    )


def main():
    window = make_Speech2Image_window()

    # update image for button and image object
    window["-EXIT-"].update(
        image_data=convert_to_bytes(
            QUIT_BTN, config["size"]["default_btn_size"]
        )
    )
    window["-RECORD-"].update(
        image_data=convert_to_bytes(
            RECORD_BTN, config["size"]["default_btn_size"]
        )
    )
    window["-DELETE-"].update(
        image_data=convert_to_bytes(
            DELETE_BTN, config["size"]["default_btn_size"]
        )
    )

    window["-RESULT_IMAGE-"].update(
        data=convert_to_bytes(SAMPLE_IMG, config["size"]["img_size"])
    )
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

    window.close()


if __name__ == "__main__":
    main()
