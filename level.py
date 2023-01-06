import numpy as np
import pygame
import random
import colors
from obstacle import Obstacle
import config
import bpm_finder

if config.DEBUG_SHOW_LEVEL or config.DEBUG_BPM_FINDER:
    from matplotlib import pyplot as plt

pygame.init()
pygame.mixer.init()


class Level:
    def __init__(self, song):
        self.song = pygame.mixer.Sound(song)
        pygame.mixer.music.load(song)
        self.duration = self.song.get_length()
        self.array = pygame.sndarray.array(self.song)
        self.blocks = []

        # Find tempo of the song
        bpm = bpm_finder.get_bpm(self.array, self.duration)

        def adjust_frequency_to_aim(frequency, aim):
            while frequency < aim * 0.66:
                frequency *= 2
            while frequency > aim * 1.33:
                frequency /= 2
            return frequency

        blocks_per_sec = adjust_frequency_to_aim(
            bpm / 60.0, config.BLOCKS_PER_SECOND_AIM
        )
        print(
            "Blocks per second: ", blocks_per_sec, "that's", blocks_per_sec * 60, "bpm"
        )

        # Build map from audio
        sampler = len(self.array) // (
            self.duration * blocks_per_sec
        )  # audio samples per block
        for foo in range(int(self.duration * blocks_per_sec) - 1):
            self.blocks.append(
                np.mean(
                    np.abs(
                        self.array[int(foo * sampler) : int((foo + 1) * sampler - 1)]
                    )
                )
            )
        self.blocks = np.array(self.blocks)

        # Normalize blocks
        minimum = np.quantile(self.blocks, config.MAP_LOWER_QUANTILE)
        self.blocks -= minimum
        maximum = np.quantile(self.blocks, config.MAP_UPPER_QUANTILE)
        self.blocks *= config.HEIGHT_LEVELS / maximum
        self.blocks = self.blocks.clip(min=0, max=config.HEIGHT_LEVELS)

        # Clear space at the beginning of the song
        start_blocks = int(config.DISP_HEI / config.VELOCITY_X * blocks_per_sec)
        for i in range(start_blocks - start_blocks * 2 // 3):
            self.blocks[i] = 0  # free plain
        for i in range(
            start_blocks - start_blocks * 2 // 3, start_blocks
        ):  # ramping up to normal map
            self.blocks[i] *= i / start_blocks * 3 / 2 - 0.5

        # Quantize blocks
        self.blocks = np.round(self.blocks)

        # Show map in seperate window
        if config.DEBUG_SHOW_LEVEL:
            plt.bar(
                range(len(self.blocks)) / blocks_per_sec,
                self.blocks,
                width=1 / blocks_per_sec,
            )
            plt.legend()
            plt.show()

        # Assign graphical elements to blocks
        self.obstacles = []
        self.color = pygame.Color(random.choice(list(colors.neon.values())))
        self.colors = []
        floor_pos = config.DISP_HEI - config.FLOOR_HEIGHT
        block_hei = floor_pos / config.HEIGHT_LEVELS * config.RELATIVE_BLOCK_HEIGHT
        block_wid = config.VELOCITY_X / blocks_per_sec
        for index, block in enumerate(self.blocks):
            if block:
                self.obstacles.append(
                    Obstacle(
                        int(config.PLAYER_POS_X + index * block_wid),
                        floor_pos - block_hei * block,
                        int((index + 1) * block_wid) - int(index * block_wid),
                        block_hei * block,
                    )
                )
                rect_color = int(random.uniform(0, 50))
                if random.random() < 0.5:
                    self.colors.append(
                        pygame.Color(self.color)
                        + pygame.Color(rect_color, rect_color, rect_color)
                    )
                else:
                    self.colors.append(
                        pygame.Color(self.color)
                        - pygame.Color(rect_color, rect_color, rect_color)
                    )

        # Set gravity to the beat
        seconds_per_jump = config.JUMP_LENGTH / blocks_per_sec
        self.jump_speed = 4 * config.JUMP_HEIGHT * block_hei / seconds_per_jump
        self.gravity = 2 * self.jump_speed / seconds_per_jump
