#!/usr/bin/env python3
"""
.. module settings
   :platform: Unix, Windows, Mac, Linux
"""

import collections
from typing import Any, Dict, Tuple, Union
import numpy as np
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


# ===================== What can be exported? =====================
__all__ = ['DEFAULT_SETTINGS', 'Settings']

DEFAULT_SETTINGS: Dict[str, Any] = {
    'NV': 501,
    'NT': 251,
    'folder': 'dir/%sK.txt',
    'initP': 0,
    'finalP': 500,
    'ratio': 1.2,
    'temperature': [1500, 2000, 2500, 3000, 3500, 4000],
    'output_directory': './results/',
}


class Settings:
    """
    Read settings from a yaml file
    """
    def __init__(self, dic: Dict):
        self.NV = dic['NV']
        self.NT = dic['NT']
        self.folder = dic['folder']
        self.initP = dic['initP']
        self.finalP = dic['finalP']
        self.ratio = dic['ratio']
        self.temperature = dic['temperature']
        self.output_directory = dic['output_directory']
        self.continuous_temperature = np.linspace(self.temperature[0], self.temperature[-1], self.NT)
        self.desired_pressure = np.linspace(self.initP, self.finalP, self.NV)

    def read_from_yaml(self, filename: str):
        if not filename.endswith('.yaml'):
            filename += '.yaml'
        with open(filename, 'r') as f:
            dic = yaml.load(f, Loader=Loader)
            # print(dic)
            self.NV = dic['NV']
            self.NT = dic['NT']
            self.folder = dic['folder']
            self.initP = dic['initP']
            self.finalP = dic['finalP']
            self.ratio = dic['ratio']
            self.temperature = dic['temperature']
            self.output_directory = dic['output_directory']
            self.continuous_temperature = np.linspace(self.temperature[0], self.temperature[-1], self.NT)
            self.desired_pressure = np.linspace(self.initP, self.finalP, self.NV)
