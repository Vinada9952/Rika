from pydub import AudioSegment

def GetAudioDuration(file_path):
    audio = AudioSegment.from_file(file_path)
    duration_seconds = audio.duration_seconds
    return int(f"{duration_seconds:.2f}")

# Example usage:
file_path = 'cache/output.mp3' # or .wav, .ogg, .m4a, etc.
duration = GetAudioDuration(file_path)
if duration is not None:
    print(f"Duration: {duration} seconds")
