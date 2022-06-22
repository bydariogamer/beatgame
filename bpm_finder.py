import numpy as np
import config

if config.DEBUG_SHOW_LEVEL or config.DEBUG_BPM_FINDER:
    from matplotlib import pyplot as plt


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
    while max_index == a or max_index == length - 1 - b:
        if max_index == a:
            a += 1
        else:
            b += 1
        if length - a - b > 1:
            max_index = np.argmax(signal[a : length - 1 - b]) + a
        else:
            print("The only possible maximum is not fully in range!")
            a = 0
            b = 0
            max_index = np.argmax(signal)
            break
    if a + b > 0:
        print("Maximum at the beginning (", a, ") or end (", b, ") ignored")
    return max_index


def find_bpm_in_range(
    corrected_autocorrelation, min_bpm, max_bpm, duration, fine_adjust_recursion=3
):
    length = len(corrected_autocorrelation)
    first_offset = int(60 / max_bpm / duration * length)
    first_index = length // 2 + first_offset
    last_offset = int(60 / min_bpm / duration * length)
    last_index = length // 2 + last_offset

    interesting_part = corrected_autocorrelation[first_index:last_index]
    n = 1  # uneven integer, not choosing one leads to worse results
    dd_interesting_part = np.concatenate(
        [np.zeros(n), np.diff(np.diff(interesting_part, n), n), np.zeros(n)]
    ) / (
        n**2
    )  # dd is the second derivative

    index_beat_length = argmax(interesting_part) + first_offset
    index_beat_length_dd = argmax(-dd_interesting_part) + first_offset
    bpm = length / index_beat_length * 60 / duration
    bpm_dd = length / index_beat_length_dd * 60 / duration

    def tempos_are_similar(a, b):
        return abs(a - b) <= 1 or abs(2 * a - b) <= 1 or abs(a - 2 * b) <= 1

    if config.DEBUG_BPM_FINDER:
        x_range = range(first_offset, last_offset)
        plt.plot(x_range, interesting_part)
        plt.plot(x_range, -dd_interesting_part)
        x_range = range(last_offset)
        plt.plot(
            x_range, corrected_autocorrelation[length // 2 : length // 2 + last_offset]
        )
        plt.scatter(
            index_beat_length,
            interesting_part[index_beat_length - first_offset],
            label=str(bpm) + " bpm",
        )
        plt.scatter(
            index_beat_length_dd,
            -dd_interesting_part[index_beat_length_dd - first_offset],
            label=str(bpm_dd) + " bpm",
        )
        plt.legend()
        plt.show()

    if not tempos_are_similar(index_beat_length, index_beat_length_dd):
        # Compare the quality of the findings by comparing the autocorrelation for 2, 3 and 4 beats
        beats = np.array([2, 3, 4])
        scores = np.zeros(len(beats))
        scores_dd = np.zeros(len(beats))
        for i, n in enumerate(beats):
            scores[i] = corrected_autocorrelation[length // 2 + n * index_beat_length]
            scores_dd[i] = corrected_autocorrelation[
                length // 2 + n * index_beat_length_dd
            ]

        if sum(scores) > sum(scores_dd):
            rough_bpm = bpm
        else:
            rough_bpm = bpm_dd

        if config.DEBUG_BPM_FINDER:
            print(" Non-trivial rhythm")
            print("  index:", index_beat_length, index_beat_length_dd)
            print("  bpm:", bpm, bpm_dd)

            x_range = range(last_offset * 2)
            plt.plot(
                x_range,
                corrected_autocorrelation[length // 2 : length // 2 + last_offset * 2],
            )
            plt.scatter(
                index_beat_length,
                interesting_part[index_beat_length - first_offset],
                label=str(bpm) + " bpm",
            )
            plt.scatter(
                index_beat_length_dd,
                -dd_interesting_part[index_beat_length_dd - first_offset],
                label=str(bpm_dd) + " bpm",
            )
            plt.scatter(
                beats * index_beat_length, scores, label=str(bpm) + " bpm beats"
            )
            plt.scatter(
                beats * index_beat_length_dd,
                scores_dd,
                label=str(bpm_dd) + " bpm beats",
            )
            plt.legend()
            plt.show()
    else:
        rough_bpm = bpm
        if config.DEBUG_BPM_FINDER:
            print(" Tempos match: ", bpm, bpm_dd)

    if fine_adjust_recursion and (60 / rough_bpm < duration / 5):
        variation = 0.08
        if config.DEBUG_BPM_FINDER:
            print(
                "",
                fine_adjust_recursion,
                "bpm-Range",
                rough_bpm * 0.5 * (1 - variation),
                rough_bpm * 0.5 * (1 + variation),
            )
        return 2 * find_bpm_in_range(
            corrected_autocorrelation,
            rough_bpm * 0.5 * 0.95,
            rough_bpm * 0.5 * 1.05,
            duration,
            fine_adjust_recursion - 1,
        )
    else:
        return rough_bpm


def get_bpm(song, duration):
    # Simplify signal
    mono_signal = np.mean(song, 1)
    # subsample
    len_subsampled = len(mono_signal) // config.BPM_FINDER_SUBSAMPLING
    subsampled = np.zeros(len_subsampled)
    for i in range(len_subsampled):
        subsampled[i] = np.mean(
            np.abs(
                mono_signal[
                    i
                    * config.BPM_FINDER_SUBSAMPLING : (i + 1)
                    * config.BPM_FINDER_SUBSAMPLING
                ]
            )
        )
    # tempo / autocorrelation
    autocorrelation = np.correlate(subsampled, subsampled, "same")
    corrected_autocorr = correct_autocorrelation(autocorrelation, len_subsampled)
    bpm = find_bpm_in_range(
        corrected_autocorr,
        config.BPM_FINDER_MINIMUM,
        config.BPM_FINDER_MAXIMUM,
        duration,
        fine_adjust_recursion=3,
    )
    if config.DEBUG_BPM_FINDER:
        print("bpm:", bpm)
    return bpm
