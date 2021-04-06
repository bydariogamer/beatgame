import pygame


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
        new_blocks = []
        for block in self.blocks:
            block -= minimum
            new_blocks.append(int(block))
        self.blocks = new_blocks
        maximum = max(self.blocks)
        new_blocks = []
        for block in self.blocks:
            block //= (maximum/7+1)
            new_blocks.append(int(block))
        self.blocks = new_blocks


if __name__ == '__main__':
    level1 = Level(pygame.mixer.Sound('assets/songs/laundry_room.mp3'))
    level1.gen()
