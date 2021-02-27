import pygame


# INITIALIZE PYGAME
pygame.init()
pygame.mixer.init()

# WINDOW CONSTANTS
DISP_WID = 800
DISP_HEI = 500
DISP_TIT = 'BEATGAME'
DISP_ICO = pygame.image.load('assets/images/heart.png')  # change this
clock = pygame.time.Clock()

# CREATE WINDOW
pygame.display.set_caption(DISP_TIT)
pygame.display.set_icon(DISP_ICO)
game = pygame.display.set_mode((DISP_WID, DISP_HEI))

# CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FONT = pygame.font.Font("assets/fonts/8bitOperatorPlus-Bold.ttf", 64)
LIFE = pygame.image.load("assets/images/heart.png")
LIFE.set_colorkey(WHITE)
LIFE.convert()

# CLASSES
class Player:
    def __init__(self):
        self.image = pygame.image.load("assets/images/player.png")
        self.rect = self.image.get_rect()
        self.vel_x = 20
        self.vel_y = 0
        self.grav = 10


class Button:
    def __init__(self, color, x, y, width, height, outcolor=None, image=None):
        """a button with given color, position, width, heigh, a secondary color if it has mouse over and an image"""
        self.color = pygame.Color(color)
        self.rect = pygame.Rect(x, y, width, height)
        if image is not None:
            self.image = image
        else:
            self.image = None
        if outcolor is None:
            self.outcolor = self.color + pygame.Color((15, 15, 15))
        else:
            self.outcolor = outcolor

    def draw(self, window):
        # draw the button on the window
        pygame.draw.rect(window, self.color, self.rect)
        if self.mouseover():
            pygame.draw.rect(window, self.outcolor, self.rect)
        if self.image:
            window.blit(self.image, (self.rect.x + (self.rect.w/2 - self.image.get_width()/2), self.rect.y + (self.rect.h/2 - self.image.get_height()/2)))

    def mouseover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def mouseclic(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(num_buttons=3)[0]:
            return True
        else:
            return False

# GAME OBJECTS
play_button = Button((120, 120, 125, 255), 300, 200, 200, 70, image=FONT.render('PLAY', False, (0, 0, 0)))
exit_button = Button((120, 120, 125, 255), 300, 400, 200, 70, image=FONT.render('EXIT', False, (0, 0, 0)))
levels_buttons = [
    Button((120, 120, 125, 255), 150, 100, 520, 100, image=FONT.render('FIRST LEVEL', False, (0, 0, 0))),
    Button((120, 120, 125, 255), 150, 300, 520, 100, image=FONT.render('SECOND LEVEL', False, (0, 0, 0)))
]

# SONG
pygame.mixer.Sound("assets/")

# GAME LOOP
state = 'start'
while state != 'close':

    # EMERGENCY EXIT
    """for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = 'close'"""

    # START MENU
    if state == 'start':
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
            if exit_button.mouseclic():
                state = 'close'
            # RENDER
            game.fill((0, 0, 0))
            play_button.draw(game)
            exit_button.draw(game)

            # FLIP
            pygame.display.update()

    # LEVEL SELECTOR
    if state == 'choose':
        while state == 'choose':
            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = 'close'

            # TIME
            clock.tick(60)

            # RENDER
            game.fill((0, 0, 0))
            for button in levels_buttons:
                button.draw(game)

            # FLIP
            pygame.display.update()
