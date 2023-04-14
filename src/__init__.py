#!/usr/bin/env python3
# coding: utf-8

from ._version import __version__

from .daemon import VirtualControl
from .play_game import DinosaurGame
from .speech2image import EngToImage, SpeechToViet, VietToEng, recording
from .style_transfer import NeuralStyle
