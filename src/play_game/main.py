import random
import pygame
from pathlib import Path

from .objects import Ground, Dino, Cactus, Cloud, Ptera, Star

class DinosaurGame:
    def __init__(self):
        self.SCREEN = self.WIDTH, self.HEIGHT = (600, 200)
        self.FPS = 60
        
        PARENT = Path(__file__).parent
        ASSETS = PARENT.joinpath('Assets')
        
        self.start_img_path = ASSETS.joinpath('start_img.png')
        self.game_over_img_path = ASSETS.joinpath('game_over.png')
        self.replay_img_path = ASSETS.joinpath('replay.png')
        self.numbers_img_path = ASSETS.joinpath('numbers.png')
        
        SOUND = PARENT.joinpath('Sounds')
        self.jump_fx_path = SOUND.joinpath('jump.wav')
        self.die_fx_path = SOUND.joinpath('die.wav')
        self.checkpoint_fx_path = SOUND.joinpath('checkPoint.wav')

        # COLORS *********************************************************************
        self.WHITE = (225,225,225)
        self.BLACK = (0, 0, 0)
        self.GRAY = (32, 33, 36)

        # VARIABLES ******************************************************************
        self.counter = 0
        self.enemy_time = 100
        self.cloud_time = 500
        self.stars_time = 175

        self.SPEED = 5
        self.jump = False
        self.duck = False

        self.score = 0
        self.high_score = 0

        self.start_page = True
        self.mouse_pos = (-1, -1)

        self.running = True

        # CHEATCODES *****************************************************************

        # GODMODE -> immortal jutsu ( can't die )
        # DAYMODE -> Swap between day and night
        # LYAGAMI -> automatic jump and duck
        # IAMRICH -> add 10,000 to score
        # HISCORE -> highscore is 99999
        # SPEEDUP -> increase speed by 2

        self.keys = []
        self.GODMODE = False
        self.DAYMODE = False
        self.LYAGAMI = False
        
    def __call__(self):
        pygame.init()

        win = pygame.display.set_mode(self.SCREEN, pygame.NOFRAME)

        clock = pygame.time.Clock()


        # IMAGES *********************************************************************
        start_img = pygame.image.load(self.start_img_path)
        start_img = pygame.transform.scale(start_img, (60, 64))

        game_over_img = pygame.image.load(self.game_over_img_path)
        game_over_img = pygame.transform.scale(game_over_img, (200, 36))

        replay_img = pygame.image.load(self.replay_img_path)
        replay_img = pygame.transform.scale(replay_img, (40, 36))
        replay_rect = replay_img.get_rect()
        replay_rect.x = self.WIDTH // 2 - 20
        replay_rect.y = 100

        numbers_img = pygame.image.load(self.numbers_img_path)
        numbers_img = pygame.transform.scale(numbers_img, (120, 12))


        # SOUNDS *********************************************************************
        jump_fx = pygame.mixer.Sound(self.jump_fx_path)
        die_fx = pygame.mixer.Sound(self.die_fx_path)
        checkpoint_fx = pygame.mixer.Sound(self.checkpoint_fx_path)


        # OBJECTS & GROUPS ***********************************************************
        ground = Ground()
        self.dino = Dino(50, 160)

        self.cactus_group = pygame.sprite.Group()
        self.ptera_group = pygame.sprite.Group()
        self.cloud_group = pygame.sprite.Group()
        self.stars_group = pygame.sprite.Group()


        #running game
        while self.running:
            self.jump = False
            if self.DAYMODE:
                win.fill(self.WHITE)
            else:
                win.fill(self.GRAY)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False

                    if event.key == pygame.K_SPACE:
                        if self.start_page:
                            self.start_page = False
                        elif self.dino.alive:
                            self.jump = True
                            jump_fx.play()
                        else:
                            self.reset()

                    if event.key == pygame.K_UP:
                        self.jump = True
                        jump_fx.play()

                    if event.key == pygame.K_DOWN:
                        self.duck = True

                    key = pygame.key.name(event.key)
                    self.keys.append(key)
                    keys = self.keys[-7:]
                    if ''.join(keys).upper() == 'GODMODE':
                        self.GODMODE = not self.GODMODE

                    if ''.join(keys).upper() == 'DAYMODE':
                        self.DAYMODE = not self.DAYMODE

                    if ''.join(keys).upper() == 'LYAGAMI':
                        self.LYAGAMI = not self.LYAGAMI

                    if ''.join(keys).upper() == 'SPEEDUP':
                        self.SPEED += 2

                    if ''.join(keys).upper() == 'IAMRICH':
                        self.score += 10000

                    if ''.join(keys).upper() == 'HISCORE':
                        self.high_score = 99999

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.jump = False

                    if event.key == pygame.K_DOWN:
                        self.duck = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = event.pos

                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_pos = (-1, -1)

            if self.start_page:
                win.blit(start_img, (50, 100))
            else:
                ptera = Ptera(0, 0) #for preventing unbounded

                if self.dino.alive:
                    self.counter += 1
                    if self.counter % int(self.enemy_time) == 0:
                        if random.randint(1, 10) == 5:
                            y = random.choice([85, 130])
                            ptera = Ptera(self.WIDTH, y)
                            self.ptera_group.add(ptera)
                        else:
                            type = random.randint(1, 4)
                            cactus = Cactus(type)
                            self.cactus_group.add(cactus)

                    if self.counter % self.cloud_time == 0:
                        y = random.randint(40, 100)
                        cloud = Cloud(self.WIDTH, y)
                        self.cloud_group.add(cloud)

                    if self.counter % self.stars_time == 0:
                        type = random.randint(1, 3)
                        y = random.randint(40, 100)
                        star = Star(self.WIDTH, y, type)
                        self.stars_group.add(star)

                    if self.counter % 100 == 0:
                        self.SPEED += 0.1
                        self.enemy_time -= 0.5

                    if self.counter % 5 == 0:
                        self.score += 1

                    if self.score and self.score % 100 == 0:
                        checkpoint_fx.play()

                    if not self.GODMODE:
                        for cactus in self.cactus_group:
                            if self.LYAGAMI:
                                dx = cactus.rect.x - self.dino.rect.x
                                if 0 <= dx <= (70 + (self.score//100)):
                                    self.jump = True

                            if pygame.sprite.collide_mask(self.dino, cactus):
                                self.SPEED = 0
                                self.dino.alive = False
                                die_fx.play()

                        for cactus in self.ptera_group:
                            if self.LYAGAMI:
                                dx = ptera.rect.x - self.dino.rect.x
                                if 0 <= dx <= 70:
                                    if self.dino.rect.top <= ptera.rect.top:
                                        self.jump = True
                                    else:
                                        self.duck = True
                                else:
                                    self.duck = False

                            if pygame.sprite.collide_mask(self.dino, ptera):
                                self.SPEED = 0
                                self.dino.alive = False
                                die_fx.play()

                ground.update(self.SPEED)
                ground.draw(win)
                self.cloud_group.update(self.SPEED-3, self.dino)
                self.cloud_group.draw(win)
                self.stars_group.update(self.SPEED-3, self.dino)
                self.stars_group.draw(win)
                self.cactus_group.update(self.SPEED, self.dino)
                self.cactus_group.draw(win)
                self.ptera_group.update(self.SPEED-1, self.dino)
                self.ptera_group.draw(win)
                self.dino.update(self.jump, self.duck)
                self.dino.draw(win)

                string_score = str(self.score).zfill(5)
                for i, num in enumerate(string_score):
                    win.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

                if self.high_score:
                    win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
                    string_score = f'{self.high_score}'.zfill(5)
                    for i, num in enumerate(string_score):
                        win.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

                if not self.dino.alive:
                    win.blit(game_over_img, (self.WIDTH//2-100, 55))
                    win.blit(replay_img, replay_rect)

                    if replay_rect.collidepoint(self.mouse_pos):
                        self.reset()

            pygame.draw.rect(win, self.WHITE, (0, 0, self.WIDTH, self.HEIGHT), 4)
            clock.tick(self.FPS)
            pygame.display.update()

        pygame.quit()


    # FUNCTIONS ******************************************************************
    def reset(self):
        if self.score and self.score >= self.high_score:
            self.high_score = self.score

        self.counter = 0
        self.SPEED = 5
        self.score = 0

        self.cactus_group.empty()
        self.ptera_group.empty()
        self.cloud_group.empty()
        self.stars_group.empty()

        self.dino.reset()


if __name__ == '__main__':
    dinosaurGame = DinosaurGame()
    dinosaurGame()