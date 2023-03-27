#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image/speechToViet.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image
Created Date: Saturday, March 4th 2023, 6:10:23 pm

Copyright (c) 2023 ICSLab
'''
from __future__ import absolute_import, division, print_function

from pathlib import Path

import torch #type: ignore
import librosa #type: ignore
from typing import Union

from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor #type: ignore


class SpeechToViet:
    def __init__(self):
        # get current file path
        PARENT_PATH = Path(__file__).parent
        ASSETS_PATH = PARENT_PATH.joinpath("assets")

        self.AUDIO_PATH = ASSETS_PATH.joinpath(*["audio-test", "test1.wav"])
        self.LIB_PATH = PARENT_PATH.joinpath("wav2vec2-base-vietnamese-250h")

    def __call__(self, audio_path: Union[str, Path] = None): # type: ignore
        if audio_path is None:
            audio_path = self.AUDIO_PATH

        # load model and tokenizer
        self.processor = Wav2Vec2Processor.from_pretrained(self.LIB_PATH)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.LIB_PATH)

        return self.__loadSpeech(audio_path=audio_path)


    def __loadSpeech(self, audio_path: Union[str, Path]) -> str:
        y, _ = librosa.load(audio_path, sr=16000)

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


def main():
    speechToViet = SpeechToViet()    
    speechToViet()

if __name__ == "__main__":
    main()
