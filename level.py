import pygame


pygame.init()
pygame.mixer.init()


class Level:
    def __init__(self, song: pygame.mixer.Sound):
        self.song = song
        self.duration = int(self.song.get_length())
        self.array = pygame.sndarray.array(song)
        self.blocks = []

    def gen(self):
        sampler = len(self.array) // (self.duration * 2)   # the 2 might become a 4 or 3 if needed
        for foo in range(self.duration * 2):
            self.blocks.append(self.array[foo*sampler:(foo+1)*sampler-1].mean())

