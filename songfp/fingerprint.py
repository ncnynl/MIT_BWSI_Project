import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion
from scipy.ndimage.morphology import iterate_structure
from collections import Counter

class Fingerprint:
    def __init__(self, spectrogram, freqs, times):
        self.spectrogram = spectrogram
        self.freqs = freqs
        self.times = times
        self.peaks = self.find_peaks(self.spectrogram, self.freqs)
        self.distance = 100 #adjust as necessary
        self.fingerprint = self.process(self.peaks, self.freqs, self.times, self.distance)

    def find_peaks(self, data, freqs):
        """
        Find local peaks in a 2D array of data (from spectrogram)

        Parameters
        ----------
        data: 2D numpy array
        [potentially background: float]

        Returns
        -------
        numpy 2D array (dtype = bool)
            of the same shape as `data`. True indicates a local peak.
        """

        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, 20)  # this incorporates roughly 20 nearest neighbors
        ys, xs = np.histogram(data.flatten(), bins=data.size//2, normed=True)
        dx = xs[-1] - xs[-2]
        cdf = np.cumsum(ys)*dx  # this gives you the cumulative distribution of amplitudes
        cutoff = xs[np.searchsorted(cdf, 0.77)]

        foreground =  (data >= cutoff)
        return np.logical_and(data == maximum_filter(data, footprint = neighborhood), foreground)

    def process(self, peaks, freqs, times, distance): # No idea if this is what we need
        """
        Convert peak data to footprints

        Parameters
        ----------
        peaks: 2D numpy array of booleans
        distance: int
            maximum distance between peak pairs
        frTime: 2d numpy array of frequencies paired with times

        Returns
        -------
        numpy array with shape(N, 2), where N is the number of peak keys
            N pairs of tuples of ((f1, f2, dT), t1)

        """

        peaks_list = np.array(np.where(peaks)).T
        peaks_list = peaks_list[np.argsort(peaks_list[:, 1])]
        f = peaks_list[:, 0]
        t = peaks_list[:, 1]
        out = []
        for i in range(peaks_list.shape[0]):
            for j in range(i+1, min(peaks_list.shape[0], distance + i)):
                freq1 = f[i]
                freq2 = f[j]
                time1 = t[i]
                time2 = t[j]
                dT = np.abs(time2-time1)
                key = (freq1, freq2, dT)
                pair = (key, time1)
                out.append(pair)
        out = np.copy(out)
        return out
    def best_match(self, database): #implement
        """
        Looks through database for best match to fingerprint

        Parameters:
        database: Database
            database of songs and fingerprints

        Returns
        -------
        Song/artist/etc that best matches the fingerprint, or None if no close matches
        """
        matches = []
        match_no_time = []
        for i in range(len(self.fingerprint)):
            key = self.fingerprint[i, 0]
            time1 = self.fingerprint[i, 1]
            songs = database.music.get(key, None)
            if(songs == None):
                continue;
            else:
                for i in range(len(songs)):
                    song, time2 = songs[i]
                    toAdd = (database.songs[song], np.abs(time2-time1))
                    matches.append(toAdd)
                    match_no_time.append(database.songs[song])

        counter = Counter(matches)
        counter2 = Counter(match_no_time)
        # print(counter)
        # print(counter2)
        return counter.most_common(1)
