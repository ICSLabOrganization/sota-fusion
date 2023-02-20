from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import soundfile as sf
import torch
import librosa

from pathlib import Path, PurePath
import yaml

# get current file path
DIR_PATH = Path(__file__).parent.absolute().joinpath("classes")

CONFIG_PATH = DIR_PATH.parent.absolute().joinpath("config.yml")

# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)

class SpeechToViet :

    # load model and tokenizer
    processor = Wav2Vec2Processor.from_pretrained(config["LIB"]["RECOGNIZER"])
    model = Wav2Vec2ForCTC.from_pretrained(config["LIB"]["RECOGNIZER"])

    # define function to read in sound file
    def map_to_array(batch):
        speech, _ = sf.read(batch["file"])
        batch["speech"] = speech
        return batch

    # load dummy dataset and read soundfiles
    # ds = map_to_array({
    #     "file": 'audio-test/test.mp3'
    # })

    def loadSpeech(self, fileLink: str) -> str:
        y, ds = librosa.load(fileLink, sr=16000)

        # tokenize
        input_values = self.processor(y, return_tensors="pt", padding="longest").input_values  # Batch size 1

        # retrieve logits
        logits = self.model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)
        return transcription[0]

# print(transcription[0])