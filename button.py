import pygame


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
            window.blit(self.image, (self.rect.x + (self.rect.w - self.image.get_width())/2, self.rect.y + (self.rect.h - self.image.get_height())/2))

    def mouseover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def mouseclic(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed(num_buttons=3)[0]:
            return True
        else:
            return False