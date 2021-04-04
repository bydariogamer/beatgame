import pygame
import os
import sys
import random
from button import Button
from player import Player
import colors


# TEST MODE
TEST = True

# INITIALIZE PYGAME
pygame.init()
pygame.mixer.init()

# WINDOW CONSTANTS
DISP_WID = 800
DISP_HEI = 500
DISP_TIT = 'BEATGAME'
DISP_ICO = pygame.image.load('assets/images/heart.png')  # change this
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
clock = pygame.time.Clock()

# CREATE WINDOW
pygame.display.set_caption(DISP_TIT)
pygame.display.set_icon(DISP_ICO)
game = pygame.display.set_mode((DISP_WID, DISP_HEI))

# CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font("assets/fonts/8bitOperatorPlus-Bold.ttf", 48)
FONT_BIG = pygame.font.Font("assets/fonts/8bitOperatorPlus-Bold.ttf", 64)
FONT_SMALL = pygame.font.Font("assets/fonts/8bitOperatorPlus-Bold.ttf", 32)
LIFE = pygame.image.load("assets/images/heart.png")
LIFE.set_colorkey(WHITE)
LIFE = LIFE.convert()

SONGS = []
for file in os.listdir(os.path.join(PATH, 'assets', 'songs')):
    if os.path.isfile(os.path.join(PATH, 'assets', 'songs', file)):
        new_song = file.split('.')[0]
        SONGS.append([new_song.replace('_', ' '), os.path.join(PATH, 'assets', 'songs', file)])

        if TEST:
            print(SONGS)


# GAME LOOP
state = 'start'
while state != 'close':

    # EMERGENCY EXIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = 'close'

    # START MENU
    if state == 'start':
        title = FONT_BIG.render('> B E A T G A M E <', False, colors.neon['blue'])
        author = FONT_SMALL.render('bydariogamer', False, colors.neon['red'])
        play_button = Button(colors.neon['fucsia'], 300, 150, 200, 70, image=FONT.render('PLAY', False, (0, 0, 0)))
        help_button = Button(colors.neon['fucsia'], 300, 250, 200, 70, image=FONT.render('HELP', False, (0, 0, 0)))
        exit_button = Button(colors.neon['fucsia'], 300, 350, 200, 70, image=FONT.render('EXIT', False, (0, 0, 0)))
        background = pygame.image.load('assets/images/title_background.png').convert()

        # LOOP
        while state == 'start':
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'
            # TIME
            clock.tick(60)

            # LOGIC
            if play_button.mouseclic():
                state = 'choose'
            if help_button.mouseclic():
                state = 'help'
            if exit_button.mouseclic():
                state = 'close'

            # RENDER
            game.fill((0, 0, 0))
            game.blit(background, (0, 0))
            game.blit(title, (80, 10))
            game.blit(author, (90, 90))
            play_button.draw(game)
            help_button.draw(game)
            exit_button.draw(game)

            # FLIP
            pygame.display.update()

    if state == 'help':
        # TODO: help page
        pass

    # LEVEL SELECTOR
    if state == 'choose':
        levels = []
        background = pygame.image.load('assets/images/title_background.png').convert()
        for song in SONGS:
            title = FONT.render(song[0].upper(), False, (0, 0, 0))
            levels.append([Button(random.choice(list(colors.neon.values())), 300, 150, 200, 70, title), song[1]])

        while state == 'choose':
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'

            # TIME
            clock.tick(60)

            # LOGIC
            # TODO: implement menu logic

            # RENDER
            game.fill((0, 0, 0))

            for level in levels:
                level[0].draw(game)

            # FLIP
            pygame.display.update()

    # LEVEL ITSELF
    if state == 'level':
        while state == 'level':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'

pygame.quit()
sys.exit()
