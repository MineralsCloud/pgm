"""
Core module for energy calculation in pgm
"""

from pgm.reader.read_input import Input
from pgm.util.fitting import polynomial_least_square_fitting
from pgm.util.grid_interpolation import calculate_eulerian_strain, from_eulerian_strain
import numpy as np
from scipy.constants import physical_constants as pc
from typing import Callable, Optional
from scipy.interpolate import UnivariateSpline, InterpolatedUnivariateSpline
from scipy.integrate import cumtrapz

HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]
K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]


class FreeEnergyCalculation:
    """
    Calculate free energy using pgm
    """

    def __init__(self, NV, NT, initP, finalP, ratio, discrete_temperatures, folder):
        self.NV = NV
        self.NT = NT
        self.ratio = ratio
        self.folder = folder
        self.discrete_temperatures = discrete_temperatures
        self.continuous_temperature = np.linspace(discrete_temperatures[0], discrete_temperatures[-1], NT)
        self.pressures = np.linspace(initP, finalP, NV)

    def calculate(self):
        calc_input = Input(self.folder, self.discrete_temperatures)

        vib_energies, vib_entropies = pgm(self.NV, self.ratio, self.continuous_temperature, calc_input)

        volumes, energies, static_energies = qha(self.NV, self.ratio, calc_input)

        energies[0] = np.zeros(len(energies[0]))

        static_free_energies, interpolated_volumes = spline_interpolation(volumes, static_energies,
                                                                          self.discrete_temperatures,
                                                                          self.continuous_temperature)
        total_free_energies = vib_energies + static_free_energies

        volumes = interpolated_volumes[0]

        return total_free_energies, vib_entropies, volumes, self.pressures, self.continuous_temperature


def pgm(NTV, ratio, continuous_temperatures, input: Input = None):
    """
    phonon gas model
    compute free energies by intergrating entropies
    return:
    vib_free_energies: a continous grid of vibrational free energies
    interpolated_entropies: a continous grid of entropies
    """
    all_volumes = []
    all_entropies = []
    input_dict = input.get_input()
    discrete_temperatures = input.get_temperature()

    for temp in input_dict.keys():
        inter = Interpolation(input_dict[temp][1], NTV, ratio)
        if temp == 0:
            new_s = np.zeros(NTV)
        else:
            s = entropy(temp, input_dict[temp][3], input_dict[temp][4])
            new_s = inter.fitting(s)

        # s = entropy(temp, rs[3], rs[4])
        # new_s = inter.fitting(s)

        all_volumes.append(inter.out_volumes)
        all_entropies.append(new_s)
    all_volumes = np.array(all_volumes)
    all_entropies = np.array(all_entropies)
    interpolated_entropies, interpolated_volumes = spline_interpolation(all_volumes, all_entropies,
                                                                        discrete_temperatures, continuous_temperatures,
                                                                        # calibrate_option=calibrate_option
                                                                        )
    vib_free_energies = intergrate(continuous_temperatures, interpolated_entropies)
    return vib_free_energies, interpolated_entropies


def qha(NTV, ratio, input: Input):
    """
    A similar function as pgm
    Computes qha energy
    return:
    all_volumes: interpolated volumes at different discreate temperatures
    all_energies: interpolated qha energies at different discreate temperatures
    all_static_energies: interpolated static energies at different discreate temperatures
    """

    def qha_energy(temperature, frequency, weights):
        """
        Compute vibrational free energies using qha formula
        """

        def vib_energy(temperature, frequency):
            kt = K * temperature
            mat = np.zeros(frequency.shape)
            for i in range(frequency.shape[0]):
                for j in range(frequency.shape[1]):
                    for k in range(frequency.shape[2]):
                        if frequency[i][j][k] <= 0:
                            mat[i][j][k] = 0
                        else:
                            freq = frequency[i][j][k]
                            hw = HBAR * freq
                            mat[i][j][k] = 1 / 2 * hw + kt * np.log(1 - np.exp(-hw / kt))
            return mat

        scaled_q_weights = weights / np.sum(weights)
        vibrational_energies = np.dot(vib_energy(temperature, frequency).sum(axis=2), scaled_q_weights)

        return vibrational_energies

    all_volumes = []
    all_energies = []
    all_static_energies = []
    input_dict = input.get_input()

    for temp in input_dict.keys():
        vib_f = qha_energy(temp, input_dict[temp][3], input_dict[temp][
            4])  # compute vibrational free energies using qha formula, only vibrational!
        inter = Interpolation(input_dict[temp][1], NTV, ratio)
        static_f = inter.fitting(input_dict[temp][2])
        new_vib_f = inter.fitting(vib_f)

        all_volumes.append(inter.out_volumes)
        all_energies.append(new_vib_f)
        all_static_energies.append(static_f)

    all_volumes = np.array(all_volumes)
    all_energies = np.array(all_energies)
    all_static_energies = np.array(all_static_energies)
    return all_volumes, all_energies, all_static_energies


def entropy_fit(raw_volumes, raw_energies, discrete_temperatures, continuous_temperatures
                ):
    configurations_amount, volume_number = raw_volumes.shape
    index = 0
    interpolated_volumes = np.tile(
        raw_volumes[index], (len(continuous_temperatures), 1))
    calibrated_energy = calibrate_energy_on_reference(
        raw_volumes, raw_energies, order=4, calibrate_index=index).T
    interpolated_free_energies = []

    def fit_it(x, y, vi, xnew):
        def ffunc(x, a, b, c, d, e):
            if x[0] == 0:
                x[0] = 1
            x = np.array(x, dtype=np.float64)
            h = HBAR * 2 * np.pi

            kx = K * x
            w = a + b * np.exp(x / 6000)
            # w = a
            hw = HBAR * w
            hw_2kt = hw / (2 * kx)
            # n = 1/(np.exp(hw / kx)-1)

            return K * (hw_2kt / np.tanh(hw_2kt) - np.log(2 * np.sinh(hw_2kt))) * e
            # return K * ((n+1)*np.log(n+1) - (n)*np.log(n))
            # return np.log(x**1.5 - a) * b + c

        popt, _ = curve_fit(ffunc, x, y)
        return ffunc(xnew, *popt)

    for i in range(volume_number):
        # print(i, b3_to_a3( raw_volumes[0][i])/2)
        x = continuous_temperatures

        f1 = InterpolatedUnivariateSpline(
            discrete_temperatures, calibrated_energy[i])

        # f1.set_smoothing_factor()

        y1 = f1(x)
        # if i == 333:
        #     print(y1, raw_volumes[0][i])

        y = fit_it(discrete_temperatures, calibrated_energy[i], raw_volumes[0][i], x)

        # y = fit_it(x, y1, raw_volumes[0][i], x)

        interpolated_free_energies.append(
            y
        )
    # InterpolatedUnivariateSpline < > UnivariateSpline

    interpolated_free_energies = np.array(interpolated_free_energies)

    return interpolated_free_energies.T, interpolated_volumes


def spline_interpolation(raw_volumes, raw_energies, discrete_temperatures, continuous_temperatures
                         ):
    configurations_amount, volume_number = raw_volumes.shape
    index = 0
    interpolated_volumes = np.tile(raw_volumes[index], (len(continuous_temperatures), 1))
    calibrated_energy = calibrate_energy_on_reference(raw_volumes, raw_energies, order=4, calibrate_index=index).T
    interpolated_free_energies = []
    for i in range(volume_number):
        interpolated_free_energies.append(

            InterpolatedUnivariateSpline(
                discrete_temperatures, calibrated_energy[i])(continuous_temperatures)
        )
    # InterpolatedUnivariateSpline < > UnivariateSpline

    interpolated_free_energies = np.array(interpolated_free_energies)

    return interpolated_free_energies.T, interpolated_volumes


def calibrate_energy_on_reference(volumes_before_calibration, energies_before_calibration,
                                  order: Optional[int] = 3, calibrate_index=0):
    """
    In multi-configuration system calculation, volume set of each calculation may varies a little,
    This function would make the volume set  of configuration 1 (normally, the most populated configuration)
    as a reference volume set, then calibrate the energies of all configurations to this reference volume set.

    :param volumes_before_calibration: Original volume sets of all configurations
    :param energies_before_calibration: Free energies of all configurations on the corresponding volume sets.
    :param order: The order of Birch--Murnaghan EOS fitting.
    :param calibrate_option: The option to control the calibrate reference
    :return: Free energies of each configuration on referenced volumes (usually the volumes of the first configuration).
    """
    configurations_amount, _ = volumes_before_calibration.shape
    volumes_for_reference = volumes_before_calibration[calibrate_index]
    energies_after_calibration = np.empty(volumes_before_calibration.shape)
    for i in range(configurations_amount):
        strains_before_calibration = calculate_eulerian_strain(volumes_before_calibration[i, calibrate_index],
                                                               volumes_before_calibration[i])
        strains_after_calibration = calculate_eulerian_strain(volumes_before_calibration[i, calibrate_index],
                                                              volumes_for_reference)
        _, energies_after_calibration[i, :] = polynomial_least_square_fitting(strains_before_calibration,
                                                                              energies_before_calibration[i],
                                                                              strains_after_calibration,
                                                                              order=order)
    return energies_after_calibration


def entropy(temperature, frequency, weights):
    def vib_entropy(temperature, frequency):
        kt = K * temperature
        mat = np.zeros(frequency.shape)
        for i in range(frequency.shape[0]):
            for j in range(frequency.shape[1]):
                for k in range(frequency.shape[2]):
                    if frequency[i][j][k] <= 0:
                        mat[i][j][k] = 0
                    else:
                        freq = frequency[i][j][k]
                        hw = HBAR * freq
                        hw_2kt = hw / (2 * kt)
                        mat[i][j][k] = K * (hw_2kt / np.tanh(hw_2kt) - np.log(2 * np.sinh(hw_2kt)))
        return mat

    scaled_q_weights = weights / np.sum(weights)
    vibrational_entropies = np.dot(vib_entropy(temperature, frequency).sum(axis=2), scaled_q_weights)

    return vibrational_entropies


def zero_point_motion(temperature, frequency, weights):
    def vib_entropy(temperature, frequency):
        kt = K * temperature
        mat = np.zeros(frequency.shape)
        for i in range(frequency.shape[0]):
            for j in range(frequency.shape[1]):
                for k in range(frequency.shape[2]):
                    if frequency[i][j][k] <= 0:
                        mat[i][j][k] = 0
                    else:
                        freq = frequency[i][j][k]
                        hw_2 = HBAR * freq / 2
                        mat[i][j][k] = hw_2
        return mat

    scaled_q_weights = weights / np.sum(weights)
    zero_free_energies = np.dot(vib_entropy(temperature, frequency).sum(axis=2), scaled_q_weights)
    return zero_free_energies


def intergrate(temperatures, entropies):
    all_energies = []
    for i, entropy in enumerate(entropies.T):  # for same temperature
        energy = cumtrapz(entropy, temperatures, initial=entropy[0])
        all_energies.append(energy)

    return - np.array(all_energies).T


class Interpolation:
    """
    Interpolating a quantity based on the volume grid
    """

    def __init__(self, in_volumes, num, ratio):
        """
        in_volumes: the volume list
        """
        self.in_volumes = np.array(in_volumes)
        self.num = num
        self.ratio = ratio
        self.out_volumes, self.out_strains, self.in_strains = self.interpolate_volumes

    @property
    def interpolate_volumes(self):
        """
        for a vector of volumes, interpolate num, expand the volume by ratio
        """
        in_strains = calculate_eulerian_strain(self.in_volumes[0], self.in_volumes)
        v_min, v_max = np.min(self.in_volumes), np.max(self.in_volumes)
        # r = v_upper / v_max = v_min / v_lower
        v_lower, v_upper = v_min / self.ratio, v_max * self.ratio
        # The *v_max* is a reference value here.
        s_upper, s_lower = calculate_eulerian_strain(v_max, v_lower), calculate_eulerian_strain(v_max, v_upper)
        out_strains = np.linspace(s_lower, s_upper, self.num)
        out_volumes = from_eulerian_strain(v_max, out_strains)
        return out_volumes, out_strains, in_strains

    def fitting(self, quantity, order=3):
        _, fitted_quantity = polynomial_least_square_fitting(self.in_strains, quantity, self.out_strains, order)
        return fitted_quantity


if __name__ == '__main__':
    pass
