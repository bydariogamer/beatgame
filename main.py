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
FONT = pygame.font.Font("assets/fonts/8bitOperatorPlus-Bold.ttf", 32)
LIFE = pygame.image.load("assets/images/heart.png")
LIFE.set_colorkey(WHITE)
LIFE.convert()


# CLASSES
class Button:
    def __init__(self, color, x, y, width, height, outcolor=None, image=None):
        """a button with given color, position, width, heigh, a secondary color if it has mouse over and an image"""
        self.color = pygame.Color(color)
        self.rect = pygame.Rect(x, y, width, height)
        if image is not None:
            self.image = image
        if outcolor is None:
            self.outcolor = self.color + pygame.Color((15, 15, 15))
        else:
            self.outcolor = outcolor

    def draw(self, window):
        # draw the button on the window
        pygame.draw.rect(window, self.color, self.rect)
        if self.mouseover():
            pygame.draw.rect(window, self.outcolor, self.rect)
        if self.image is not None:
            window.blit(self.image, (self.rect.x, self.rect.y))
            window.blit(self.image, (self.rect.x + (self.rect.w/2 - self.image.get_width()/2), self.rect.y + (self.rect.h/2 - self.image.get_height()/2)))

    def mouseover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def mouseclic(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(num_buttons=3)[0]:
            return True
        else:
            return False


state = 'menu'
while state != 'close':
    if state == 'menu':
        game.fill((0, 0, 0))


