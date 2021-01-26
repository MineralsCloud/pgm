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
from pgm.util.unit_conversion import gpa_to_ry_b3, ry_b3_to_gpa, ry_to_j_mol, ry_to_ev, b3_to_a3
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

        out_dir = user_settings.output_directory
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        print("Caution: If negative frequencies found, they are currently treated as 0!")
        calc = FreeEnergyCalculation(user_settings)
        print("Calculating free energies")
        total_free_energies, vib_entropies, volumes, desired_pressure, continuous_temperature = calc.calculate()
        # print(desired_pressure)
        print(total_free_energies)
        print( vib_entropies)
        print("Calculating thermodynamics properties")
        thermo = ThermodynamicProperties(volumes, continuous_temperature, gpa_to_ry_b3(desired_pressure),
                                         total_free_energies)

        # self.ptv = dic['pressure']
        # self.stv = dic['entropy']
        # self.utp = dic['internal_energy']
        # self.htp = dic['enthalpy']
        # self.gtp = dic['gibbs_free_energy']
        # self.alpha_tp = dic['thermal_expansion_coefficient']
        # self.bt_tp = dic['isothermal_bulk_modulus']
        # self.gamma_tp = dic['grunesien_parameter']
        # self.bs_tp = dic['adiabatic_bulk_modulus']
        # self.cv_tp = dic['volumetric_heat_capacity']
        # self.cp_tp = dic['isobaric_heat_capacity']

        save_data(ry_to_ev(total_free_energies), continuous_temperature, b3_to_a3(volumes), out_dir + 'ftv_ev_a3')
    

        if (user_settings.ptv):
            ptv = ry_b3_to_gpa(thermo.p_tv)
            save_data(ptv, continuous_temperature, b3_to_a3(volumes), out_dir + 'ptv_gpa_K_a3')

        if (user_settings.stv):
            stv = ry_to_ev(thermo.s_tv)
            save_data(stv, continuous_temperature, b3_to_a3(volumes), out_dir + 'stv_ev_K_a3')

        if (user_settings.utp):
            utp = ry_to_ev(thermo.u_tp)
            save_data(utp, continuous_temperature, desired_pressure, out_dir + 'utp_ev_K_gpa')

        if (user_settings.htp):
            htp = ry_to_ev(thermo.h_tp)
            save_data(htp, continuous_temperature, desired_pressure, out_dir + 'htp_ev_T_gpa')

        if (user_settings.gtp):
            gtp = ry_to_ev(thermo.g_tp)
            save_data(gtp, continuous_temperature, desired_pressure, out_dir + 'gtp_ev_T_gpa')

        if (user_settings.alpha_tp):
            alpha_tp = thermo.alpha_tp
            save_data(alpha_tp, continuous_temperature, desired_pressure, out_dir + 'alpha_K_gpa')

        if (user_settings.bt_tp):
            bt_tp = ry_b3_to_gpa(thermo.bt_tp)
            save_data(bt_tp, continuous_temperature, desired_pressure, out_dir + 'bt_gpa_K_gpa')

        if (user_settings.gamma_tp):
            gamma_tp = thermo.gamma_tp
            save_data(gamma_tp, continuous_temperature, desired_pressure, out_dir + 'gamma_K_gpa')

        if (user_settings.bs_tp):
            bs_tp = ry_b3_to_gpa(thermo.bs_tp)
            save_data(bs_tp, continuous_temperature, desired_pressure, out_dir + 'bs_gpa_K_gpa')

        if (user_settings.cv_tp):
            cv = ry_to_j_mol(thermo.cv_tp)
            save_data(cv, continuous_temperature, desired_pressure, out_dir + 'cv_jmol_K_gpa')

        if (user_settings.cp_tp):
            cp = ry_to_j_mol(thermo.cp_tp)
            save_data(cp, continuous_temperature, desired_pressure, out_dir + 'cp_jmol_K_gpa')
        # bt = ry_b3_to_gpa(thermo.bt_tp)
        # alpha = thermo.alpha_tp
        # cp = ry_to_j_mol(thermo.cp_tp)
        # cv = ry_to_j_mol(thermo.cv_tp)
        # gamma = thermo.gamma_tp
        # bs = ry_b3_to_gpa(thermo.bs_tp)
        print("Saving thermodynamics properties")


