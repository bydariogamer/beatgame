import pygame


class Button:
    def __init__(self, color, x, y, width, height, outcolor=None, image=None):
        """a button with given color, position, width, heigh, a secondary color if it has mouse over and an image"""
        self.color = pygame.Color(color)
        self.rect = pygame.Rect(x, y, width, height)
        if image is not None:
            self.image = image
            self.image_w = self.image.get_width()
            self.image_h = self.image.get_height()
        else:
            self.image = None
        if outcolor is None:
            self.outcolor = self.color + pygame.Color((15, 15, 15, 15))
        else:
            self.outcolor = outcolor

    def draw(self, window):
        # draw the button on the window
        pygame.draw.rect(window, self.color, self.rect)
        if self.mouseover():
            pygame.draw.rect(window, self.outcolor, self.rect)
        if self.image:
            if self.image_w < self.rect.w:
                window.blit(self.image, (self.rect.x + (self.rect.w - self.image_w)/2, self.rect.y + (self.rect.h - self.image_h)/2))
            else:
                window.blit(self.image, (self.rect.x + 1, self.rect.y + (self.rect.h - self.image_h) / 2))

    def mouseover(self, resize=None):
        if resize:
            if self.rect.collidepoint(pygame.mouse.get_pos()[0]/resize[0], pygame.mouse.get_pos()[1]/resize[1]):
                return True
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            return True

    def mouseclic(self, resize=None):
        if self.mouseover(resize=resize) and pygame.mouse.get_pressed(num_buttons=3)[0]:
            return True
        else:
            return False
