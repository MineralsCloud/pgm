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
    'pressure': True,
    'entropy': False,
    'internal_energy': False,
    'enthalpy': False,
    'gibbs_free_energy': False,
    'thermal_expansion_coefficient': False,
    'isothermal_bulk_modulus': False,
    'gruneisen_parameter': False,
    'adiabatic_bulk_modulus': False,
    'volumetric_heat_capacity': False,
    'isobaric_heat_capacity': False
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
        self.ptv = False
        self.stv = False
        self.utp = False
        self.htp = False
        self.gtp = False
        self.alpha_tp = False
        self.bt_tp = False
        self.gamma_tp = False
        self.bs_tp = False
        self.cv_tp = False
        self.cp_tp = False

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
            self.temperature = dic['temperature'] # Notice this is a list
            self.output_directory = dic['output_directory']
            self.continuous_temperature = np.linspace(self.temperature[0], self.temperature[-1], self.NT)
            self.desired_pressure = np.linspace(self.initP, self.finalP, self.NV)

            self.ptv = dic['pressure']
            self.stv = dic['entropy']
            self.utp = dic['internal_energy']
            self.htp = dic['enthalpy']
            self.gtp = dic['gibbs_free_energy']
            self.alpha_tp = dic['thermal_expansion_coefficient']
            self.bt_tp = dic['isothermal_bulk_modulus']
            self.gamma_tp = dic['gruneisen_parameter']
            self.bs_tp = dic['adiabatic_bulk_modulus']
            self.cv_tp = dic['volumetric_heat_capacity']
            self.cp_tp = dic['isobaric_heat_capacity']
