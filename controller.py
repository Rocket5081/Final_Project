from pydub import AudioSegment
import os
from scipy.io import wavfile

class AudioController:
    @staticmethod
    def process_audio(input_file_path):
        try:
            # Load audio file
            audio = AudioSegment.from_file(input_file_path)

            # Convert to WAV, reduce channels to 1, and strip metadata
            mono_wav = audio.set_channels(1)
            output_file_path = "tempaudio.wav"
            mono_wav.export(output_file_path, format="wav")

            return output_file_path

        except Exception as e:
            raise RuntimeError(f"An error occurred: {str(e)}")
