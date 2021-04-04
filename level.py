import pygame


pygame.init()
pygame.mixer.init()

class Level:
    def __init__(self, song):
        self.song = song
        self.array = pygame.sndarray(song)

    def gen(self):
        pass
