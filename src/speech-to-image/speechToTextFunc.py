from pathlib import Path

from classes.speechToViet import SpeechToViet



DIR_PATH = Path(__file__).parent.absolute().joinpath("speech-to-image")

AUDIO_PATH = DIR_PATH.parent.absolute().joinpath("audio-test").joinpath("output.wav")
# AUDIO_PATH = AUDIO_PATH.joinpath("test.mp3")
# print(AUDIO_PATH)

speech = SpeechToViet()


def testspeech(file: str) -> str:
    return speech.loadSpeech(file)


# print(vietToEngFunc.translate(testspeech(AUDIO_PATH)))
# print(testspeech(AUDIO_PATH))

# enToImg = Stability()
# viToEn = VietToEng()

step1 = testspeech(AUDIO_PATH)
print(step1)

# step2 = viToEn.translate_vi2en(step1)
# print(step2)


# enToImg.generateImage(step2)
