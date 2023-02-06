#!/usr/bin/env python

import random
from pathlib import Path

import PySimpleGUI as sg
import yaml
from main_window import convert_to_bytes

"""
Filename: /home/tiendat/Workspace/SOTA_CV-App/ui/StyleTransfer_window.py
Path: /home/tiendat/Workspace/SOTA_CV-App/ui
Created Date: Thursday, February 2nd 2023, 10:20:32 am
Author: tiendat

Copyright (c) 2023 ICSLab
"""

CONFIG_PATH = Path(__file__).parent.absolute().joinpath("config.yml")
# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

# update image path
DIR_PATH = Path(__file__).parent.absolute().joinpath("assets/style_transfer")
RESULT_IMG = DIR_PATH.joinpath("sample_result.png")
QUIT_BTN = DIR_PATH.parent.joinpath("quit_button.png")

btn_dict = {
    "-SWITCH SAMPLE-": DIR_PATH.joinpath("samples"),
    "-SWITCH STYLE-": DIR_PATH.joinpath("styles"),
}


def update_img(window, key, btn_size):
    if btn_dict[key].is_file():
        random_imgPath = random.choice(
            [
                img_path
                for img_path in btn_dict[key].parent.iterdir()
                if not img_path.samefile(btn_dict[key])
            ]
        )
    else:
        random_imgPath = random.choice(
            [img_path for img_path in btn_dict[key].iterdir()]
        )

    # update button dict
    btn_dict[key] = random_imgPath
    window[key].update(image_data=convert_to_bytes(random_imgPath, btn_size))
    return


def make_StyleTransfer_window():
    layout = [
        [sg.Button(key="-EXIT-")],
        [sg.Button(key=key) for key in btn_dict.keys()],
        [sg.Button("Generate", key="-GENERATE-", expand_x=True)],
        [sg.Image(key="-RESULT_IMAGE-", expand_x=True)],
    ]

    return sg.Window(
        "Style transfer mode", layout, finalize=True, size=(1000, 500)
    )


def main():
    # TODO: remove bad practice
    window = make_StyleTransfer_window()

    # update image for button and image object
    window["-EXIT-"].update(
        image_data=convert_to_bytes(
            QUIT_BTN, config["size"]["default_btn_size"]
        )
    )

    for key in btn_dict.keys():
        update_img(
            window, key, config["size"]["img_btn_size"]
        )  # button size not changes

    # window["-RESULT_IMAGE-"].expand(expand_y = True)
    window["-RESULT_IMAGE-"].update(
        data=convert_to_bytes(RESULT_IMG, config["size"]["img_size"])
    )

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        for key in btn_dict.keys():
            if event == key:
                update_img(
                    window, key, config["size"]["img_btn_size"]
                )  # button size not changes
    window.close()


if __name__ == "__main__":
    main()
