import pygame


class Obstacle(pygame.Rect):
    def __init__(self, initial_x, y, width, height):
        """A Rectangle that will move with time and has an initial position"""
        
        pygame.Rect.__init__(self, initial_x, y, width, height)
        self.initial_x = initial_x

    def updateOffset(self, offset):
        self.x = self.initial_x + offset
