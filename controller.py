from pydub import AudioSegment

class AudioController:
    @staticmethod
    def process_audio(input_file_path):
        try:
            # Load audio file
            audio_data = AudioSegment.from_file(input_file_path)

            # Convert to mono if stereo
            if audio_data.channels > 1:
                audio_data = audio_data.set_channels(1)

            # Convert to WAV, and strip metadata
            if not input_file_path.endswith('.wav'):
                input_file_path = input_file_path.replace(input_file_path.split('.')[-1], 'wav')
                audio_data.export(input_file_path, format='wav')

            return input_file_path

        except Exception as e:
            raise RuntimeError(f"An error occurred: {str(e)}")
