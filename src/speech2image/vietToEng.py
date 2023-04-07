#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech2image/vietToEng.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech2image
Created Date: Friday, March 3rd 2023, 4:22:07 pm

Copyright (c) 2023 ICSLab
"""

from __future__ import absolute_import, division, print_function

import sys
from pathlib import Path

import requests

# from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # type: ignore

sys.path.append(str(Path(__file__).parent.parent))  # src folder
from _config import load_config  # noqa: E402


class VietToEng:
    def __init__(self):
        self.config = load_config(mode="speech-to-image")

        self.config = load_config(mode="speech-to-image")
        self.API_URL = self.config["vietToEng"]["URL"]
        self.headers = {
            "Authorization": "Bearer " + self.config["vietToEng"]["KEY"]
        }

    def __call__(self, vi_inputText) -> str:
        vi_inputText = vi_inputText.encode("utf-8")
        output = self._translate_vi2en(vi_inputText=vi_inputText)

        output = output[0]["generated_text"]

        return output

    def _translate_vi2en(self, vi_inputText: dict) -> str:
        reponse = requests.post(
            self.API_URL, headers=self.headers, data=vi_inputText
        )

        return reponse.json()


def main():
    vietToEng = VietToEng()
    vietToEng(vi_inputText="Hai con mèo đang bơi")


if __name__ == "__main__":
    main()
