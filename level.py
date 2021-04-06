import pygame
import numpy

pygame.init()
pygame.mixer.init()


class Level:
    def __init__(self, song: pygame.mixer.Sound):
        self.song = song

    def gen(self):
        self.duration = int(self.song.get_length())
        self.array = pygame.sndarray.array(self.song)
        self.blocks = []
        sampler = len(self.array) // (self.duration * 4)   # the 2 might become a 4 or 3 if needed
        for foo in range(int(self.duration * 4) - 1):
            self.blocks.append(self.array[foo*sampler:(foo+1)*sampler-1].mean())
        minimum = min(self.blocks)
        for block in self.blocks:
            block -= minimum
            block = int(block)
        maximum = max(self.blocks)
        for block in self.blocks:
            block %= (maximum/7)

