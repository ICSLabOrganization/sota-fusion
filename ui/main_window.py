#!/usr/bin/env python

import base64
import io
from pathlib import Path, PurePath

import PIL.Image
import PIL.ImageOps
import PySimpleGUI as sg
import yaml

"""
Main window layout and connection between other windows

Filename: /home/tiendat/Workspace/SOTA_CV-App/ui/main_window.py
Path: /home/tiendat/Workspace/SOTA_CV-App/ui
Created Date: Tuesday, January 31st 2023, 1:20:17 pm
Author: tiendat

Copyright (c) 2023 ICSLab
"""

# get current file path
DIR_PATH = Path(__file__).parent.absolute().joinpath("assets")

CONFIG_PATH = DIR_PATH.parent.absolute().joinpath("config.yml")

# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

QUIT_BTN = DIR_PATH.joinpath(config["img_path"]["QUIT_BTN"])
SETTINGS_BTN = DIR_PATH.joinpath(config["img_path"]["SETTINGS_BTN"])
MODE1_BTN = DIR_PATH.joinpath(config["img_path"]["MODE1_BTN"])
MODE2_BTN = DIR_PATH.joinpath(config["img_path"]["MODE2_BTN"])
MODE3_BTN = DIR_PATH.joinpath(config["img_path"]["MODE3_BTN"])

btn_dict = {
    "-MODE1-": [MODE1_BTN, config["modes"]["button1"]],
    "-MODE2-": [MODE2_BTN, config["modes"]["button2"]],
    "-MODE3-": [MODE3_BTN, config["modes"]["button3"]],
}


def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = PIL.Image.new("RGBA", (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im


def convert_to_bytes(file_or_bytes, resize=None, fill=False):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :param fill: If True then the image is filled/padded so that the image is not distorted
    :type fill: (bool)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """

    # TODO: check path is exists and PNG extension
    if isinstance(file_or_bytes, PurePath):
        img = PIL.Image.open(file_or_bytes)

    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    # cur_width, cur_height = img.size
    if resize:
        width, height = resize
        img = PIL.ImageOps.pad(img, (width, height), color=(255, 255, 255))
    if fill:
        if resize is not None:
            img = make_square(img, resize[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


def make_main_window():
    column_centered = [
        [sg.Text(config["instruction_text"], key="INSTRUCTION")]
    ]

    # TODO: image size
    layout = [
        [sg.Button(image_filename=SETTINGS_BTN, image_subsample=10)],
        # components centered
        [
            sg.Push(),
            sg.Column(column_centered, element_justification="center"),
            sg.Push(),
        ],
        [
            sg.Button(key=key, expand_x=True, expand_y=True)
            for key in btn_dict.keys()
        ],
    ]

    return sg.Window("SOTA-CV demo", layout, finalize=True, size=(1000, 500))


def main():
    # main window dose not active when open other windows
    # styleTransfer_window = None
    # speech2Image_window = None
    main_window = make_main_window()

    # event binding
    # main_window.bind('<Configure>', '-CONFIG-')
    for mode in btn_dict.keys():
        main_window[mode].bind("<Enter>", "+MOUSE OVER+")
        main_window[mode].bind("<Leave>", "+MOUSE AWAY+")

    # update image for buttons
    for key, value in btn_dict.items():
        btn_size = main_window[key].get_size()
        main_window[key].update(
            image_data=convert_to_bytes(value[0], btn_size)
        )  # image path
    while True:
        window, event, values = sg.read_all_windows()

        if event == sg.WIN_CLOSED and window == main_window:
            break

        if window == main_window:
            # print(event)

            # update text when mouse move over element
            if event.endswith("+MOUSE OVER+"):
                for key in btn_dict:
                    if event.startswith(key):
                        window["INSTRUCTION"].update(
                            btn_dict[key][1]  # text content
                        )
            elif event.endswith("+MOUSE AWAY+"):
                window["INSTRUCTION"].update(config["instruction_text"])

        # playing game mode

        # style transfer mode
        # if event == 'MODE2' and not styleTransfer_window:
        #    main_window.hide()
        #    styleTransfer_window = make_StyleTransfer_window()

        # if window == styleTransfer_window and (event in (sg.WIN_CLOSED, 'Exit')):
        #    styleTransfer_window.close()
        #    styleTransfer_window = None
        #    main_window.un_hide()

        # speech to image mode
        # if event == 'MODE3' and not speech2Image_window:
        #    main_window.hide()
        #    speech2Image_window = make_Speech2Image_window()

        # if window == speech2Image_window and (event in (sg.WIN_CLOSED, 'Exit')):
        #    speech2Image_window.close()
        #    speech2Image_window = None
        #    main_window.un_hide()

    main_window.close()


if __name__ == "__main__":
    main()
