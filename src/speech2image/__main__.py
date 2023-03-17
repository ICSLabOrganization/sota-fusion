from .recording import recording
from .speechToViet import SpeechToViet
from .vietToEng import VietToEng
from .engToImage import EngToImage

class TextToImage :
    def __init__(self) -> None:
        self.engToImageObj = EngToImage()
        self.vietToEngObj = VietToEng()
    
    def __call__(self, input : str) :
        input = self.vietToEngObj(input)
        input = self.engToImageObj(input)
        return input
    
class SpeechToText :
    def __init__(self) -> None:
        self.speechToVietObj = SpeechToViet()
    
    def __call__(self) :
        output = recording()
        output = self.speechToVietObj(output)
        return output