from classes.speechToViet import SpeechToViet
# import vietToEngFunc, engToImgFunc

speech = SpeechToViet()

def testspeech(file : str) -> str:
    return speech.loadSpeech(file)

# engToImgFunc.engToImg(vietToEngFunc.translate(testspeech('audio-test/test.mp3')))
# print(testspeech('audio-test/test.mp3'))