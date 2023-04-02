#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image/speechToViet.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image
Created Date: Saturday, March 4th 2023, 6:10:23 pm

Copyright (c) 2023 ICSLab
"""
from __future__ import absolute_import, division, print_function

import sys
from pathlib import Path
from typing import Union

import librosa  # type: ignore
import requests
import torch  # type: ignore
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor  # type: ignore

sys.path.append(str(Path(__file__).parent.parent))  # src folder
from _config import load_config  # noqa: E402


class SpeechToViet:
    def __init__(self):
        # get current file path
        PARENT_PATH = Path(__file__).parent
        ASSETS_PATH = PARENT_PATH.parent.parent.joinpath("assets")
        # print(ASSETS_PATH)

        self.AUDIO_PATH = ASSETS_PATH.joinpath(*["audio-test", "test1.wav"])
        # self.LIB_PATH = PARENT_PATH.joinpath("wav2vec2-base-vietnamese-250h")
        self.config = load_config(mode="speech-to-image")
        self.API_URL = self.config["speechToViet"]["URL"]
        self.headers = {
            "Authorization": "Bearer " + self.config["speechToViet"]["KEY"]
        }

    def __call__(self, audio_path: Union[str, Path] = None):  # type: ignore
        if audio_path is None:
            audio_path = self.AUDIO_PATH

        # load model and tokenizer
        output = self.__loadSpeech(audio_path=audio_path)

        return output["text"]

    def __loadSpeech(self, audio_path: Union[str, Path]) -> str:
        with open(audio_path, "rb") as f:
            data = f.read()
        response = requests.post(self.API_URL, headers=self.headers, data=data)
        return response.json()


def main():
    speechToViet = SpeechToViet()
    print(speechToViet())  # turn on to test


if __name__ == "__main__":
    main()
