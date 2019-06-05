import matplotlib.pyplot as plt
from qha.unit_conversion import *
from qha.tools import find_nearest, find_value
from pgm.sqha import sqha, spline_interpolation, calculator
from pgm.thermo import ThermodynamicProperties
import numpy as np
import pandas as pd
from qha.thermodynamics import calculate_derivatives
from pgm.data import save_line
import matplotlib

if __name__ == "__main__":
    # following are all the input parameters
    NTV = 450
    NT = 801
    discrete_temperatures = [0, 300, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    temperature = np.linspace(0, 8000, NT)
    qha_temp_list = [300, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    qha_temperature = np.linspace(300, 8000, 771)
    temp_list = list(temperature)
    
    desired_pressure = np.linspace(30, 400, NTV)
    folder = 'data/epaw0/upto_400GPa/%sK/input.txt'
    ratio = 1.2
    vib_energies, vib_entropies = sqha(len(desired_pressure), ratio, discrete_temperatures, temperature, folder)
    volumes, energies, static_energies = calculator(len(desired_pressure), ratio, discrete_temperatures, folder)

    energies[0] = np.zeros(len(energies[0]))

    tqha_energies, tqha_volumes = spline_interpolation(volumes, energies, discrete_temperatures, temperature)
    static_free_energies, interpolated_volumes = spline_interpolation(volumes, static_energies, discrete_temperatures, temperature)

    total_free_energies = vib_energies + static_free_energies
    tqha_total_free_energies = tqha_energies + static_free_energies
    sqha_volume = interpolated_volumes[0]

    # the following three instances are tqha, sqha, and static results.
    # thermodynamics can be computed by using the apis in pgm.thermo
    tqha = ThermodynamicProperties(tqha_volumes[0], temperature, gpa_to_ry_b3(desired_pressure), tqha_total_free_energies)
    interpolation = ThermodynamicProperties(sqha_volume, temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)
    static = ThermodynamicProperties(sqha_volume, temperature, gpa_to_ry_b3(desired_pressure), static_free_energies)

    ptv = ry_b3_to_gpa(interpolation.p_tv)
    # this gives the pressure in unit of T and V
    # other example can be
    # g_tp, gibbs free energy as T and P
    # bt_tp bulk modulus as T and P

    plt.plot(ptv[31], ry_to_kb(vib_entropies[31])/2-0.30, label = 'TPGM 300K', color = '#FF0066',lw = 5)
    plt.legend()
    plt.xlabel('Pressure(GPa)', labelpad=20)
    plt.ylabel(r'S$_{vib}$(k$_B$)', labelpad=20)
    plt.savefig('svib2_b.png', dpi = 300, bbox_inches='tight')
    plt.close('all')