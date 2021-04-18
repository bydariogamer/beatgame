import numpy as np
from matplotlib import pyplot as plt
import pygame
from colors import neon
from obstacle import Obstacle
import random


pygame.init()
pygame.mixer.init()


class Level:
    def __init__(self, song: pygame.mixer.Sound, song_name):
        self.song = song
        self.song_name = song_name
        self.duration = self.song.get_length()
        self.array = pygame.sndarray.array(self.song)
        self.blocks = []

        self.pixels_per_sec = 240   # Movement in x direction in pixels per second.
        
        stride = 500    # Factor for subsampling
        minimumBeatsPerMinute= 48
        maximumBeatsPerMinute = 240
        debugTempoFinder = False
        debugLevelGeneration = False
        aim_blocksPerSecond = 4
        heightLevels = 10
        start_Offset = 800 # see DISP_WID 
        player_pos_x = 70

        # Find Tempo / Autocorrelation
        # Simplify signal
        mono_signal= np.mean(self.array, 1)
        # subsample
        len_subsampled = len(mono_signal) // stride
        subsampled = np.zeros(len_subsampled)
        for i in range(len_subsampled):
            subsampled[i] = np.mean(np.abs(mono_signal[i*stride:(i+1)*stride]))
        # tempo / autocorrelation

        def default_autocorrelation(length, maximum):
            result = np.zeros(length)
            for i in range(length // 2 + 1):
                temp = maximum * (0.5 + i / length)
                result[length - i - 1] = temp
            return result

        def correct_autocorrelation(autocorrelation, length):
            result = autocorrelation - default_autocorrelation(length, max(autocorrelation))
            result += max(0, -min(result))  # raise result above 0
            return result

        def argmax(signal):
            length = len(signal)
            max_index = np.argmax(signal)
            # ignore maxima at the beginning and the end
            a = 0
            b = 0
            while max_index == 0 + a or max_index == length-1-b:
                if max_index == 0 +a:
                    a += 1
                else:
                    b += 1
                if length - a - b > 1:
                    max_index = np.argmax(signal[a:length-1-b]) + a
                else:
                    print('The only possible maximum is not fully in range!')
                    a = 0
                    b = 0
                    max_index = np.argmax(signal)
                    break
            if a+b > 0:
                print('Maximum at the beginning (', a, ') or end (', b, ') ignored')
            return max_index

        def findBPMinRange(corrected_autocorrelation, minBPM, maxBPM, fineAdjustRecursion=3):
            length = len(corrected_autocorrelation)
            firstOffset = int(60/maxBPM/self.duration*length)
            firstIndex = length//2 + firstOffset
            lastOffset = int(60/minBPM/self.duration*length)
            lastIndex = length//2 + lastOffset
            
            interestingPart = corrected_autocorrelation[firstIndex:lastIndex]
            n = 1   # uneven integer, not choosing one leads to worse results
            ddinterestingPart = np.concatenate([np.zeros(n),np.diff(np.diff(interestingPart, n), n), np.zeros(n)])/(n**2)

            indexBeatLength = argmax(interestingPart) + firstOffset
            indexBeatLength_dd = argmax(-ddinterestingPart) + firstOffset
            BPM = length/indexBeatLength*60/self.duration
            BPM_dd = length/indexBeatLength_dd*60/self.duration

            def temposAreSimilar(a, b):
                if abs(a - b) <= 1:
                    return True
                if abs(2 * a - b) <= 1:
                    return True
                if abs(a - 2 * b) <= 1:
                    return True
                return False
            
            if debugTempoFinder:
                xRange = range(firstOffset, lastOffset)
                plt.plot(xRange, interestingPart)
                plt.plot(xRange, -ddinterestingPart)
                xRange = range(lastOffset)
                plt.plot(xRange, corrected_autocorrelation[length//2: length//2 + lastOffset])           
                plt.scatter(indexBeatLength, interestingPart[indexBeatLength - firstOffset], label=str(BPM) + ' bpm')
                plt.scatter(indexBeatLength_dd, -ddinterestingPart[indexBeatLength_dd - firstOffset], label=str(BPM_dd) + ' bpm')
                plt.legend()
                plt.show()

            if not temposAreSimilar(indexBeatLength, indexBeatLength_dd):
                # for a valid tempo half the tempo will also have a good autocorrelation
                score = corrected_autocorrelation[length//2 + 2*indexBeatLength]
                score_dd = corrected_autocorrelation[length//2 + 2*indexBeatLength_dd]                
                if score > score_dd:
                    rough_BPM = BPM
                else:
                    rough_BPM = BPM_dd

                if debugTempoFinder:
                    print(' Non-trivial rhythm')
                    print('  index:', indexBeatLength, indexBeatLength_dd)
                    print('  bpm:', BPM, BPM_dd)

                    xRange = range(lastOffset*2)
                    plt.plot(xRange, corrected_autocorrelation[length//2: length//2 + lastOffset*2])
                    plt.scatter(indexBeatLength, interestingPart[indexBeatLength - firstOffset], label=str(BPM) + ' bpm')
                    plt.scatter(indexBeatLength_dd, -ddinterestingPart[indexBeatLength_dd - firstOffset], label=str(BPM_dd) + ' bpm')
                    plt.scatter(2*indexBeatLength, score, label=str(0.5*BPM) + ' bpm')
                    plt.scatter(2*indexBeatLength_dd, score_dd, label=str(0.5*BPM_dd) + ' bpm')
                    plt.legend()
                    plt.show()
            else:
                rough_BPM = BPM
                if debugTempoFinder:
                    print(' Tempos match: ', BPM, BPM_dd)

            if fineAdjustRecursion and (60/rough_BPM < self.duration/5):
                variation = 0.08
                if debugTempoFinder:
                    print('', fineAdjustRecursion, 'BPM-Range', rough_BPM*0.5*(1-variation), rough_BPM*0.5*(1+variation))
                return 2*findBPMinRange(corrected_autocorrelation, rough_BPM*0.5*0.95, rough_BPM*0.5*1.05, fineAdjustRecursion-1)
            else:
                return rough_BPM

        autocorrelation = np.correlate(subsampled, subsampled, 'same')
        corrected_autocorr = correct_autocorrelation(autocorrelation, len_subsampled)
        BPM = findBPMinRange(corrected_autocorr, minimumBeatsPerMinute, maximumBeatsPerMinute, fineAdjustRecursion=3)
        if debugTempoFinder:
            print('BPM:', BPM)
        
        blocks_per_sec = BPM/60.
        while blocks_per_sec < aim_blocksPerSecond*0.66:
            blocks_per_sec *= 2
        while blocks_per_sec > aim_blocksPerSecond*1.33:
            blocks_per_sec /= 2
        print('Blocks per second: ', blocks_per_sec, 'that\'s', blocks_per_sec*60, 'bpm')

        # Build Map from audio
        sampler = len(self.array) // (self.duration * blocks_per_sec) # audio samples per block
        for foo in range(int(self.duration * blocks_per_sec) - 1):
            self.blocks.append(np.mean(np.abs(self.array[int(foo*sampler):int((foo+1)*sampler-1)])))
        self.blocks = np.array(self.blocks)

        # Normalize blocks
        minimum = np.quantile(self.blocks, 0.05)
        self.blocks -= minimum
        maximum = np.quantile(self.blocks, 0.95)
        self.blocks *= heightLevels/maximum
        self.blocks = self.blocks.clip(min=0, max=heightLevels)
        # Clear space at the beginning of the song
        start_Blocks = int(start_Offset/self.pixels_per_sec*blocks_per_sec)
        for i in range(start_Blocks-start_Blocks*2//3):
            self.blocks[i] = 0 # free plain
        for i in range(start_Blocks-start_Blocks*2//3, start_Blocks): # ramping up to normal map
            self.blocks[i] *= float(i)/start_Blocks*3/2-0.5
        # Quantize Blocks
        self.blocks = np.round(self.blocks)
        
        # Show map in seperate window
        if debugLevelGeneration:
            plt.bar(range(len(self.blocks))/blocks_per_sec, self.blocks, width=1/blocks_per_sec)
            plt.legend()
            plt.show()

        # Assign graphical elements to blocks
        self.obstacles = []
        self.color = pygame.color.Color(random.choice(list(neon.values())))
        self.colors = []
        block_wid = self.pixels_per_sec/blocks_per_sec
        block_hei = 18

        for index, block in enumerate(self.blocks):
            if block:
                self.obstacles.append(Obstacle(int(player_pos_x + index*block_wid), 400-block_hei*block, int(block_wid), block_hei*block))
                rect_color = int(random.uniform(0, 50))
                if random.random() < 0.5:
                    self.colors.append(pygame.Color(self.color) + pygame.color.Color(rect_color, rect_color, rect_color))
                else:
                    self.colors.append(pygame.Color(self.color) - pygame.color.Color(rect_color, rect_color, rect_color))

        for rect_color in self.colors:
            if rect_color.a < 255:
                rect_color.a = 255
