from pathlib import Path, PurePath

import librosa
import soundfile as sf
import torch
import yaml
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# get current file path
DIR_PATH = Path(__file__).parent.absolute().joinpath("classes")

CONFIG_PATH = DIR_PATH.parent.absolute().joinpath("config.yml")

LIB_PATH = DIR_PATH.parent.absolute().joinpath("wav2vec2-base-vietnamese-250h")

# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)


class SpeechToViet:

    # load model and tokenizer
    processor = Wav2Vec2Processor.from_pretrained(LIB_PATH)
    model = Wav2Vec2ForCTC.from_pretrained(LIB_PATH)

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
        input_values = self.processor(
            y, return_tensors="pt", padding="longest"
        ).input_values  # Batch size 1

        # retrieve logits
        logits = self.model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)
        return transcription[0]


# print(transcription[0])
