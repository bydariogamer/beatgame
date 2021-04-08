import pygame
import os
import sys
import random
from button import Button
from player import Player
from level import Level
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
DISP_ICO = pygame.image.load('assets/images/run1.png')
BASE_FPS = 60
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
clock = pygame.time.Clock()

# CREATE WINDOW
pygame.display.set_caption(DISP_TIT)
pygame.display.set_icon(DISP_ICO)
display = pygame.display.set_mode((DISP_WID, DISP_HEI), pygame.RESIZABLE)
display_rect = display.get_rect()
game = pygame.Surface((DISP_WID, DISP_HEI))
resize = None


def render():
    if display_rect.h != DISP_HEI or display_rect.w != DISP_WID:
        pygame.transform.scale(game, (display_rect.w, display_rect.h), display)
    else:
        display.blit(game, (0, 0))


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


def pager(length, cut):
    solution = []
    done = 0
    for _ in range(int(length/cut)):
        solution.append(slice(done, done+cut))
        done += cut
    if length % cut:
        solution.append(slice(done, done + (length % cut)))
    return solution


# GAME LOOP
state = 'start'
while state != 'close':

    # EMERGENCY EXIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = 'close'
        if event.type == pygame.VIDEORESIZE:
            display_rect = display.get_rect()
            resize = (display_rect.w / DISP_WID, display_rect.h / DISP_HEI)

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
                if event.type == pygame.VIDEORESIZE:
                    display_rect = display.get_rect()
                    resize = (float(display_rect.w) / float(DISP_WID), float(display_rect.h) / float(DISP_HEI))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'close'

            # TIME
            clock.tick(BASE_FPS)

            # LOGIC
            if play_button.mouseclic(resize=resize):
                state = 'choose'
            if help_button.mouseclic(resize=resize):
                state = 'help'
            if exit_button.mouseclic(resize=resize):
                state = 'close'

            # RENDER
            game.fill((0, 0, 0))
            game.blit(background, (0, 0))
            game.blit(title, (90, 10))
            game.blit(author, (100, 90))
            play_button.draw(game)
            help_button.draw(game)
            exit_button.draw(game)

            # FLIP
            render()
            pygame.display.update()

    if state == 'help':
        help_page = pygame.image.load('assets/images/help.png')
        help_page.set_colorkey((255, 255, 255))
        seen = False
        while state == 'help':
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'
                if event.type == pygame.VIDEORESIZE:
                    display_rect = display.get_rect()
                    resize = (display_rect.w / DISP_WID, display_rect.h / DISP_HEI)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'start'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    seen = True
                if event.type == pygame.MOUSEBUTTONUP and seen:
                    state = 'start'

            # RENDER
            game.fill((240, 250, 240))
            game.blit(help_page, (0, 0))

            # FLIP
            render()
            pygame.display.update()

            # TIME
            clock.tick(BASE_FPS)

    # LEVEL SELECTOR
    if state == 'choose':
        levels = []
        page_back = Button(pygame.color.Color('gray'), 10, DISP_HEI-80, DISP_WID/2-30, 70, image=FONT.render('<', False, (0, 0, 0)))
        page_forward = Button(pygame.color.Color('gray'), 20 + DISP_WID/2, DISP_HEI-80, DISP_WID/2-30, 70, image=FONT.render('>', False, (0, 0, 0)))
        page = 0
        pages = pager(len(SONGS), 5)
        color = random.choice(list(colors.neon.values()))
        for song in SONGS:
            title = FONT.render(song[0].upper(), False, (0, 0, 0))
            levels.append([Button(color, 10, 10 + 80*(len(levels) % 5), DISP_WID-20, 70, image=title), song[1]])

        mouse_rel = False
        while state == 'choose':

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'
                if event.type == pygame.VIDEORESIZE:
                    display_rect = display.get_rect()
                    resize = (display_rect.w / DISP_WID, display_rect.h / DISP_HEI)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'start'
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_rel = True

            # TIME
            clock.tick(BASE_FPS)

            # LOGIC
            for level in levels[pages[page]]:
                if level[0].mouseclic(resize=resize):
                    if TEST:
                        print('level', level[1])
                    try:
                        if mouse_rel:
                            player = Player(Level(pygame.mixer.Sound(level[1])))
                            if TEST:
                                print(player)
                            state = 'level'

                    except pygame.error:
                        clic = False
                        while not clic:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    clic = True
                                    state = 'close'
                                if event.type == pygame.VIDEORESIZE:
                                    display_rect = display.get_rect()
                                    resize = (display_rect.w / DISP_WID, display_rect.h / DISP_HEI)
                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    clic = True
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    clic = True

                            clock.tick(BASE_FPS)
                            pygame.draw.rect(game, (255, 255, 255), (20, 100, DISP_WID-40, 70))
                            game.blit(FONT_SMALL.render('ERROR LOADING SONG, CHECK FILE FORMAT', False, (255, 0, 0)), (30, 100))
                            render()
                            pygame.display.update()

            if page_back.mouseclic(resize=resize) and mouse_rel:
                page -= 1
                if page < 0:
                    page = 0
                mouse_rel = False
                color = random.choice(list(colors.neon.values()))
                for level in levels:
                    level[0].color = color

            if page_forward.mouseclic(resize=resize) and mouse_rel:
                page += 1
                if page > len(levels) // 5:
                    page -= 1
                mouse_rel = False
                color = random.choice(list(colors.neon.values()))
                for level in levels:
                    level[0].color = color

            # RENDER
            game.fill((0, 0, 0))
            game.blit(background, (0, 0))
            page_back.draw(game)
            page_forward.draw(game)
            for level in levels[pages[page]]:
                level[0].draw(game)

            # FLIP
            render()
            pygame.display.update()

    # LEVEL ITSELF
    if state == 'level':
        while state == 'level':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'
                if event.type == pygame.VIDEORESIZE:
                    display_rect = display.get_rect()
                    resize = (display_rect.w / DISP_WID, display_rect.h / DISP_HEI)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'start'
                    player.level.song.stop()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.spacebar()
            if player.ended:
                state = 'start'

            # LOGIC
            player.update()

            # RENDER
            player.draw(game)
            text_color = pygame.color.Color(255, 255, 255) - player.level.color
            text_color.a = 200
            lifes = FONT_SMALL.render(str(int(player.life)), False, text_color)
            lifes_rect = lifes.get_rect()
            lifes_rect.topright = (700, 20)
            game.blit(lifes, (lifes_rect.x, lifes_rect.y))

            # TIME
            clock.tick(BASE_FPS)

            # FLIP
            render()
            pygame.display.update()

pygame.quit()
sys.exit()
