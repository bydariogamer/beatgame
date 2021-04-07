import pygame
from colors import neon
import random


pygame.init()
pygame.mixer.init()

TEST = True

class Level:
    def __init__(self, song: pygame.mixer.Sound):
        self.song = song
        self.duration = int(self.song.get_length())
        self.array = pygame.sndarray.array(self.song)
        self.blocks = []
        sampler = len(self.array) // (self.duration * 4)   # the 2 might become a 4 or 3 if needed
        for foo in range(int(self.duration * 4) - 1):
            self.blocks.append(self.array[foo*sampler:(foo+1)*sampler-1].mean())
        minimum = min(self.blocks)
        new_blocks = []
        for block in self.blocks:
            block -= minimum
            new_blocks.append(int(block))
        self.blocks = new_blocks
        maximum = int(max(self.blocks))
        new_blocks = []
        for block in self.blocks:
            new_blocks.append(int(block) // (maximum/12 + 1))
        self.blocks = new_blocks
        self.obstacles = []
        self.color = random.choice(list(neon.values()))
        self.colors = []
        for index, block in enumerate(self.blocks):
            if block:
                self.obstacles.append([pygame.Rect((800 + index*30, 400-15*block, 10, 20*block))])
                color = int(random.uniform(0, 50))
                if random.random() < 0.5:
                    self.colors.append(pygame.Color(self.color) + pygame.color.Color(color, color, color))
                else:
                    self.colors.append(pygame.Color(self.color) - pygame.color.Color(color, color, color))


if __name__ == '__main__':
    level = Level(pygame.mixer.Sound('assets/songs/laundry_room.mp3'))
    level.gen()
    for obstacle in level.obstacles:
        print(obstacle)
    print(len(level.blocks))
    print(len(level.obstacles))
    print(len(level.colors))
