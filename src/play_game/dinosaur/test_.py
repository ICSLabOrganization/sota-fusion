import os
import random
from pathlib import Path
import sys
import pygame

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class Play():
    def __init__(self):
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        self.clock = pygame.time.Clock()
        self.player = Dinosaur()
        self.cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        obstacles = []
        self.death_count = 0
        self.run = True 
    def __config(self):
        def _score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1
            
            text = self.font.render("Points " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)
        def _background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed
        while self.run:
            if self.death_count == 0:
                text = self.font.render("Press Space to Start", True, (0, 0, 0))
            elif self.death_count > 0:
                text = self.font.render("Press Space to Restart", True, (0, 0, 0))
                score = self.font.render("Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(
            RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140)
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()
            self.player.draw(SCREEN)
            self.player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))
            
            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if self.player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(200)
                    self.death_count += 1
                    self.play(self.death_count)
            _background()
            self.cloud.draw(SCREEN)
            self.cloud.update()
            _score()
            self.clock.tick(40)
            pygame.display.update()
        pygame.quit()
    def play(self, death_count = 0):
        global points
        self.run = True
        while self.run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font("freesansbold.ttf", 30)

            if death_count == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(
                RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140)
            )
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.__config()
        pygame.quit()

play = Play()
play.play()