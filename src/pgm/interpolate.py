"""
All interpolation related module in pgm
   :platform: Unix, Windows, Mac, Linux
   :synopsis:
.. moduleauthor:: Hongjin Wang <hw2626@columbia.edu>
"""

from typing import Callable, Optional
from scipy.interpolate import UnivariateSpline, InterpolatedUnivariateSpline
from pgm.util.fitting import polynomial_least_square_fitting
from pgm.util.grid_interpolation import calculate_eulerian_strain, from_eulerian_strain

import numpy as np


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
        e = UnivariateSpline(discrete_temperatures, calibrated_quantities[i])(continuous_temperatures)
        interpolated_quantities.append(e)
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
