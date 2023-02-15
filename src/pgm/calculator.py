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
from scipy.optimize import curve_fit
from .settings import Settings
from .interpolate import Interpolation, spline_interpolation, calibrate_energy_on_reference, FrequencyInterpolation, \
    ElectronicEntropyInterpolation
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

    def calculate(self):
        calc_input = Input(self.folder, self.discrete_temperatures)

        # calculate vibrational free energies using pgm
        # note here the vibrational energies and entropies are already interpolated between configurations
        vib_energies, vib_entropies = pgm(self.NV, self.ratio, self.continuous_temperature, calc_input)

        volumes, zp_energies, static_energies = zp_and_static(self.NV, self.ratio, calc_input)

        # interpolate static energy between configurations
        static_free_energies, interpolated_volumes = spline_interpolation(volumes, static_energies,
                                                                          self.discrete_temperatures,
                                                                          self.continuous_temperature)

        total_free_energies = vib_energies + static_free_energies

        # if the first temperature isn't 0, the free energy needs to minus a base energy S_0T
        if 0 not in self.discrete_temperatures:
            s0T = np.min(self.discrete_temperatures) * np.array(vib_entropies[0, :])
            total_free_energies -= np.array([list(s0T)] * self.NT)
        else:
            zp_free_energies, _ = spline_interpolation(volumes, zp_energies,
                                                       self.discrete_temperatures,
                                                       self.continuous_temperature)
            total_free_energies += + zp_free_energies

        volumes = interpolated_volumes[0]

        return total_free_energies, vib_entropies, volumes, self.pressures, self.continuous_temperature

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
            raise NotImplementedError
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


def pgm(NTV, ratio, continuous_temperatures, input: Input = None):
    """
    phonon gas model
    compute free energies by integrating entropies
    NTV: number of volumes
    ratio: volume expansion ratio
    continuous_temperatures: a series of continuous temperatures
    input: Input class, i.e. bundle of all input files
    return:
    vib_free_energies: a continuous grid of vibrational free energies
    interpolated_entropies: a continuous grid of entropies
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

        all_volumes.append(inter.out_volumes)
        all_entropies.append(new_s)
    all_volumes = np.array(all_volumes)
    all_entropies = np.array(all_entropies)

    """
    Interpolate entropies between configurations
    """
    interpolated_entropies, interpolated_volumes = fit_entropy(all_volumes, all_entropies,
                                                               discrete_temperatures, continuous_temperatures,
                                                               )

    vib_free_energies = integrate(continuous_temperatures, interpolated_entropies)

    return vib_free_energies, interpolated_entropies


def zp_and_static(NTV, ratio, input: Input):
    """
    Computes zero point energy
    NTV: number of volumes
    ratio: volume expansion ratio
    input: Input class, i.e. bundle of all input files
    return:
    all_volumes: interpolated volumes at different discrete temperatures
    all_zp_energies: interpolated zp energies at different discrete temperatures
    all_static_energies: interpolated static energies at different discrete temperatures
    """

    def zp_energy(temperature, frequency, weights):
        """
        Compute vibrational free energies using qha formula
        """

        @jit(nopython=True, parallel=True)
        def zp_formula(temperature, frequency):
            kt = K * temperature
            shape = frequency.shape
            frequency = frequency.reshape(-1)

            # if frequency is negative, they are treated as 0
            frequency[frequency < 0] = 0.0
            hw = HBAR * frequency
            result = 1 / 2 * hw
            return result.reshape(shape)

        scaled_q_weights = weights / np.sum(weights)
        zp_energies = np.dot(np.nan_to_num(zp_formula(
            temperature, frequency)).sum(axis=2), scaled_q_weights)

        return zp_energies

    all_volumes = []
    all_zp_energies = []
    all_static_energies = []
    input_dict = input.get_input()

    for temp in input_dict.keys():
        vib_f = zp_energy(temp, input_dict[temp][3], input_dict[temp][
            4])  # compute zero point energies

        # input_dict[temp][1] is the volumes from a single qha input file
        # inter is used to calculate the strain based on the volume
        inter = Interpolation(input_dict[temp][1], NTV, ratio)

        # input_dict[temp][2] is the static free energy from a single qha input file
        # Then interpolate between the static free energy using the strain calculated in inter
        static_f = inter.fitting(input_dict[temp][2])

        new_vib_f = inter.fitting(vib_f)

        all_volumes.append(inter.out_volumes)
        all_zp_energies.append(new_vib_f)
        all_static_energies.append(static_f)

    all_volumes = np.array(all_volumes)
    all_zp_energies = np.array(all_zp_energies)
    all_static_energies = np.array(all_static_energies)
    return all_volumes, all_zp_energies, all_static_energies


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
        For fitting function, see https://journals.aps.org/prb/pdf/10.1103/PhysRevB.89.094109
        """

        def func(x, a, b, c, d):
            if x[0] == 0:
                x[0] = 1
            x = np.array(x, dtype=np.float64)
            kx = K * x

            w = a + b * np.exp(x / np.max(x))
            # w = a * np.exp(-x / b) + d
            # w = a * x * x + b * x + d
            hw = HBAR * w
            hw_2kt = hw / (2 * kx)

            return K * (hw_2kt / np.tanh(hw_2kt) - np.log(2 * np.sinh(hw_2kt))) * c

        popt, _ = curve_fit(func, x, y)
        return func(xnew, *popt)

    def fit_freq(t, s, tnew):
        """
        Fitting function for entropy
        return the entropy in a finer T grid by interpolating the 'efficient' frequency
        - important: not working!
        """
        raise NotImplementedError

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
            # rs = InterpolatedUnivariateSpline(discrete_temperatures, calibrated_quantities[i])(continuous_temperatures)
            rs = fit_it(discrete_temperatures, calibrated_quantities[i], continuous_temperatures)
        else:
            rs = fit_it(discrete_temperatures, calibrated_quantities[i], continuous_temperatures)
        interpolated_quantities.append(
            rs
        )
    # InterpolatedUnivariateSpline < > UnivariateSpline

    interpolated_quantities = np.array(interpolated_quantities).T

    return interpolated_quantities, interpolated_volumes


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


def interpolate_frequencies():
    NotImplemented


if __name__ == '__main__':
    pass
