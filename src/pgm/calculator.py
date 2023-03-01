"""
Core module for energy calculation in pgm
   :platform: Unix, Windows, Mac, Linux
   :synopsis:
.. moduleauthor:: Hongjin Wang <hw2626@columbia.edu>
.. moduleauthor:: Jingyi Zhuang <jz2907@columbia.edu>
"""

from pgm.reader.read_input import Input
import numpy as np
from scipy.constants import physical_constants as pc
from scipy.integrate import cumtrapz
from .settings import Settings
from .interpolate import Interpolation, FrequencyInterpolation, ElectronicEntropyInterpolation
from numba import jit

HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]
K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]


class FreeEnergyCalculation:
    """
    Calculate free energy using pgm
    """

    def __init__(self, setting: Settings):
        self.NV = setting.NV
        self.NT = setting.NT
        self.ratio = setting.ratio
        self.folder = setting.folder
        self.discrete_temperatures = setting.temperature
        self.continuous_temperature = setting.continuous_temperature
        self.pressures = setting.desired_pressure
        self.input = Input(self.folder, self.discrete_temperatures)

    def interpolate_frequencies(self):
        """
        interpolate the frequencies
        """
        freq = FrequencyInterpolation(self.input).numba_polyfit(self.continuous_temperature)
        return freq

    def calculate_electronic_entropy(self):
        """
        interpolate the electronic_entropy
        """
        s_el = ElectronicEntropyInterpolation(self.input).numba_polyfit(self.continuous_temperature)
        return s_el

    def calculate_vibrational_entropy(self):
        """
        calculate vibrational properties, i.e. vibrational entropy and free energy
        depends on "interpolate_frequencies"
        """
        number_of_raw_volume = len(self.input.volumes)
        s_vib = np.empty((self.NT, number_of_raw_volume))
        freq = self.interpolate_frequencies()
        weight = self.input.weights[0]  # here of course ensure that all weights are the same
        for i in range(len(self.continuous_temperature)):
            s_vib[i] = entropy(self.continuous_temperature[i], freq[i], weight)
        return s_vib

    def calculate_zero_point_energy(self):
        """
        Calculate zero point energy
        depends on "interpolate_frequencies"
        """
        number_of_raw_volume = len(self.input.volumes)
        f_zp = np.empty((self.NT, number_of_raw_volume))
        freq = self.interpolate_frequencies()
        weight = self.input.weights[0]  # here of course ensure that all weights are the same
        fzp0 = zero_point_energy(freq[0], weight)
        for i in range(len(self.continuous_temperature)):
            f_zp[i] = fzp0
        return f_zp

    def integrate_entropy(self):
        """
        Calculate the free energy on a finer temperature grid by integrating entropy
        The entropy here is the summation of electronic entropy and vibrational entropy
        depends on "calculate_vibrational_entropy" and "calculate_electronic_entropy"
        """
        s_vib = self.calculate_vibrational_entropy()
        s_el = self.calculate_electronic_entropy()
        assert (s_el.shape == s_vib.shape)
        s_total = s_vib + s_el
        f_total = integrate(self.continuous_temperature, s_total)
        return f_total, s_total

    def interpolate_F_total(self):
        """
        interpolate the F_total on a finer volume grid
        depends on "integrate_entropy"
        """
        f_total_raw, s_total_raw = self.integrate_entropy()
        raw_E = self.input.static_energy  # E(V) from input
        raw_V = self.input.volumes  # V
        inter = Interpolation(raw_V, num=self.NV, ratio=self.ratio)
        F_total_fitted = np.empty((self.NT, self.NV))
        # if the first temperature isn't 0, the free energy needs to minus a base energy S_0T
        if 0 not in self.discrete_temperatures:
            T_0 = self.discrete_temperatures[0]
            F_total = f_total_raw + raw_E - T_0 * s_total_raw[0]
        else:
            f_zp = self.calculate_zero_point_energy()
            F_total = f_total_raw + f_zp + raw_E
        for i in range(len(self.continuous_temperature)):
            F_total_fitted[i] = inter.fitting(F_total[i])
        return F_total_fitted

    def calculate_volumes(self):
        """
        Interpolate volumes on a finer volume grid
        """
        raw_V = self.input.volumes  # V
        inter = Interpolation(raw_V, num=self.NV, ratio=self.ratio)
        return inter.out_volumes


def zero_point_energy(frequency, weights):
    """
    Equation for calculate entropy from frequencies
    """

    @jit(nopython=True, parallel=True)
    def zp_formula(frequency):
        shape = frequency.shape
        frequency = frequency.reshape(-1)
        # if frequency is negative, they are treated as 0
        frequency[frequency < 0] = 0.0
        hw = HBAR * frequency
        result = 1 / 2 * hw
        return result.reshape(shape)

    scaled_q_weights = weights / np.sum(weights)
    zp_energies = np.dot(np.nan_to_num(zp_formula(
        frequency)).sum(axis=2), scaled_q_weights)

    return zp_energies


def entropy(temperature, frequency, weights):
    """
    Equation for calculate entropy from frequencies
    """

    @jit(nopython=True, parallel=True)
    def vib_entropy(temperature, frequency):
        kt = K * temperature
        shape = frequency.shape
        frequency = frequency.reshape(-1)
        # if frequency is negative, they are treated as 0
        frequency[frequency < 0] = 0.0

        # result = np.zeros(len(frequency))
        hw = HBAR * frequency
        hw_2kt = hw / (2 * kt)
        result = K * (hw_2kt / np.tanh(hw_2kt) - np.log(2 * np.sinh(hw_2kt)))

        return result.reshape(shape)

    scaled_q_weights = weights / np.sum(weights)
    vibrational_entropies = np.dot(np.nan_to_num(vib_entropy(temperature, frequency)).sum(axis=2), scaled_q_weights)

    return vibrational_entropies


def integrate(temperatures, entropies):
    all_energies = []
    for i, entropy in enumerate(entropies.T):  # for same temperature
        energy = cumtrapz(entropy, temperatures, initial=entropy[0])
        all_energies.append(energy)

    return - np.array(all_energies).T


if __name__ == '__main__':
    pass
