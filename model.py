import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import traceback

class AudioModel:
    def __init__(self, input_path):
        self.sample_rate, self.data = wavfile.read(input_path)

        if len(self.data.shape) > 1:  # Check if the audio has multiple channels
            self.data = np.mean(self.data, axis=1)  # Average the channels for simplicity

        self.freqs = np.fft.fftfreq(len(self.data), 1 / self.sample_rate)
        self.spectrum = np.fft.fft(self.data)
        self.t = np.arange(0, len(self.data) / self.sample_rate, 1 / self.sample_rate)

    def find_target_frequency(self, target_band):
        # Define frequency ranges for each band
        frequency_ranges = {
            "high": (2000, max(self.freqs)),
            "mid": (500, 2000),
            "low": (0, 500),
            "all": (0, max(self.freqs))
        }
        return frequency_ranges[target_band]

    def frequency_check(self, target_band):
        # Get the frequency range for the specified band
        min_freq, max_freq = self.find_target_frequency(target_band)

        # Find the index corresponding to the target frequency
        index_of_frequency = np.where((self.freqs >= min_freq) & (self.freqs <= max_freq))[0]

        # Extract data for the specified frequency range
        data_for_frequency = self.spectrum[index_of_frequency]

        # Convert data to dB and adjust the time array length
        data_in_db_fun = 10 * np.log10(np.abs(data_for_frequency))
        return data_in_db_fun, self.t[:len(data_in_db_fun)]

    def plot_spectrogram(self, target_band):
        try:
            if not target_band:
                raise ValueError("Target band is empty")

            # Create a new figure for the spectrogram plot
            plt.figure()

            # Get the frequency range for the specified band
            min_freq, max_freq = self.find_target_frequency(target_band)

            # Plot the spectrogram with the updated frequency range
            spectrum, freqs, t, im = plt.specgram(self.data, Fs=self.sample_rate, NFFT=1024,
                                                  cmap=plt.get_cmap('autumn_r'),
                                                  vmin=-40, vmax=40)

            plt.xlabel('Time (s)')
            plt.ylabel('Frequency (Hz)')
            plt.title(f'Spectrogram ({target_band.capitalize()} frequency range)')
            plt.colorbar(label='Intensity (dB)')

            if target_band != "all":
                # Manually select frequencies within the desired range
                min_index = int(np.searchsorted(freqs, min_freq))
                max_index = int(np.searchsorted(freqs, max_freq))
                selected_spectrum = spectrum[min_index:max_index, :]

                # Plot the spectrogram with the selected frequency range
                extent = [t.min(), t.max(), freqs[min_index], freqs[max_index]]
                plt.imshow(10 * np.log10(np.abs(selected_spectrum)), aspect='auto', origin='lower', cmap='autumn_r',
                           extent=extent, vmin=-40, vmax=40)

            else:
                # Plot the spectrogram for all frequencies
                plt.imshow(10 * np.log10(np.abs(spectrum)), aspect='auto', origin='lower', cmap='autumn_r',
                           extent=[t.min(), t.max(), 0, max_freq], vmin=-40, vmax=40)

            plt.show()

        except Exception as e:
            print(f"An error occurred in plot_spectrogram: {str(e)}")
            traceback.print_exc()
            raise  # Re-raise the exception to see the full traceback
    def plot_waveform_simple(self):
        # Create a new figure for the waveform plot
        plt.figure()

        # Plot the waveform
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
        # Get the total time in seconds and round to three decimal places
        total_seconds = round(self.t[-1], 3)
        return total_seconds

    def compute_low_rt60(self):
        low_freq_range = self.find_target_frequency("low")
        low_data, low_t = self.frequency_check("low")

        # Example: Replace this with your actual implementation for low RT60 calculation
        low_rt60_values = np.random.rand(10)  # Placeholder, replace with your code
        return low_rt60_values
    def compute_mid_rt60(self):
        mid_freq_range = self.find_target_frequency("mid")
        mid_data, mid_t = self.frequency_check("mid")

        # Example: Replace this with your actual implementation for mid RT60 calculation
        mid_rt60_values = np.random.rand(10)  # Placeholder, replace with your code
        return mid_rt60_values
    def compute_high_rt60(self):
        high_freq_range = self.find_target_frequency("high")
        high_data, high_t = self.frequency_check("high")

        # Example: Replace this with your actual implementation for high RT60 calculation
        high_rt60_values = np.random.rand(10)  # Placeholder, replace with your code
        return high_rt60_values
    def compute_combined_rt60(self):
        # Example: Replace this with your actual implementation for combining RT60 values
        combined_rt60_values = np.concatenate([
            self.compute_low_rt60(),
            self.compute_mid_rt60(),
            self.compute_high_rt60()
        ])
        return combined_rt60_values
    def calculate_and_display_difference(self):
        rt60_values = self.compute_combined_rt60()

        # Example: Replace this with your actual implementation for calculating the difference
        average_rt60 = np.mean(rt60_values)
        difference = average_rt60 - 0.5

        # Display the difference in the GUI
        self.additional_info_var.set(f"Difference: {difference:.2f} seconds")
