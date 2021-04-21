import numpy as np
from matplotlib import pyplot as plt
import config

# Find the tempo (Beats Per Minute) of a song (assuming constant tempo)

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
    while max_index == a or max_index == length-1-b:
        if max_index == a:
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

def findBPMinRange(corrected_autocorrelation, minBPM, maxBPM, duration, fineAdjustRecursion=3):
    length = len(corrected_autocorrelation)
    firstOffset = int(60/maxBPM/duration*length)
    firstIndex = length//2 + firstOffset
    lastOffset = int(60/minBPM/duration*length)
    lastIndex = length//2 + lastOffset
    
    interestingPart = corrected_autocorrelation[firstIndex:lastIndex]
    n = 1   # uneven integer, not choosing one leads to worse results
    ddinterestingPart = np.concatenate([np.zeros(n),np.diff(np.diff(interestingPart, n), n), np.zeros(n)])/(n**2) # dd is the second derivative

    indexBeatLength = argmax(interestingPart) + firstOffset
    indexBeatLength_dd = argmax(-ddinterestingPart) + firstOffset
    BPM = length/indexBeatLength*60/duration
    BPM_dd = length/indexBeatLength_dd*60/duration

    def temposAreSimilar(a, b):
        if abs(a - b) <= 1:
            return True
        if abs(2 * a - b) <= 1:
            return True
        if abs(a - 2 * b) <= 1:
            return True
        return False
    
    if config.DEBUG_BPM_FINDER:
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
        # Compare the quality of the findings by comparing the autocorrelation for 2, 3 and 4 beats
        beats = np.array([2, 3, 4])
        scores = np.zeros(len(beats))
        scores_dd = np.zeros(len(beats))
        for i, n in enumerate(beats):
            scores[i] = corrected_autocorrelation[length//2 + n*indexBeatLength]
            scores_dd[i] = corrected_autocorrelation[length//2 + n*indexBeatLength_dd]  
         
        if sum(scores) > sum(scores_dd):
            rough_BPM = BPM
        else:
            rough_BPM = BPM_dd

        if config.DEBUG_BPM_FINDER:
            print(' Non-trivial rhythm')
            print('  index:', indexBeatLength, indexBeatLength_dd)
            print('  bpm:', BPM, BPM_dd)

            xRange = range(lastOffset*2)
            plt.plot(xRange, corrected_autocorrelation[length//2: length//2 + lastOffset*2])
            plt.scatter(indexBeatLength, interestingPart[indexBeatLength - firstOffset], label=str(BPM) + ' bpm')
            plt.scatter(indexBeatLength_dd, -ddinterestingPart[indexBeatLength_dd - firstOffset], label=str(BPM_dd) + ' bpm')
            plt.scatter(beats*indexBeatLength, scores, label=str(BPM) + ' bpm beats')
            plt.scatter(beats*indexBeatLength_dd, scores_dd, label=str(BPM_dd) + ' bpm beats')
            plt.legend()
            plt.show()
    else:
        rough_BPM = BPM
        if config.DEBUG_BPM_FINDER:
            print(' Tempos match: ', BPM, BPM_dd)

    if fineAdjustRecursion and (60/rough_BPM < duration/5):
        variation = 0.08
        if config.DEBUG_BPM_FINDER:
            print('', fineAdjustRecursion, 'BPM-Range', rough_BPM*0.5*(1-variation), rough_BPM*0.5*(1+variation))
        return 2*findBPMinRange(corrected_autocorrelation, rough_BPM*0.5*0.95, rough_BPM*0.5*1.05, duration, fineAdjustRecursion-1)
    else:
        return rough_BPM

def getBPM(song, duration):
    # Simplify signal
    mono_signal= np.mean(song, 1)
    # subsample
    len_subsampled = len(mono_signal) // config.BPM_FINDER_SUBSAMPLING
    subsampled = np.zeros(len_subsampled)
    for i in range(len_subsampled):
        subsampled[i] = np.mean(np.abs(mono_signal[i*config.BPM_FINDER_SUBSAMPLING:(i+1)*config.BPM_FINDER_SUBSAMPLING]))
    # tempo / autocorrelation
    autocorrelation = np.correlate(subsampled, subsampled, 'same')
    corrected_autocorr = correct_autocorrelation(autocorrelation, len_subsampled)
    BPM = findBPMinRange(corrected_autocorr, config.BPM_FINDER_MINIMUM, config.BPM_FINDER_MAXIMUM, duration, fineAdjustRecursion=3)
    if config.DEBUG_BPM_FINDER:
        print('BPM:', BPM)
    return BPM