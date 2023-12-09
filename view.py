import tkinter as tk
from tkinter import filedialog, messagebox
from model import AudioModel
from controller import AudioController


class AudioView:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Processing and Plotting")

        self.input_audio_file_path = None
        self.frequency_band = tk.StringVar()
        self.controller = AudioController()

        self.create_widgets()

        # Labels for displaying results
        self.resonance_label = tk.Label(self.root, text="Highest Resonance Frequency:")
        self.resonance_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.time_label = tk.Label(self.root, text="Time Values:")
        self.time_label.grid(row=3, column=2, columnspan=2, pady=10)

    def create_widgets(self):
        # File Upload
        file_label = tk.Label(self.root, text="Select Audio File:")
        file_label.grid(row=0, column=0, pady=10)

        file_button = tk.Button(self.root, text="Browse", command=self.browse_audio_file)
        file_button.grid(row=0, column=1, pady=10)

        # Frequency Radio Buttons
        freq_label = tk.Label(self.root, text="Select Frequency Band:")
        freq_label.grid(row=1, column=0, pady=10)

        high_freq_radio = tk.Radiobutton(self.root, text="High", variable=self.frequency_band, value="high")
        high_freq_radio.grid(row=1, column=1, pady=10)

        mid_freq_radio = tk.Radiobutton(self.root, text="Mid", variable=self.frequency_band, value="mid")
        mid_freq_radio.grid(row=1, column=2, pady=10)

        low_freq_radio = tk.Radiobutton(self.root, text="Low", variable=self.frequency_band, value="low")
        low_freq_radio.grid(row=1, column=3, pady=10)

        # All frequency option
        all_freq_radio = tk.Radiobutton(self.root, text="All", variable=self.frequency_band, value="all")
        all_freq_radio.grid(row=1, column=4, pady=10)

        # Process and Plot Button for Spectrogram
        process_button = tk.Button(self.root, text="Plot Spectrogram", command=self.spectrogram_plot)
        process_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Process and Plot Button for Waveform
        waveform_button = tk.Button(self.root, text="Plot Waveform", command=self.waveform_plot)
        waveform_button.grid(row=2, column=2, columnspan=2, pady=10)

    def browse_audio_file(self):
        self.input_audio_file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.*")])

        if self.input_audio_file_path:
            try:
                # Process the audio file using the controller
                processed_file_path = self.controller.process_audio(self.input_audio_file_path)

                # Pass the processed audio file path to the AudioModel constructor
                self.model = AudioModel(processed_file_path)

                # Compute and display the highest resonance frequency
                resonance_frequency = self.model.compute_highest_resonance_frequency()
                self.resonance_label.config(text=f"Highest Resonance Frequency: {resonance_frequency:.2f} Hz")

                # Display time values
                time_values = self.model.get_time_values()
                self.time_label.config(text=f"Time Values: {time_values} seconds")

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def spectrogram_plot(self):
        if not self.input_audio_file_path:
            messagebox.showwarning("Warning", "Please select an audio file.")
            return

        try:
            # Process the audio file using the controller
            processed_file_path = self.controller.process_audio(self.input_audio_file_path)

            # Pass the processed audio file path and selected frequency to the AudioModel constructor
            self.model = AudioModel(processed_file_path)

            # Plot the spectrogram
            self.model.plot_spectrogram(self.frequency_band.get())

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def waveform_plot(self):
        if not self.input_audio_file_path:
            messagebox.showwarning("Warning", "Please select an audio file.")
            return

        try:
            # Process the audio file using the controller
            processed_file_path = self.controller.process_audio(self.input_audio_file_path)

            # Pass the processed audio file path to the AudioModel constructor
            self.model = AudioModel(processed_file_path)

            # Plot the waveform
            self.model.plot_waveform_simple()

        except Exception as e:
            messagebox.showerror("Error", str(e))
