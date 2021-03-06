import asyncio
import pygame
import os
import sys
import random

from button import Button
from player import Player
from level import Level
import colors
import config


# INITIALIZE PYGAME
pygame.init()


# WINDOW CONSTANTS
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
clock = pygame.time.Clock()

# CREATE WINDOW
pygame.display.set_caption(config.DISP_TIT)
pygame.display.set_icon(pygame.image.load(config.DISP_ICO))
display = pygame.display.set_mode((config.DISP_WID, config.DISP_HEI), pygame.RESIZABLE)
display_rect = display.get_rect()
game = pygame.Surface((config.DISP_WID, config.DISP_HEI))


def render():
    if display_rect.h != config.DISP_HEI or display_rect.w != config.DISP_WID:
        pygame.transform.scale(game, (display_rect.w, display_rect.h), display)
    else:
        display.blit(game, (0, 0))


# CONSTANTS
FONTS = {
    "normal": pygame.font.Font(config.FONT_TYPE, config.FONT_SIZE_NORMAL),
    "big": pygame.font.Font(config.FONT_TYPE, config.FONT_SIZE_BIG),
    "small": pygame.font.Font(config.FONT_TYPE, config.FONT_SIZE_SMALL),
}


def add_songs_in_folder(folder, songs, recursive=True):
    for item in os.listdir(folder):
        path = os.path.join(PATH, folder, item)
        if os.path.isfile(path):
            song_title = item.split(".")[0].replace("_", " ")
            songs.append([song_title, path])
        if recursive and os.path.isdir(path):
            print(item)
            add_songs_in_folder(path, songs, recursive)


def pager(length, cut):
    return [slice(i, min(i + cut, length)) for i in range(0, length, cut)]


SONGS = []  # [song_title, song_path]
add_songs_in_folder(os.path.join(PATH, "assets", "songs"), SONGS)

# GAME LOOP
state = "start"
player = ...


async def menu_start_loop():
    global clock, display, display_rect, game, FONTS, SONGS, state, player
    title = FONTS["big"].render(config.GAME_TITLE, False, colors.neon["blue"])
    author = FONTS["small"].render(config.GAME_AUTHOR, False, colors.neon["red"])
    author2 = FONTS["small"].render(config.GAME_AUTHOR2, False, colors.neon["red"])
    play_button = Button(
        colors.neon["fucsia"],
        300,
        200,
        200,
        70,
        image=FONTS["normal"].render("PLAY", False, (0, 0, 0)),
    )
    help_button = Button(
        colors.neon["fucsia"],
        300,
        280,
        200,
        70,
        image=FONTS["normal"].render("HELP", False, (0, 0, 0)),
    )
    exit_button = Button(
        colors.neon["fucsia"],
        300,
        360,
        200,
        70,
        image=FONTS["normal"].render("EXIT", False, (0, 0, 0)),
    )
    background = pygame.image.load(config.MENU_BACKGROUND).convert()

    # LOOP
    while state == "start":
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "close"
            if event.type == pygame.VIDEORESIZE:
                display_rect = display.get_rect()
                config.resize = (
                    float(display_rect.w) / float(config.DISP_WID),
                    float(display_rect.h) / float(config.DISP_HEI),
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "close"

        # TIME
        clock.tick(config.BASE_FPS)

        # LOGIC
        if play_button.mouseclick():
            state = "choose"
        if help_button.mouseclick():
            state = "help"
        if exit_button.mouseclick():
            state = "close"

        # RENDER
        game.fill((0, 0, 0))
        game.blit(background, (0, 0))
        game.blit(title, (90, 20))
        game.blit(author, (100, 100))
        game.blit(author2, (100, 140))
        play_button.draw(game)
        help_button.draw(game)
        exit_button.draw(game)

        # FLIP
        render()
        pygame.display.update()
        await asyncio.sleep(0)


async def menu_help_loop():
    global clock, display, display_rect, game, FONTS, SONGS, state, player

    help_page = pygame.image.load(config.HELP_IMAGE)
    help_page.set_colorkey((255, 255, 255))
    seen = False
    while state == "help":
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "close"
            if event.type == pygame.VIDEORESIZE:
                display_rect = display.get_rect()
                config.resize = (
                    display_rect.w / config.DISP_WID,
                    display_rect.h / config.DISP_HEI,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "start"
            if event.type == pygame.MOUSEBUTTONDOWN:
                seen = True
            if event.type == pygame.MOUSEBUTTONUP and seen:
                state = "start"

        # RENDER
        game.fill((240, 250, 240))
        game.blit(help_page, (0, 0))

        # FLIP
        render()
        pygame.display.update()

        # TIME
        clock.tick(config.BASE_FPS)
        await asyncio.sleep(0)


async def menu_choose_loop():
    global clock, display, display_rect, game, FONTS, SONGS, state, player

    levels = []
    page_back = Button(
        pygame.Color("darkgray"),
        10,
        config.DISP_HEI - 80,
        config.DISP_WID / 2 - 30,
        70,
        outcolor=pygame.Color("darkgray"),
        image=FONTS["normal"].render("<", False, (0, 0, 0)),
    )
    page_forward = Button(
        pygame.Color("gray"),
        20 + config.DISP_WID / 2,
        config.DISP_HEI - 80,
        config.DISP_WID / 2 - 30,
        70,
        image=FONTS["normal"].render(">", False, (0, 0, 0)),
    )
    page = 0
    pages = pager(len(SONGS), 5)
    # color = random.choice(list(colors.neon.values()))
    color = last_color = colors.neon[random.choice(list(colors.neon))]
    for song in SONGS:
        title = FONTS["normal"].render(song[0].upper(), False, (0, 0, 0))
        while color == last_color:
            color = colors.neon[random.choice(list(colors.neon))]
        last_color = color
        levels.append(
            [
                Button(
                    color,
                    10,
                    10 + 80 * (len(levels) % 5),
                    config.DISP_WID - 20,
                    70,
                    image=title,
                ),
                song[1],
                song[0].upper(),
            ]
        )
    background = pygame.image.load(config.MENU_BACKGROUND).convert()
    mouse_rel = False
    while state == "choose":

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "close"
            if event.type == pygame.VIDEORESIZE:
                display_rect = display.get_rect()
                config.resize = (
                    display_rect.w / config.DISP_WID,
                    display_rect.h / config.DISP_HEI,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "start"
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_rel = True

        # TIME
        clock.tick(config.BASE_FPS)

        # LOGIC
        for level in levels[pages[page]]:
            if level[0].mouseclick():
                try:
                    if mouse_rel:
                        player = Player(Level(pygame.mixer.Sound(level[1]), level[2]))
                        state = "level"
                        print("-level-")
                        return
                except pygame.error:
                    clic = False
                    while not clic:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                clic = True
                                state = "close"
                            if event.type == pygame.VIDEORESIZE:
                                display_rect = display.get_rect()
                                config.resize = (
                                    display_rect.w / config.DISP_WID,
                                    display_rect.h / config.DISP_HEI,
                                )
                            if (
                                event.type == pygame.KEYDOWN
                                and event.key == pygame.K_ESCAPE
                            ):
                                clic = True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                clic = True

                        clock.tick(config.BASE_FPS)
                        pygame.draw.rect(
                            game, (255, 255, 255), (20, 100, config.DISP_WID - 40, 70)
                        )
                        game.blit(
                            FONTS["small"].render(
                                "ERROR LOADING SONG, CHECK FILE FORMAT",
                                False,
                                (255, 0, 0),
                            ),
                            (30, 100),
                        )
                        render()
                        pygame.display.update()
                        await asyncio.sleep(0)

        if page_back.mouseclick() and mouse_rel:
            page -= 1
            if page < 0:
                page += 1
            else:
                pass
                # color = random.choice(list(colors.neon.values()))
                # for level in levels:
                #     level[0].color = color

            if page == 0:
                page_back.color = pygame.Color("darkgray")
                page_back.outcolor = pygame.Color("darkgray")

            if page != len(pages) - 1:
                page_forward.color = pygame.Color("gray")
                page_forward.outcolor = pygame.Color("gray") + pygame.Color(
                    15, 15, 15, 15
                )

            mouse_rel = False

        if page_forward.mouseclick() and mouse_rel:
            page += 1
            if page > len(pages) - 1:
                page -= 1
            else:
                pass
                # color = random.choice(list(colors.neon.values()))
                # for level in levels:
                #     level[0].color = color

            if page != 0:
                page_back.color = pygame.Color("gray")
                page_back.outcolor = pygame.Color("gray") + pygame.Color(15, 15, 15, 15)

            if page == len(pages) - 1:
                page_forward.color = pygame.Color("darkgray")
                page_forward.outcolor = pygame.Color("darkgray")

            mouse_rel = False

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
        await asyncio.sleep(0)


async def level_loop():
    global clock, display, display_rect, game, FONTS, SONGS, state, player

    heart = pygame.image.load(config.HEART_ICON)
    ecu = pygame.image.load(config.ECU_ICON)
    ecu.set_colorkey((255, 255, 255))
    damage = pygame.Surface((config.DISP_WID, config.DISP_HEI))
    damage.fill((20, 0, 0, 30))
    time_started = None
    lose_played = False
    lose = pygame.mixer.Sound("assets/sounds/lose.ogg")
    while state == "level":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "close"
            if event.type == pygame.VIDEORESIZE:
                display_rect = display.get_rect()
                config.resize = (
                    display_rect.w / config.DISP_WID,
                    display_rect.h / config.DISP_HEI,
                )
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "start"
                player.level.song.stop()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not player.run:
                    player.start()
                    time_started = pygame.time.get_ticks()
                player.spacebar()
        if player.ended:
            state = "start"

        # LOGIC
        if player.run:
            player.update((pygame.time.get_ticks() - time_started) / 1000)

        # RENDER
        player.draw(game)

        lifes = FONTS["small"].render(
            str(int(player.life)), False, colors.neon["orange"]
        )
        shield = FONTS["small"].render(
            str(int(player.shield)), False, colors.neon["orange"]
        )
        lifes_rect = lifes.get_rect()
        lifes_rect.topright = (700, 20)
        game.blit(lifes, lifes_rect.topleft)
        game.blit(heart, (lifes_rect.right, lifes_rect.center[1] - 14))
        game.blit(shield, (lifes_rect.left, lifes_rect.top + 30))
        game.blit(ecu, (lifes_rect.right, lifes_rect.center[1] + 16))
        score = FONTS["small"].render(
            str(int(player.score)), False, colors.neon["orange"]
        )
        combo = FONTS["small"].render(
            "  x " + str(int(player.combo)), False, colors.neon["orange"]
        )
        score_rect = score.get_rect()
        score_rect.x = 20
        score_rect.y = 20
        game.blit(score, score_rect.topleft)
        game.blit(combo, score_rect.topright)
        if not player.level.obstacles:
            end = FONTS["big"].render(config.WIN_MESSAGE, False, colors.metal["gold"])
            end_rect = end.get_rect()
            end_rect.center = (config.DISP_WID // 2, config.DISP_HEI // 2)
            game.blit(end, end_rect.topleft)
        if not player.life:
            end = FONTS["big"].render(
                config.DEATH_MESSAGE, False, colors.metal["silver"]
            )
            end_rect = end.get_rect()
            end_rect.center = (config.DISP_WID // 2, config.DISP_HEI // 2)
            game.blit(end, end_rect.topleft)
            if not lose_played:
                lose.play()
                lose_played = True

        # FLIP
        render()

        # TIME
        clock.tick(config.BASE_FPS)

        # Show
        pygame.display.update()
        await asyncio.sleep(0)
    else:
        player.save()
    await asyncio.sleep(0)


async def main():
    global clock, display, display_rect, game, FONTS, SONGS, state, player
    while state != "close":

        # EMERGENCY EXIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "close"
            if event.type == pygame.VIDEORESIZE:
                display_rect = display.get_rect()
                config.resize = (
                    display_rect.w / config.DISP_WID,
                    display_rect.h / config.DISP_HEI,
                )

        # START MENU
        if state == "start":
            await menu_start_loop()

        if state == "help":
            await menu_help_loop()

        # LEVEL SELECTOR
        if state == "choose":
            await menu_choose_loop()

        # LEVEL ITSELF
        if state == "level":
            await level_loop()
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit(0)


asyncio.run(main())
