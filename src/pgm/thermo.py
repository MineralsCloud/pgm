from lazy_property import LazyProperty
from qha.thermodynamics import *
from qha.thermodynamics import calculate_derivatives
from qha.v2p import v2p
from qha.unit_conversion import *
from qha.tools import find_nearest, is_monotonic_increasing
import numpy as np
from pgm.geotherm import geotherm

class ThermodynamicProperties:
    # all units are ry, bohr^3
    # all 2-d matrix are t,v(p)
    # energy matrix should has the same size as volume or temperature
    def __init__(self, volume, temperature, pressure, energy):
        self.__volume = volume
        self.__temperature = temperature
        self.__pressure = pressure
        self.__energy = energy
    
    @LazyProperty
    def energy(self):
        return self.__energy

    @LazyProperty
    def p_tv(self):
        return pressure(self.__volume, self.__energy)
    
    @LazyProperty
    def thermal_potential(self):
        return thermodynamic_potentials(self.__temperature, self.__volume, self.__energy, self.p_tv)

    @LazyProperty
    def v_tp(self):
        return volume(self.__volume, self.__pressure, self.p_tv)

    @LazyProperty
    def s_tv(self):
        return entropy(self.__temperature, self.energy)

    @LazyProperty
    def cv_tp(self):
        return v2p(self.cv_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def bt_tv(self):
        return isothermal_bulk_modulus(self.__volume, self.p_tv)

    @LazyProperty
    def bt_tp(self):
        return v2p(self.bt_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def cv_tv(self):
        return volumetric_heat_capacity(self.__temperature, self.thermal_potential["U"])

    @LazyProperty
    def cp_tp(self):
        return isobaric_heat_capacity(self.cv_tp, self.alpha_tp, self.gamma_tp, self.__temperature)

    @LazyProperty
    def gamma_tp(self):
        return gruneisen_parameter(self.v_tp, self.bt_tp, self.alpha_tp, self.cv_tp)

    @LazyProperty
    def bt_tp(self):
        return v2p(self.bt_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def alpha_tp(self):
        return thermal_expansion_coefficient(self.__temperature, self.v_tp)

    @LazyProperty
    def h_tp(self):
        return v2p(self.h_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def bs_tp(self):
        return adiabatic_bulk_modulus(self.bt_tp, self.alpha_tp, self.gamma_tp, self.__temperature)

    @LazyProperty
    def g_tv(self):
        return self.thermal_potential['G']

    @LazyProperty
    def g_tp(self):
        return v2p(self.g_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def cv_tp(self):
        return v2p(self.cv_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def btp_tp(self):
        return calculate_derivatives(self.__temperature, self.bt_tp)

    @LazyProperty
    def u_tv(self):
        return self.thermal_potential['U']
    
    @LazyProperty
    def u_tp(self):
        return v2p(self.u_tv, self.p_tv, self.__pressure)

    @LazyProperty
    def cp_tv(self):
        return pressure_specific_heat_capacity_tv(self.cv_tv, self.alpha_tv, self.gamma_tv, self.__temperature)

    @LazyProperty
    def geotherm(self):
        return geotherm(self.alpha_tp, self.cp_tp, self.v_tp, self.__temperature)

    def get_adiabatic_t_p(self, target_temperature, target_pressure):
        if is_monotonic_increasing(target_temperature) is False or is_monotonic_increasing(target_pressure) is False:
            raise ValueError('temperature and pressure must be monotonic increasing')
        t0 = target_temperature[0]
        p0 = target_pressure[0]
        t_max = target_temperature[-1]
        pressure_gpa = ry_b3_to_gpa(self.__pressure)
        all_t = []
        all_p = []
        geotherm_matrix = self.get_geotherm # which is actually on tp grid
        for i, pressure in enumerate(target_pressure):
            geotherm_row_index = find_nearest(self.__temperature, t0)
            geotherm_column_index = find_nearest(pressure_gpa, p0)
            dp = target_pressure[1] - target_pressure[0]
            ti = t0 + dp * geotherm_matrix[geotherm_row_index][geotherm_column_index]
            if ti >= t_max:
                print('%s times of iteration, break' % i)
                break
            else:
                all_t.append(ti)
                all_p.append(pressure)
                t0 = ti
                p0 += dp

        return all_t, all_p

    def get_adiabatic_eos(self, temperature, pressure):
        ptv = ry_b3_to_gpa(self.p_tv)
        all_volume = []
        for i, temp in enumerate(temperature):
            row_index = find_nearest(self.__temperature, temperature[i])
            column_index =find_nearest(ptv[row_index], pressure[i])
            all_volume.append(self.__volume[column_index])
        return np.array(all_volume)

