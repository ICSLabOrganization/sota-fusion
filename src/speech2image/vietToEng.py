#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech2image/vietToEng.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech2image
Created Date: Friday, March 3rd 2023, 4:22:07 pm

Copyright (c) 2023 ICSLab
'''

from __future__ import absolute_import, division, print_function

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from _config import load_config

class VietToEng:
    def __init__(self):
        self.config = load_config()

    def __call__(self, vi_inputText: str) -> str:
        self.tokenizer_vi2en = AutoTokenizer.from_pretrained(
            self.config["LIB"]["TRANSLATOR"], src_lang="vi_VN"
        )
        self.model_vi2en = AutoModelForSeq2SeqLM.from_pretrained(
            self.config["LIB"]["TRANSLATOR"]
        )

        return self.__translate_vi2en(vi_inputText=vi_inputText)

    def __translate_vi2en(self, vi_inputText: str) -> str:
        input_ids = self.tokenizer_vi2en(
            vi_inputText, return_tensors="pt"
        ).input_ids
        output_ids = self.model_vi2en.generate(
            input_ids,
            do_sample=True,
            max_new_tokens=1024,
            top_k=100,
            top_p=0.8,
            decoder_start_token_id=self.tokenizer_vi2en.lang_code_to_id[
                "en_XX"
            ],
            num_return_sequences=1,
        )
        en_text = self.tokenizer_vi2en.batch_decode(
            output_ids, skip_special_tokens=True
        )
        en_text = " ".join(en_text)
        return en_text

def main():
    vietToEng = VietToEng()    
    vietToEng(vi_inputText="")

if __name__ == "__main__":
    main()
