# This file was created by: Tyler Marshall
#added this comment to prove github is listening
# importing pygame

'''
adding pngs to player and mobs, a start screen, and a win/restart screen to the game engine
'''

import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path

# added this math function to round down the clock
from math import floor



class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'cat.png')).convert_alpha(), (TILESIZE, TILESIZE))
        self.mob_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'goomba.png')).convert_alpha(), (TILESIZE, TILESIZE))
        self.boss_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'bowser.png')).convert_alpha(), (TILESIZE, TILESIZE))
        self.map_data = ['map2.txt']

        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, 'map2.txt'), 'rt') as f: 
            for line in f:
                self.map_data.append(line) 

    def __init__(self):
        # Initialize Pygame
        pg.init()
        # Set size of screen and create the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Set up the clock
        self.clock = pg.time.Clock()

    def __init__(self):
        # Initialize other attributes...
        self.doors = pg.sprite.Group()  # Initialize doors group

    def new(self):
        # Other initialization code...
        self.doors = pg.sprite.Group()  # Reset doors group when starting a new level

    def __init__(self):
        # Initialize Pygame
        pg.init()
        # Set size of screen and create the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # Initialize other attributes...

    # Create run method which runs the whole GAME    def new(self):
        self.cooldown = Timer(self)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row, self.mob_img)
                if tile == 'U':
                    PowerUp(self, col, row)
                if tile == 'B':
                    BossSprite(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.cooldown.ticking()
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH / 2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH / 2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH / 2 - 32, 120)
        pg.display.flip()
        if self.player.moneybag == 5:
            for i in range(5, 0, -1):
                self.screen.fill(BGCOLOR)
                self.draw_text(self.screen, "You won!", 64, WHITE, WIDTH / 2 - 120, HEIGHT / 2 - 32)
                self.draw_text(self.screen, f"Closing in {i} seconds...", 32, WHITE, WIDTH / 2 - 160, HEIGHT / 2 + 32)
                pg.display.flip()
                pg.time.wait(1000)
            self.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "<= Press Space to Start =>", 40, WHITE, WIDTH / 2 - 200, 250)
        pg.display.flip()
        self.wait_for_key()
        # end screen that appears after 5 coins collected and automatically closes game after countdown
    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        # draw the timer
        self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        self.draw_text(self.screen, str(self.cooldown.event_time), 24, WHITE, WIDTH/2 - 32, 80)
        self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)
        pg.display.flip()
        # Win screen after 5 coins collected
        if self.player.moneybag == 5:
            for i in range(5, 0, -1):  # Countdown from 5 to 1
                self.screen.fill(BGCOLOR)
                self.draw_text(self.screen, "You won!", 64, WHITE, WIDTH/2 - 120, HEIGHT/2 - 32)
                self.draw_text(self.screen, f"Closing in {i} seconds...", 32, WHITE, WIDTH/2 - 160, HEIGHT/2 + 32)
                pg.display.flip()
                pg.time.wait(1000)  # Wait for 1 second
            self.quit()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE:
                        waiting = False

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_start_screen()


    '''
    primary goal: add more levels and a boss fight
    
    secondary goal: add animation to sprites
    
    release verison: add graphics in the backgorund like a map to traverse around
    '''