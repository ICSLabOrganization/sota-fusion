from pathlib import Path

import sounddevice as sd  # type: ignore
from scipy.io.wavfile import write  # type: ignore

DIR_PATH = Path(__file__).parents[2]  # root directory
AUDIO_PATH = DIR_PATH.joinpath(*["assets", "audio-test", "test1.wav"])


def recording():
    fs = 16000  # Sample rate 44100 --> fix to 16000
    seconds = 3  # Duration of recording
    # Set the device to None before calling `sounddevice.InputStream`
    sd.default.device = None

    recording_obj = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(AUDIO_PATH, fs, recording_obj)  # Save as WAV file

    return AUDIO_PATH


if __name__ == "__main__":
    recording()
