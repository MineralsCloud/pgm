#!/usr/bin/env python3
"""
.. module cli.runner
   :platform: Unix, Windows, Mac, Linux
"""

import os
import pathlib
import time

from pgm.calculator import FreeEnergyCalculation
from pgm.data import save_data
from pgm.settings import Settings, DEFAULT_SETTINGS
from pgm.thermo import ThermodynamicProperties
from pgm.util.unit_conversion import gpa_to_ry_b3, ry_b3_to_gpa, ry_to_j_mol
from .handler import CommandHandler


class PgmRunner(CommandHandler):
    def __init__(self):
        super().__init__()

        self.settings = None
        self.start_time = None

    def init_parser(self, parser):
        super().init_parser(parser)
        parser.add_argument('settings', type=str)

    def run(self, namespace):
        start_time_total = time.time()

        user_settings = Settings(DEFAULT_SETTINGS)
        file_settings = namespace.settings
        user_settings.read_from_yaml(file_settings)

        print("Caution: If negative frequencies found, they are currently treated as 0!")
        calc = FreeEnergyCalculation(user_settings)
        print("Calculating free energies")
        total_free_energies, vib_entropies, volumes, desired_pressure, continuous_temperature = calc.calculate()
        print("Calculating thermodynamics properties")
        thermo = ThermodynamicProperties(volumes, continuous_temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)

        ptv = ry_b3_to_gpa(thermo.p_tv)
        # bt = ry_b3_to_gpa(thermo.bt_tp)
        # alpha = thermo.alpha_tp
        # cp = ry_to_j_mol(thermo.cp_tp)
        # cv = ry_to_j_mol(thermo.cv_tp)
        # gamma = thermo.gamma_tp
        # bs = ry_b3_to_gpa(thermo.bs_tp)
        print("Saving thermodynamics properties")
        out_dir = user_settings.output_directory

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        save_data(ptv, continuous_temperature, volumes, out_dir+'ptv_gpa')
        # save_data(bt, continuous_temperature, desired_pressure, out_dir + 'bttp_gpa')
