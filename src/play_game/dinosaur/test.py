from pathlib import Path
import pygame
c = [i for i in Path.iterdir(Path(__file__).parent)]
d = [i for i in Path.iterdir(c[1])]

dino = [i for i in Path.iterdir(d[2])]
cactus = [i for i in Path.iterdir(d[1])]
bird = [i for i in Path.iterdir(d[0])]
bg = [i for i in Path.iterdir(d[3])]
print(bg)
RUNNING = [pygame.image.load(dino[4]),
           pygame.image.load(dino[5])]

JUMPING = pygame.image.load(dino[3])

DUCKING = [pygame.image.load(dino[1]),
            pygame.image.load(dino[2])]

SMALL_CACTUS = [pygame.image.load(cactus[3]),
                pygame.image.load(cactus[4]),
                pygame.image.load(cactus[5])]
LARGE_CACTUS = [pygame.image.load(cactus[0]),
                pygame.image.load(cactus[1]),
                pygame.image.load(cactus[2])]

BIRD = [pygame.image.load(i) for i in bird]

CLOUD = pygame.image.load(bg[0])

BG = pygame.image.load(bg[-1])
