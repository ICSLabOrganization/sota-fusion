import os
from pathlib import Path

import pygame

PARENTPATH = Path(__file__).parent
ASSETSPATH = PARENTPATH.joinpath(*["assets"])

BIRDPATH = ASSETSPATH.joinpath(*["Bird"])
CACTUSPATH = ASSETSPATH.joinpath(*["Cactus"])
DINOPATH = ASSETSPATH.joinpath(*["Dino"])
BGPATH = ASSETSPATH.joinpath(*["Other"])

RUNNING = [
    pygame.image.load(DINOPATH.joinpath(*["DinoRun1.png"])),
    pygame.image.load(DINOPATH.joinpath(*["DinoRun2.png"])),
]
JUMPING = pygame.image.load(DINOPATH.joinpath(*["DinoJump.png"]))

DUCKING = [
    pygame.image.load(DINOPATH.joinpath(*["DinoDuck1.png"])),
    pygame.image.load(DINOPATH.joinpath(*["DinoDuck2.png"])),
]

SMALL_CACTUS = [
    pygame.image.load(CACTUSPATH.joinpath(*["SmallCactus1.png"])),
    pygame.image.load(CACTUSPATH.joinpath(*["SmallCactus2.png"])),
    pygame.image.load(CACTUSPATH.joinpath(*["SmallCactus3.png"])),
]

LARGE_CACTUS = [
    pygame.image.load(CACTUSPATH.joinpath(*["LargeCactus1.png"])),
    pygame.image.load(CACTUSPATH.joinpath(*["LargeCactus2.png"])),
    pygame.image.load(CACTUSPATH.joinpath(*["LargeCactus3.png"])),
]

BIRD = [pygame.image.load(i) for i in BIRDPATH.iterdir()]

CLOUD = pygame.image.load(BGPATH.joinpath(*["Cloud.png"]))

BG = pygame.image.load(BGPATH.joinpath(*["Track.png"]))
