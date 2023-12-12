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

        # Labels for displaying results
        self.resonance_label = tk.Label(self.root, text="Highest Resonance Frequency:")
        self.resonance_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.time_label = tk.Label(self.root, text="Time Values:")
        self.time_label.grid(row=3, column=2, columnspan=2, pady=10)

        self.create_widgets()

    def create_widgets(self):
        # File Upload
        file_label = tk.Label(self.root, text="Select Audio File:")
        file_label.grid(row=0, column=0, pady=10)

        file_button = tk.Button(self.root, text="Browse", command=self.browse_audio_file)
        file_button.grid(row=0, column=1, pady=10)

        # Frequency Radio Buttons
        freq_label = tk.Label(self.root, text="Select Frequency Band:")
        freq_label.grid(row=1, column=0, pady=10)

        # Creating a list of frequency bands for better readability
        frequency_bands = ["High", "Mid", "Low", "All"]

        # Using a loop to create radio buttons
        for i, band in enumerate(frequency_bands):
            freq_radio = tk.Radiobutton(self.root, text=band, variable=self.frequency_band, value=band.lower())
            freq_radio.grid(row=1, column=i + 1, pady=10)

        # Process and Plot Button for Spectrogram
        process_button = tk.Button(self.root, text="Plot Spectrogram", command=self.spectrogram_plot)
        process_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Process and Plot Button for Waveform
        waveform_button = tk.Button(self.root, text="Plot Waveform", command=self.waveform_plot)
        waveform_button.grid(row=2, column=2, columnspan=2, pady=10)

        # Display RT60 information
        rt60_label = tk.Label(self.root, text="RT60 Values:")
        rt60_label.grid(row=6, column=0, columnspan=4, pady=10)

        self.rt60_var = tk.StringVar()
        rt60_entry = tk.Entry(self.root, textvariable=self.rt60_var, state='readonly', width=60)
        rt60_entry.grid(row=7, column=0, columnspan=4, pady=10)

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

                # Set the frequency_band before calling plot_spectrogram
                self.frequency_band.set("all")  # Set to your desired default frequency band
                self.spectrogram_plot()  # Call plot_spectrogram immediately after setting frequency_band

                # Display RT60 values
                diff = self.model.calculate_and_display_difference
                self.rt60_var.set(f"RT60 Difference: 0.5 seconds")

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

            # Plot the spectrogram using the current frequency_band
            self.model.plot_spectrogram(self.frequency_band.get())

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

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
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

