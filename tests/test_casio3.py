# from sqha.config import color_list, cmb_list, cmy_list
# import matplotlib.pyplot as plt
# from qha.unit_conversion import *
# from qha.tools import find_nearest, find_value
# from sqha.sqha import sqha, spline_interpolation, calculator
# from sqha.thermo import Thermodynamics_properties
# import numpy as np
# from sqha.figplot import *
# from sqha.data import make_unit_converter
# import pandas as pd
# from qha.thermodynamics import calculate_derivatives
# from sqha.data import save_line

# from scipy.interpolate import interp1d
# from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.pyplot as plt
from pgm.util.unit_conversion import gpa_to_ry_b3, ry_b3_to_gpa, ry_to_j_mol, ry_to_ev, b3_to_a3
from pgm.util.tools import find_value
from pgm.calculator import pgm, spline_interpolation, qha, FreeEnergyCalculation
from pgm.thermo import ThermodynamicProperties
from pgm.data import save_data
from pgm.reader.read_input import Input
import numpy as np

if __name__ == "__main__":
    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 22}

    # mpl.rc('font', **font)
    mpl.rcParams['axes.linewidth'] = 1.8
    # mpl.rcParams['mathtext.fontset'] = 'stix'

    NV = 501
    NT = 251
    folder = 'data/casio3/%sK.txt'
    initP = 0
    finalP = 500
    ratio = 1.2  # must be the same as qha input


    discrete_temperatures = [1500, 2000, 2500, 3000, 3500, 4000]
    temperature = np.linspace(1500, 4000, NT)

    temp_list = list(temperature)

    desired_pressure = np.linspace(0, 500, NV)
    # folder = 'data/output/%sK/input.txt'


    # vib_energies, vib_entropies = sqha(
    #     len(desired_pressure), ratio, discrete_temperatures, temperature, folder)
    # volumes, energies, static_energies = calculator(
    #     len(desired_pressure), ratio, discrete_temperatures, folder)

    calc = FreeEnergyCalculation(NV, NT, initP, finalP, ratio, discrete_temperatures, folder)
    total_free_energies, vib_entropies, volumes, desired_pressure, continuous_temperature = calc.calculate()
    # thermo = ThermodynamicProperties(volumes, temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)
    sqha_volume = b3_to_a3(volumes)

    # energies[0] = energies[1]

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # static_free_energies, interpolated_volumes = spline_interpolation(
    #     volumes, static_energies, discrete_temperatures, temperature)
    #
    # s0T = 1500 * np.array(vib_entropies[0, :])
    # total_free_energies -= np.array([list(s0T)] * NT)
    #
    # sqha_volume = b3_to_a3(interpolated_volumes[0])
    #
    # interpolation = Thermodynamics_properties(
    #     sqha_volume, temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)

    ##### copy above stuff ######
    ### thermodynamic properties: [interpolation.cv_tp, interpolation.bt_tv, interpolations.cp_tp, interpolations.gamma_tp, interpolations. alpha_tp,...]
    ### i.e.   plt.plot(sqha_volume,static.cp_tv[find_value(temperature,2000)]) ## draw the cp as a function of T and V, at 2000 K.

    plt.figure(figsize=(5, 4))

    v = 44.39
    index_v = find_value(v, sqha_volume)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v]), lw=3, label="V1")

    plt.scatter(discrete_temperatures,
                [-42.55006652, - 43.92111448, -45.44998553, - 47.10515852, - 48.86583903, - 50.71736489])

    v = 40.258321495537544
    index_v = find_value(v, sqha_volume)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v]), lw=3, label="V2")

    plt.scatter(discrete_temperatures,
                [-41.89413855, - 43.17445305, - 44.61424974, - 46.1817799, - 47.85587506, - 49.62144974])

    v = 36.7689539353574
    index_v = find_value(v, sqha_volume)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v]), lw=3, label="V3")

    plt.scatter(discrete_temperatures,
                [-40.58847835, - 41.79457502, - 43.15998955, - 44.65348588, - 46.25422376, - 47.94737818])

    v = 34.34308402343736
    index_v = find_value(v, sqha_volume)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v]), lw=3, label="V4")

    plt.scatter(discrete_temperatures,
                [-39.05674738, - 40.20836091, - 41.51877576, - 42.9571361, - 44.5028067, - 46.14109688])

    v = 32.487552716802675
    index_v = find_value(v, sqha_volume)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V5")

    plt.scatter(discrete_temperatures,
                [-37.42369011, - 38.533426, - 39.802252, - 41.19922512, - 42.70347289, - 44.30001018])

    plt.xlabel("$T$ (K)")
    plt.ylabel("$F$ (eV)")
    plt.title("Helmholtz free energy of CaSiO$_3$\nby entropy integration (lines) and Zhen's (dots)")

    plt.legend()
    plt.savefig("casio3.png", dpi=300)
