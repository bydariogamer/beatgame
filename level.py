import pygame
from colors import neon
import random


pygame.init()
pygame.mixer.init()


class Level:
    def __init__(self, song: pygame.mixer.Sound):
        self.song = song
        self.duration = int(self.song.get_length())
        self.array = pygame.sndarray.array(self.song)
        self.blocks = []
        blocks_per_sec = 6
        sampler = len(self.array) // (self.duration * blocks_per_sec)
        for foo in range(int(self.duration * blocks_per_sec) - 1):
            self.blocks.append(self.array[foo*sampler:(foo+1)*sampler-1].mean())
        print(len(self.blocks), self.duration)
        minimum = min(self.blocks)
        new_blocks = []
        for index, block in enumerate(self.blocks):
            block -= minimum
            new_blocks.append(int(block))
        self.blocks = new_blocks
        maximum = max(self.blocks)
        new_blocks = []
        highs = 10
        for block in self.blocks:
            new_blocks.append(int(block / (maximum/highs + 1)))
        self.blocks = new_blocks
        self.obstacles = []
        self.color = pygame.color.Color(random.choice(list(neon.values())))
        self.colors = []
        block_wid = 36
        block_hei = 18
        # soft mode
        """
        for index in range(len(self.blocks)-1):
            if self.blocks[index+1]-self.blocks[index] > 2:
                self.blocks[index+1] = self.blocks[index] + 2
        """
        for index, block in enumerate(self.blocks):
            if block:
                self.obstacles.append(pygame.Rect((800+index*block_wid, 400-block_hei*block, block_wid, block_hei*block)))
                rect_color = int(random.uniform(0, 50))
                if random.random() < 0.5:
                    self.colors.append(pygame.Color(self.color) + pygame.color.Color(rect_color, rect_color, rect_color))
                else:
                    self.colors.append(pygame.Color(self.color) - pygame.color.Color(rect_color, rect_color, rect_color))

        for rect_color in self.colors:
            if rect_color.a < 255:
                rect_color.a = 255
