import numpy as np
from matplotlib import pyplot as plt
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
        
        stride = 500 # Factor for subsampling
        minimumBeatsPerSecond = 0.8
        maximumBeatsPerSecond = 4

        ## Simplify signal
        mono_signal= np.mean(self.array, 1)
        # subsample
        len_subsampled = len(mono_signal) // stride
        subsampled = np.zeros(len_subsampled)
        for i in range(len_subsampled):
            subsampled[i] = np.mean(np.abs(mono_signal[i*stride:(i+1)*stride]))
        
        ## Find Tempo / Autocorrelation
        def default_autocorrelation(length, maximum):
            result = np.zeros(length)
            for i in range(length//2 +1):
                temp = maximum*(i/length)
                result[i] = temp
                result[length-i-1] = temp
            return result
        def gaussian(x, mu, sigma):
            return (np.exp(-(x-mu)**2/2/sigma**2)/np.sqrt(2*np.pi)/sigma)
        autocorrelation = np.correlate(subsampled, subsampled, 'same')
        corrected_autocorr = autocorrelation - default_autocorrelation(len_subsampled, max(autocorrelation))
        firstIndex = len_subsampled//2 + int(1/maximumBeatsPerSecond/self.duration*len_subsampled)
        lastIndex = len_subsampled//2 + int(1/minimumBeatsPerSecond/self.duration*len_subsampled)
        interestingPart = corrected_autocorr[firstIndex:lastIndex]
        max_index_intPart = np.argmax(interestingPart)
        indexBeatLength = max_index_intPart + int(1/maximumBeatsPerSecond/self.duration*len_subsampled)
        BeatLength = indexBeatLength/len_subsampled * self.duration
        BeatsPerMinute = 60/BeatLength
        print('BPM: ', 60/BeatLength)
        plt.plot(interestingPart)
        plt.scatter(max_index_intPart, interestingPart[max_index_intPart])
        plt.show()



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
