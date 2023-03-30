#!/usr/bin/env python3

"""
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image/classes/engToImage.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/speech-to-image/classes
Created Date: Friday, March 3rd 2023, 4:22:07 pm

Copyright (c) 2023 ICSLab
"""
from __future__ import absolute_import, division, print_function

import io
import os
import random
import sys
import warnings
from pathlib import Path

import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation  # type: ignore
from PIL import Image
from stability_sdk import client  # type: ignore

sys.path.append(str(Path(__file__).parent.parent))  # src folder
from _config import load_config


class EngToImage:
    def __init__(self):
        PARENT_PATH = Path(__file__).parents[2]  # root directory
        ASSETS_PATH = PARENT_PATH.joinpath(*["assets", "output-images"])

        self.IMG_PATH = ASSETS_PATH.joinpath("output1.png")

        # read config file
        self.config = load_config(mode="speech-to-image")

    def __call__(self, en_inputText: str):
        os.environ["STABILITY_KEY"] = self.config["engToImage"]["STAB_KEY"]
        os.environ["STABILITY_HOST"] = self.config["engToImage"]["STAB_HOST"]

        self.stability_api = client.StabilityInference(
            key=os.environ["STABILITY_KEY"],  # API Key reference.
            verbose=True,  # Print debug messages.
            engine="stable-diffusion-v1-5",  # Set the engine to use for generation.
            # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 stable-inpainting-v1-0 stable-inpainting-512-v2-0
        )
        img = self._generateImage(en_inputText=en_inputText)

        return img

    def _generateImage(self, en_inputText: str):
        answers = self.stability_api.generate(
            prompt=en_inputText,
            seed=random.randint(100000000, 998244353),
            # If a seed is provided, the resulting generated image will be deterministic.
            # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
            # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
            steps=30,  # Amount of inference steps performed on image generation. Defaults to 30.
            cfg_scale=8.0,  # Influences how strongly your generation is guided to match your prompt.
            # Setting this value higher increases the strength in which it tries to match your prompt.
            # Defaults to 7.0 if not specified.
            # width=512, # Generation width, defaults to 512 if not included.
            # height=512, # Generation height, defaults to 512 if not included.
            samples=1,  # Number of images to generate, defaults to 1 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M  # Choose which sampler we want to denoise our generation with.
            # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
            # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again."
                    )
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(self.IMG_PATH)

                    return img


def main():
    # engToImage = EngToImage()
    # engToImage(en_inputText="two cats are dancing")
    print("Press")


if __name__ == "__main__":
    main()
