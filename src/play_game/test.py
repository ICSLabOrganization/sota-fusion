from pathlib import Path
import pygame

PARENTPATH  = Path(__file__).parent
ASSERTPATH = PARENTPATH.joinpath('Assets')

start_img_path = ASSERTPATH.joinpath('start_img.png')
game_over_img_path = ASSERTPATH.joinpath('game_over.png')
replay_img_path = ASSERTPATH.joinpath('replay.png')
numbers_img_path = ASSERTPATH.joinpath('numbers.png')

SOUNDPATH = PARENTPATH.joinpath('Sounds')

jump_fx_path = SOUNDPATH.joinpath('jump.wav')
die_fx_path = SOUNDPATH.joinpath('die.wav')
checkpoint_fx_path = SOUNDPATH.joinpath('checkPoint.wav')

DINOPATH = ASSERTPATH.joinpath('Dino')
dinos = []
for i in range(1, 4):
    dinos.append(DINOPATH.joinpath(f'{i}.png'))

print(dinos)