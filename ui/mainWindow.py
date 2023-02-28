# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

#TODO: use class instead function

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.joinpath("assets").joinpath("mainWindow")


def relative_to_assets(path: str):
    return PhotoImage(file=(ASSETS_PATH / Path(path)))


def get_moveOver_event(ID: int, event: str=None):
    if "Enter" in event:
        canvas.itemconfig(bg, image=switcher[ID]["background_img"])
        canvas.itemconfig(switcher[ID]["btn_obj"], image=switcher[ID]["button_img"])
    
    elif "Leave" in event:
        canvas.itemconfig(bg, image=switcher[0]["background_img"])
        canvas.itemconfig(switcher[ID]["btn_obj"], image=switcher[0]["button_img"][ID-1])

    else:
        pass

# the function to call when button clicked
def get_click_event(ID:int, event=None):
    print('clicked')


########################static gui##############################
window = Tk()

window.geometry("862x519")
window.configure(bg = "#3A7FF6")

#image background 
img_bg = relative_to_assets("bg.png")
img_bg_playDinosaurGame = relative_to_assets("bg_play-dinosaur-game.png")
img_bg_styleTransfer = relative_to_assets("bg_style-transfer.png")
img_bg_speech2image = relative_to_assets("bg_speech2image.png")

#image button deactive
img_btn_playDinosaurGame = relative_to_assets("btn_play-dinosaur-game.png")
img_btn_styleTransfer = relative_to_assets("btn_style-transfer.png")
img_btn_speech2image = relative_to_assets("btn_speech2image.png")

#image button active
img_btn_playDinosaurGame_enabled = relative_to_assets("btn_play-dinosaur-game_enabled.png")
img_btn_styleTransfer_enabled = relative_to_assets("btn_style-transfer_enabled.png")
img_btn_speech2image_enabled = relative_to_assets("btn_speech2image_enabled.png")

# switcher = {
#         0 : [img_bg, [img_btn_playDinosaurGame,
#                       img_btn_styleTransfer, 
#                       img_btn_speech2image]],
#         1 : [img_bg_playDinosaurGame, img_btn_playDinosaurGame_enabled],
#         2 : [img_bg_styleTransfer,    img_btn_styleTransfer_enabled],
#         3 : [img_bg_speech2image,     img_btn_speech2image_enabled],
#         }


canvas = Canvas(
    window,
    bg = "#3A7FF6",
    height = 519,
    width = 862,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
bg = canvas.create_image(
    646.0,
    259.0,
    image=img_bg
)

btn_speech2image = canvas.create_image(
    646.0,
    423.0,
    image=img_btn_speech2image
)

btn_styleTransfer= canvas.create_image(
    646.0,
    312.0,
    image=img_btn_styleTransfer
)

btn_playDinosaurGame = canvas.create_image(
    646.0,
    201.0,
    image=img_btn_playDinosaurGame
)

canvas.create_text(
    40.0,
    127.0,
    anchor="nw",
    text="Welcome to sota-fusion",
    fill="#FCFCFC",
    font=("Roboto Bold", 24 * -1)
)

canvas.create_text(
    541.0,
    87.0,
    anchor="nw",
    text="Please select mode",
    fill="#505485",
    font=("Roboto Bold", 24 * -1)
)

canvas.create_rectangle(
    40.0,
    160.0,
    100.0,
    165.0,
    fill="#FCFCFC",
    outline="")

canvas.create_text(
    40.0,
    335.0,
    anchor="nw",
    text="one. ",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)

canvas.create_text(
    40.0,
    302.0,
    anchor="nw",
    text="technologies into only ",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)

canvas.create_text(
    40.0,
    269.0,
    anchor="nw",
    text="computer vision ",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)

canvas.create_text(
    40.0,
    236.0,
    anchor="nw",
    text="many state-of-the-art",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)

canvas.create_text(
    40.0,
    203.0,
    anchor="nw",
    text="application combining",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)

canvas.create_text(
    40.0,
    170.0,
    anchor="nw",
    text="sota-fusion is an",
    fill="#FCFCFC",
    font=("ABeeZee Regular", 24 * -1)
)
########################static gui##############################

switcher = {
        0 : {
            "background_img" : img_bg,
            "button_img" : [img_btn_playDinosaurGame,
                        img_btn_styleTransfer,
                        img_btn_speech2image
                        ]
            },
        1 : {
            "btn_obj" : btn_playDinosaurGame,
            "background_img" : img_bg_playDinosaurGame,
            "button_img" : img_btn_playDinosaurGame_enabled
            },
        2 : {
            "btn_obj" : btn_styleTransfer,
            "background_img" : img_bg_styleTransfer,
            "button_img" : img_btn_styleTransfer_enabled
            },
        3 : {
            "btn_obj" : btn_speech2image,
            "background_img" : img_bg_speech2image,
            "button_img" : img_btn_speech2image_enabled
            },
        }

#bind "button" image as real button
canvas.tag_bind(btn_playDinosaurGame, '<Button-1>', lambda event: get_click_event(ID=1))
canvas.tag_bind(btn_playDinosaurGame, '<Enter>',    lambda event: get_moveOver_event(ID=1, event=str(event)))
canvas.tag_bind(btn_playDinosaurGame, '<Leave>',    lambda event: get_moveOver_event(ID=1, event=str(event)))

canvas.tag_bind(btn_styleTransfer, '<Button-1>', lambda event: get_click_event(ID=2))
canvas.tag_bind(btn_styleTransfer, '<Enter>',    lambda event: get_moveOver_event(ID=2, event=str(event)))
canvas.tag_bind(btn_styleTransfer, '<Leave>',    lambda event: get_moveOver_event(ID=2, event=str(event)))

canvas.tag_bind(btn_speech2image, '<Button-1>', lambda event: get_click_event(ID=3))
canvas.tag_bind(btn_speech2image, '<Enter>',    lambda event: get_moveOver_event(ID=3, event=str(event)))
canvas.tag_bind(btn_speech2image, '<Leave>',    lambda event: get_moveOver_event(ID=3, event=str(event)))

window.resizable(False, False)
window.mainloop()
