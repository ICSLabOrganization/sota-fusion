#!/usr/bin/env python3

'''
Filename: /home/tiendat/Workspace/Building_app/sota-fusion/src/style_transfer/neural_style.py
Path: /home/tiendat/Workspace/Building_app/sota-fusion/src/style_transfer
Created Date: Friday, April 7th 2023, 12:39:23 pm

Copyright (c) 2023 ICSLab 
'''
from __future__ import absolute_import, division, print_function

import re
import torch
import torch.onnx
from torchvision import transforms
from pathlib import Path

from .extras import utils
from .extras.transformer_net import TransformerNet


class NeuralStyle :
    def __init__(self) -> None:
        PARENT_PATH = Path(__file__).parents[2]  # root directory
        ASSETS_PATH = PARENT_PATH.joinpath("assets")

        self.IMG_PATH = ASSETS_PATH.joinpath(*["output-images", "output2.png"])
        self.MODEL_PATH = ASSETS_PATH.joinpath("styleTransfer_models")

    def _load_modelPath(self, modelName: str) -> list:
        valid_files = [f for f in self.MODEL_PATH.glob('*') if f.stem == modelName]
        
        return valid_files
    
    # check_paths and train functions are used to train models, uncomment and paste them here if you want to use
    def __call__(self, args_content_image: Path, args_model: str, args_cuda: bool):
        device = torch.device("cuda" if args_cuda else "cpu")

        # content_image = utils.load_image(args.content_image, scale=args.content_scale)
        content_image = utils.load_image(args_content_image, scale=None)
        content_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Lambda(lambda x: x.mul(255))
        ])
        content_image = content_transform(content_image)
        content_image = content_image.unsqueeze(0).to(device)

        args_model = str(self._load_modelPath(modelName=args_model)[0]) #first index 

        if args_model.endswith(".onnx"):
            output = self.stylize_onnx(content_image, args_model)
        else:
            with torch.no_grad():
                style_model = TransformerNet()
                state_dict = torch.load(args_model)
                # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
                for k in list(state_dict.keys()):
                    if re.search(r'in\d+\.running_(mean|var)$', k):
                        del state_dict[k]
                style_model.load_state_dict(state_dict)
                style_model.to(device)
                style_model.eval()
                
                output = style_model(content_image).cpu()
        return utils.save_image(self.IMG_PATH, output[0])


    def stylize_onnx(self, content_image, model):
        """
        Read ONNX model and run it using onnxruntime
        """

        import onnxruntime

        ort_session = onnxruntime.InferenceSession(model)

        def to_numpy(tensor):
            return (
                tensor.detach().cpu().numpy()
                if tensor.requires_grad
                else tensor.cpu().numpy()
            )

        ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(content_image)}
        ort_outs = ort_session.run(None, ort_inputs)
        img_out_y = ort_outs[0]

        return torch.from_numpy(img_out_y)


def main():

    neuralStyle = NeuralStyle()

    content_image = Path(__file__).parent.joinpath("lion.jpg")
    model = neuralStyle.MODEL_PATH.joinpath("mosaic.pth")
    
    use_cuda = 0
    if torch.cuda.is_available() :
        use_cuda = 1

    neuralStyle(str(content_image), str(model), use_cuda)


if __name__ == "__main__":
    main()

