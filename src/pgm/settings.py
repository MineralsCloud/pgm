#!/usr/bin/env python3
"""
.. module settings
   :platform: Unix, Windows, Mac, Linux
"""

import collections
from typing import Any, Dict, Tuple, Union
import numpy as np
import yaml

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

    # def __init__(self, filename: str):
    # if not filename.endswith('.yaml'):
    #     filename += '.yaml'
    # with open(filename, 'w') as f:
    #     dic = yaml.load(f)
    #
    # self.NV = dic['NV']
    # self.NT = dic['NT']
    # self.folder = dic['folder']
    # self.initP = dic['initP']
    # self.finalP = dic['finalP']
    # self.ratio = dic['ratio']
    # self.temperature = dic['temperature']
    # self.output_directory = dic['output_directory']
    # self.continuous_temperature = np.linspace(self.temperature[0], self.temperature[-1], self.NT)
    # self.desired_pressure = np.linspace(self.initP, self.finalP, self.NV)
    def __init__(self, DEFAULT_SETTINGS):
        self.NV = DEFAULT_SETTINGS['NV']
        self.NT = DEFAULT_SETTINGS['NT']
        self.folder = DEFAULT_SETTINGS['folder']
        self.initP = DEFAULT_SETTINGS['initP']
        self.finalP = DEFAULT_SETTINGS['finalP']
        self.ratio = DEFAULT_SETTINGS['ratio']
        self.temperature = DEFAULT_SETTINGS['temperature']
        self.output_directory = DEFAULT_SETTINGS['output_directory']
        self.continuous_temperature = np.zeros(1)
        self.desired_pressure = np.zeros(1)

    def read_from_yaml(self, filename: str):
        if not filename.endswith('.yaml'):
            filename += '.yaml'
        with open(filename, 'w') as f:
            dic = yaml.load(f)

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
