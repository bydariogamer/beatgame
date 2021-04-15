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
        minimumBeatsPerSecond = 48/60.0
        maximumBeatsPerSecond = 240/60.0
        debug = True

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
                temp = maximum*(0.5 + i/length)
                result[length-i-1] = temp
            return result
        def correct_autocorrelation(autocorrelation, length):
            result = autocorrelation - default_autocorrelation(length, max(autocorrelation))
            result += max(0, -min(result)) #raise result above 0
            return result
        def argmax(signal):
            length = len(signal)
            max_index = np.argmax(signal)
            #ignore maxima at the beginning and the end
            a = 0
            b = 0
            while(max_index == 0 + a or max_index == length-1-b):
                print('maximum at the beginning or end ignored', max_index)
                if(max_index == 0 +a):
                    a +=1
                else:
                    b +=1
                max_index = np.argmax(signal[a:length-1-b]) + a
            return max_index
        autocorrelation = np.correlate(subsampled, subsampled, 'same')
        corrected_autocorr = correct_autocorrelation(autocorrelation, len_subsampled)
        
        def findBPMinRange(corrected_autocorrelation, minBPM, maxBPM):
            length = len(corrected_autocorrelation)
            firstOffset = int(1/maxBPM/self.duration*length)
            firstIndex = length//2 + firstOffset
            lastOffset = int(1/minBPM/self.duration*length)
            lastIndex = length//2 + lastOffset
            
            interestingPart = corrected_autocorrelation[firstIndex:lastIndex]
            n = 1 #uneven integer, not choosing one leads to worse results
            ddinterestingPart = np.concatenate([np.zeros(n),np.diff(np.diff(interestingPart, n), n), np.zeros(n)])/(n**2)

            indexBeatLength = argmax(interestingPart) + firstOffset
            indexBeatLength_dd = argmax(-ddinterestingPart) + firstOffset
            BPM = length/indexBeatLength*60/self.duration
            BPM_dd = length/indexBeatLength_dd*60/self.duration

            def temposAreSimilar(a,b):
                if abs(a-b) <=1:
                    return True
                if (abs(2*a-b) <= 1):
                    return True
                if (abs(a-2*b) <= 1):
                    return True
                return False
                
            if(not temposAreSimilar(indexBeatLength, indexBeatLength_dd)):
                if debug:
                    print('Non-trivial rhythm')
                    print(indexBeatLength, indexBeatLength_dd)
                    print(BPM, BPM_dd)
                    xRange = range(firstOffset, lastOffset)
                    plt.plot(xRange, interestingPart)
                    plt.plot(xRange, -ddinterestingPart)
                    plt.scatter(indexBeatLength, interestingPart[indexBeatLength - firstOffset], label=str(BPM) + ' bpm')
                    plt.scatter(indexBeatLength_dd, -ddinterestingPart[indexBeatLength_dd - firstOffset], label=str(BPM_dd) + ' bpm')
                    plt.legend()
                    plt.show()

                    xRange = range(lastOffset*2)
                    plt.plot(xRange, corrected_autocorrelation[length//2: length//2 + lastOffset*2])
                    plt.scatter(indexBeatLength, interestingPart[indexBeatLength - firstOffset], label=str(BPM) + ' bpm')
                    plt.scatter(indexBeatLength_dd, -ddinterestingPart[indexBeatLength_dd - firstOffset], label=str(BPM_dd) + ' bpm')
                    plt.legend()
                    plt.show()
                #TODO: find the right tempo by comparing the doubles of both beat lengths
                #for factor, variation in [(2, 0.1), (4, 0.03)]
            else:
                print('Tempo found:', BPM, 'bpm')

        
        findBPMinRange(corrected_autocorr, minimumBeatsPerSecond, maximumBeatsPerSecond)

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
