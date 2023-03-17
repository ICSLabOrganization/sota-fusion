import sounddevice as sd
from scipy.io.wavfile import write

from pathlib import Path

DIR_PATH = Path(__file__).parent.joinpath("speech-2-image")
AUDIO_PATH = DIR_PATH.parent.joinpath("assets").joinpath("audio-test").joinpath("test1.wav")

def recording():
    fs = 16000  # Sample rate 44100 --> fix to 16000
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(AUDIO_PATH, fs, myrecording)  # Save as WAV file 
    # return AUDIO_PATH


if __name__ == "__main__":
    recording()

