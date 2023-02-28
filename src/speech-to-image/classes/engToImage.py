import io
import os
import random
import warnings
from pathlib import Path, PurePath

import numpy as np
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import yaml
from PIL import Image
from stability_sdk import client

# get current file path
DIR_PATH = Path(__file__).parent.absolute().joinpath("classes")

IMG_PATH = DIR_PATH.parent.absolute().joinpath("root.png")

CONFIG_PATH = DIR_PATH.parent.absolute().joinpath("config.yml")

# TODO: check path is exists
# read config file
with open(CONFIG_PATH, "r") as config_file:
    config = yaml.safe_load(config_file)


class Stability:
    # os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
    # os.environ['STABILITY_KEY'] = 'sk-ILR5A3LYbmvocBSM5pcJpq3vFCQrMcOgGB9onIKN8V15lZxx'
    # os.environ['STABILITY_KEY'] = 'sk-cHfjUwInF8Uuds4AS77mGm3HQWuwXkl5N64o6XwfxkKVcWRh'
    os.environ["STABILITY_KEY"] = config["engToImage"]["STAB_KEY"]
    os.environ["STABILITY_HOST"] = config["engToImage"]["STAB_HOST"]
    stability_api = client.StabilityInference(
        key=os.environ["STABILITY_KEY"],  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-v1-5",  # Set the engine to use for generation.
        # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 stable-inpainting-v1-0 stable-inpainting-512-v2-0
    )
    # def __init__(self) :

    def generateImage(self, string):
        answers = self.stability_api.generate(
            prompt=string,
            seed=random.randint(
                100000000, 998244353
            ),  # If a seed is provided, the resulting generated image will be deterministic.
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
                    # img.save(str(artifact.seed)+ ".png") # Save our generated images with their seed number as the filename.
                    img.save(IMG_PATH)
                    # mask = np.array(img.convert('L'))
                    # print(mask)
                    return IMG_PATH
                    # img.show()
                    # return img
