"""
Core module for energy calculation in pgm
   :platform: Unix, Windows, Mac, Linux
   :synopsis:
.. moduleauthor:: Hongjin Wang <hw2626@columbia.edu>
.. moduleauthor:: Jingyi Zhuang <jz2907@columbia.edu>
"""

from pgm.reader.read_input import Input
from pgm.util.fitting import polynomial_least_square_fitting
from pgm.util.grid_interpolation import calculate_eulerian_strain, from_eulerian_strain
import numpy as np
from scipy.constants import physical_constants as pc
from typing import Callable, Optional
from scipy.interpolate import UnivariateSpline, InterpolatedUnivariateSpline
from scipy.integrate import cumtrapz
from scipy.optimize import curve_fit
from .settings import Settings

# from sympy import symbols,tanh,sinh,log
# from sympy.solvers import solve

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
        self.pressures = setting.continuous_temperature

    # def __init__(self, NV, NT, initP, finalP, ratio, discrete_temperatures, folder):
    #     self.NV = NV
    #     self.NT = NT
    #     self.ratio = ratio
    #     self.folder = folder
    #     self.discrete_temperatures = discrete_temperatures
    #     self.continuous_temperature = np.linspace(discrete_temperatures[0], discrete_temperatures[-1], NT)
    #     self.pressures = np.linspace(initP, finalP, NV)

    def calculate(self):
        calc_input = Input(self.folder, self.discrete_temperatures)

        # calculate vibrational free energies using pgm
        vib_energies, vib_entropies = pgm(self.NV, self.ratio, self.continuous_temperature, calc_input)

        volumes, energies, static_energies = qha(self.NV, self.ratio, calc_input)

        energies[0] = np.zeros(len(energies[0]))

        # interpolation between configurations(temperatures)
        static_free_energies, interpolated_volumes = spline_interpolation(volumes, static_energies,
                                                                          self.discrete_temperatures,
                                                                          self.continuous_temperature)
        total_free_energies = vib_energies + static_free_energies

        # if the first temperature isn't 0, the free energy needs to minus a base energy
        if 0 not in self.discrete_temperatures:
            s0T = np.min(self.discrete_temperatures) * np.array(vib_entropies[0, :])
            total_free_energies -= np.array([list(s0T)] * self.NT)

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
    """
    Start from here there are 2 options:
    If the input comes with configuration starts from 0K, we can use spline interpolation
    Otherwise, if the starting temperature is somewhat higher than 0K, we need to fit the entropy
    """
    interpolated_entropies, interpolated_volumes = fit_entropy(all_volumes, all_entropies,
                                                               discrete_temperatures, continuous_temperatures,
                                                               )

    vib_free_energies = intergrate(continuous_temperatures, interpolated_entropies)

    return vib_free_energies, interpolated_entropies


def qha(NTV, ratio, input: Input):
    """
    Computes qha energy
    return:
    all_volumes: interpolated volumes at different discrete temperatures
    all_energies: interpolated qha energies at different discrete temperatures
    all_static_energies: interpolated static energies at different discrete temperatures
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

        # input_dict[temp][1] is the volumes from a single qha input file
        # inter is used to calculate the strain based on the volume
        inter = Interpolation(input_dict[temp][1], NTV, ratio)

        # input_dict[temp][2] is the static free energy from a single qha input file
        # Then interpolate between the static free energy using the strain calculated in inter
        static_f = inter.fitting(input_dict[temp][2])

        new_vib_f = inter.fitting(vib_f)

        all_volumes.append(inter.out_volumes)
        all_energies.append(new_vib_f)
        all_static_energies.append(static_f)

    all_volumes = np.array(all_volumes)
    all_energies = np.array(all_energies)
    all_static_energies = np.array(all_static_energies)
    return all_volumes, all_energies, all_static_energies


def fit_entropy(raw_volumes, raw_entropy, discrete_temperatures, continuous_temperatures
                ):
    """
    interpolate between configurations
    raw_volumes: a volume dataframe with the size of (# of configurations, # of volumes)
    raw_quantity: a entropy dataframe with the size of (# of configurations, # of entropy)
    discrete_temperatures: a array of the temperatures for all the configurations
    continuous_temperatures: target temperatures array
    """

    def fit_it(x, y, xnew):
        """
        Fitting function for entropy
        """

        def func(x, a, b, c):
            if x[0] == 0:
                x[0] = 1
            x = np.array(x, dtype=np.float64)
            kx = K * x
            w = a + b * np.exp(x / np.max(x))

            hw = HBAR * w
            hw_2kt = hw / (2 * kx)

            return K * (hw_2kt / np.tanh(hw_2kt) - np.log(2 * np.sinh(hw_2kt))) * c

        popt, _ = curve_fit(func, x, y)
        return func(xnew, *popt)

    def fit_freq(t,s,tnew):
        """
        Fitting function for  ...
        return the entropy in a finer T grid by interpolating the 'efficient' frequency
        - important: not working!
        """
        # freq_eff = []
        # print("start")
        # for i in range(len(t)):
        #     si = s[i]
        #     ti = t[i]
        #     a = symbols('a', real=True, positive=True)
        #
        #     # a = symbols('a')
        #     # eq = round(K*10**7, 3) * (a / tanh(a) - log(2 * sinh(a))) - round(si*10**7, 3)
        #     eq = round(K*10**7, 3) * ((1+a)*log(1+a) - a * log(a)) - round(si*10**7, 3)
        #     print(eq)
        #     solutions = solve(eq, quick=True)
        #     print(solutions)
        #     # onlysolution = solutions[0]
        #     # hw_2kt_eff = onlysolution.evalf(subs=onlysolution)
        #     # kt =  K * ti
        #     # hw_eff = hw_2kt_eff * (2*kt)
        #     # w_eff = hw_eff/HBAR
        #     # freq_eff.append(w_eff)
        #
        # print(freq_eff)

        return None

    configurations_amount, volume_number = raw_volumes.shape
    index = 0
    interpolated_volumes = np.tile(raw_volumes[index], (len(continuous_temperatures), 1))
    calibrated_quantities = calibrate_energy_on_reference(raw_volumes, raw_entropy, order=4, calibrate_index=index).T
    interpolated_quantities = []
    for i in range(volume_number):
        """
        Here decide which interpolation method to use
        Case1: if the input comes with phonon calculated at 0K, we can use spline interpolation
        Case2: if the input comes without phonon calculated at 0K, we need to fit the entropy
        """

        if 0 in discrete_temperatures:
            rs = InterpolatedUnivariateSpline(discrete_temperatures, calibrated_quantities[i])(continuous_temperatures)
        else:
            rs = fit_it(discrete_temperatures, calibrated_quantities[i], continuous_temperatures)
        interpolated_quantities.append(
            rs
        )
    # InterpolatedUnivariateSpline < > UnivariateSpline

    interpolated_quantities = np.array(interpolated_quantities).T

    return interpolated_quantities, interpolated_volumes


def spline_interpolation(raw_volumes, raw_quantities, discrete_temperatures, continuous_temperatures
                         ):
    """
    interpolate between configurations
    raw_volumes: a volume dataframe with the size of (# of configurations, # of volumes)
    raw_quantity: a quantity(eg. entropy/energy) dataframe with the size of (# of configurations, # of quantity)
    discrete_temperatures: a array of the temperatures for all the configurations
    continuous_temperatures: target temperatures array
    """
    configurations_amount, volume_number = raw_volumes.shape
    index = 0
    interpolated_volumes = np.tile(raw_volumes[index], (len(continuous_temperatures), 1))
    calibrated_quantities = calibrate_energy_on_reference(raw_volumes, raw_quantities, order=4, calibrate_index=index).T
    interpolated_quantities = []
    for i in range(volume_number):
        interpolated_quantities.append(

            InterpolatedUnivariateSpline(
                discrete_temperatures, calibrated_quantities[i])(continuous_temperatures)
        )
    # InterpolatedUnivariateSpline < > UnivariateSpline

    interpolated_quantities = np.array(interpolated_quantities).T

    return interpolated_quantities, interpolated_volumes


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
    """
    Equation for calculate entropy from frequencies
    """

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
