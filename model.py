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
            min_freq, max_freq = 2000, max(freqs)
        elif target_band == "mid":
            min_freq, max_freq = 500, 2000
        elif target_band == "low":
            min_freq, max_freq = 0, 500
        else:
            raise ValueError("Invalid frequency band")
        return min_freq, max_freq

    def frequency_check(self, target_band):
        target_frequency = self.find_target_frequency(self.freqs, target_band)
        index_of_frequency = np.where(self.freqs == target_frequency)[0][0]
        data_for_frequency = self.spectrum[index_of_frequency]

        data_in_db_fun = 10 * np.log10(np.abs(data_for_frequency))
        return data_in_db_fun, self.t[:len(data_in_db_fun)]  # Adjust the time array length



    def plot_spectrogram(self, target_band):
        # Create a new figure for each spectrogram plot
        plt.figure()

        # Use find_target_frequency to get the appropriate frequency range
        if target_band == "all":
            min_freq, max_freq = 0, max(self.freqs)
        else:
            min_freq, max_freq = self.find_target_frequency(self.freqs, target_band)

        # Plot the spectrogram with the updated frequency range
        spectrum, freqs, t, im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'), vmin=-40, vmax=40)

        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title(f'Spectrogram ({target_band} frequency range)')
        plt.colorbar(label='Intensity (dB)')

        if target_band != "all":
            # Manually select frequencies within the desired range
            min_index = int(np.searchsorted(freqs, min_freq))
            max_index = int(np.searchsorted(freqs, max_freq))
            selected_spectrum = spectrum[min_index:max_index, :]

            # Plot the spectrogram with the selected frequency range
            extent = [t.min(), t.max(), freqs[min_index], freqs[max_index]]
            plt.imshow(10 * np.log10(np.abs(selected_spectrum)), aspect='auto', origin='lower', cmap='autumn_r', extent=extent, vmin=-40, vmax=40)

        else:
            # Plot the spectrogram for all frequencies
            plt.imshow(10 * np.log10(np.abs(spectrum)), aspect='auto', origin='lower', cmap='autumn_r', extent=[t.min(), t.max(), 0, max_freq], vmin=-40, vmax=40)

        plt.show()


    def plot_waveform_simple(self):
        plt.figure()
        plt.plot(self.t, self.data, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Waveform')
        plt.grid()
        plt.show()

    def compute_highest_resonance_frequency(self):
        # Find the frequency with the highest amplitude in the spectrum
        max_freq_index = np.argmax(np.abs(self.spectrum))
        highest_resonance_frequency = self.freqs[max_freq_index]
        return highest_resonance_frequency

    def get_time_values(self):
        total_seconds = self.t[-1]  # Get the total time in seconds
        rounded_duration = round(total_seconds, 3)  # Round to three decimal places
        return rounded_duration
