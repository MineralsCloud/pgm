import numpy as np
from scipy.integrate import cumtrapz
from scipy.constants import physical_constants as pc
import pandas as pd
from qha.unit_conversion import ry_to_kb
from qha.readers import read_input
from pgm.sqha import *
import matplotlib.pyplot as plt

HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]
K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]

def heat_capacity(temperature, frequency, weights):
    def vib_heat_capacity(temperature, frequency):
        T = temperature
        kt = K * T
        mat = np.zeros(frequency.shape)
        for i in range(frequency.shape[0]):
            for j in range(frequency.shape[1]):
                for k in range(frequency.shape[2]):
                    if frequency[i][j][k] <= 0:
                        mat[i][j][k] = 0
                    else:
                        freq = frequency[i][j][k]
                        hw = HBAR * freq
                        hw_2kt = hw / (2*kt)
                        mat[i][j][k] = 1/ (4*kt * T) * (hw / np.sinh(hw_2kt))**2
        return mat

    scaled_q_weights: Vector = weights / np.sum(weights)
    vibrational_heat_capacity: Vector = np.dot(vib_heat_capacity(temperature, frequency).sum(axis=2), scaled_q_weights)
    
    return vibrational_heat_capacity

def cvqha(NTV, ratio, discrete_temperatures, continuous_temperatures, path = 'data/vibration/%sK/input.txt'):
    all_volumes = []
    all_cvs = []
    for temp in discrete_temperatures:
        rs = read_input(path % temp)
        cv = heat_capacity(temp, rs[3], rs[4])
        inter = interpolation(rs[1], NTV, ratio)
        new_cv = inter.fitting(cv)
        all_volumes.append(inter.out_volumes)
        all_cvs.append(new_cv)
    all_volumes = np.array(all_volumes)
    all_cvs = np.array(all_cvs)
    interpolated_cvs, interpolated_volumes = spline_interpolation(all_volumes, all_cvs, discrete_temperatures, continuous_temperatures)
    # free_energies = intergrate(continuous_temperatures, interpolated_cvs)
    return interpolated_cvs, all_volumes[0]

def find_value(array, value):
    return np.argmin(np.abs(np.array(array)-value))

if __name__ == "__main__":
    dis_temp = [300, 1000, 2000, 3000,4000, 5000, 6000, 7000, 8000]
    temperature = np.linspace(300, 8000, 771)
    temp_list = list(temperature)
    pressure = np.linspace(51, 449, 450)

    cv, v = cvqha(450, 1.2, dis_temp, temperature, path='data/epaw0/upto_400GPa/%sK/input.txt')
    all_cv = []
    murphy_volumes = np.array([5.92, 5.81, 5.56, 5.36, 5.27, 5.15, 5, 4.89, 4.81, 4.70, 4.58])
    murphy_s = np.array([2.63, 2.57, 2.38, 2.24, 2.20, 2.10, 2.01, 1.92, 1.87, 1.81, 1.70])
    murphy_cv = np.array([2.62, 2.60, 2.54, 2.49, 2.47, 2.44, 2.40, 2.36, 2.33, 2.30, 2.25])
    # for volume in murphy_volumes:
    #     volume = cm3_mol_to_b3(volume)
    #     # print(volume)
    #     index = find_value(v/2, volume)
    #     # print(index)
    #     all_cv.append(ry_to_kb(cv[0, index])/2)
        # print(volume, index, 
        # # interpolation.alpha_tp[1, index]*1e5,
        # # interpolation.gamma_tp[1, index],
        # ry_to_kb(vib_entropies[0, index])/2
        # )

    plt.plot(v/2, ry_to_kb(cv[0])/2, label = 'SQHA')
    plt.scatter(cm3_mol_to_b3(murphy_volumes), murphy_cv, label = 'Murphy')
    plt.xlabel('Volume(cm$^3$/mol)')
    plt.ylabel('C$_V$(K$_B$)')
    plt.legend()
    plt.show()