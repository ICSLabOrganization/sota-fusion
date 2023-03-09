import sounddevice as sd
from scipy.io.wavfile import write

from pathlib import Path

DIR_PATH = Path(__file__).parent.joinpath("speech-to-image")
AUDIO_PATH = DIR_PATH.parent.joinpath("audio-test").joinpath("test1.wav")

def main():
    fs = 16000  # Sample rate 44100 --> fix to 16000
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(AUDIO_PATH, fs, myrecording)  # Save as WAV file 


if __name__ == "__main__":
    main()

