import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

class AudioModel:
    def __init__(self, input_path):
        self.sample_rate, self.data = wavfile.read(input_path)
        self.freqs = np.fft.fftfreq(len(self.data), 1/self.sample_rate)
        self.spectrum = np.fft.fft(self.data)
        self.t = np.arange(0, len(self.data)/self.sample_rate, 1/self.sample_rate)

    def find_target_frequency(self, freqs, target_band):
        if target_band == "high":
            min_freq, max_freq = 1000, max(freqs)
        elif target_band == "mid":
            min_freq, max_freq = 500, 1000
        elif target_band == "low":
            min_freq, max_freq = 0, 500
        else:
            raise ValueError("Invalid frequency band")
        for x in freqs:
            if min_freq <= x <= max_freq:
                break
        return x

    def frequency_check(self, target_band):
        target_frequency = self.find_target_frequency(self.freqs, target_band)
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        data_for_frequency = self.spectrum[index_of_frequency]

        data_in_db_fun = 10 * np.log10(np.abs(data_for_frequency))
        return data_in_db_fun, self.t[:len(data_in_db_fun)]  # Adjust the time array length

    def plot_spectogram(self, target_band):
        spectrum, freqs, t, im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Spectrogram')
        plt.colorbar(label='Intensity (dB)')
        plt.show()

        print(f'The RT60 reverb time is not applicable for spectrogram.')

    def plot_waveform_simple(self):
        plt.figure()
        plt.plot(self.t, self.data, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.grid()
        plt.show()
