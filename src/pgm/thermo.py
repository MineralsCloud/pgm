from lazy_property import LazyProperty
# from qha.thermodynamics import *
# from qha.thermodynamics import calculate_derivatives
from .v2p import v2p
from .util.unit_conversion import *
from .util.tools import find_value\
    # , is_monotonic_increasing
import numpy as np
# from pgm.geotherm import geotherm


def calculate_derivatives(xs, fs):
    """
    Calculate the derivative of :math:`f(x)`, i.e., :math:`\\frac{ df(x) }{ dx }`.

    :param xs: A 1D vector, with length :math:`N_x`.
    :param fs: A matrix, with shape :math:`(N_x, _)`.
    :return: A matrix, with shape :math:`(N_x, _)`.
    """
    if xs.ndim > 1 or fs.ndim < 2:
        raise ValueError('The argument *xs* should be a 1D array and *ys* should be a 2D array!')

    return np.gradient(fs, axis=0) / np.gradient(xs)[:, None]  # df(x)/dx.


def pressure(vs, free_energies):
    """
    Calculate the pressure as a function of temperature and volume, i.e.,

    .. math::

       P = - \\bigg( \\frac{ \\partial F(T, V) }{ \\partial V } \\bigg)_T.

    :param vs: A vector of volumes.
    :param free_energies: A matrix, the free energy as a function of temperature and volume, i.e., :math:`F(T, V)`.
    :return: A matrix, the pressure as a function of temperature and volume, i.e., :math:`P(T,V)`.
    """
    return -np.gradient(free_energies, axis=1) / np.gradient(vs)


def entropy(temperature, free_energies):
    """
    Calculate the entropy as a function of temperature and volume, i.e.,

    .. math::

       S = - \\bigg( \\frac{ \\partial F(T, V) }{ \\partial T } \\bigg)_V.

    :param temperature: A vector of temperature.
    :param free_energies: A matrix, the free energy as a function of temperature and volume, i.e., :math:`F(T, V)`.
    :return: A matrix, the entropy as a function of temperature and volume, i.e., :math:`S(T,V)`.
    """
    return -calculate_derivatives(temperature, free_energies)


def thermodynamic_potentials(temperature, vs, free_energies, ps):
    """
    Calculate the enthalpy :math:`H(T, V)`, the internal energy :math:`U(T, V)`,
    and the Gibbs free energy :math:`G` on a :math:`(T, V)` grid from Helmholtz free energy :math:`F(T, V)` by

    .. math::

       U(T, V) &= F(T, V) + T S(T, V), \\\\
       H(T, V) &= U(T, V) + P(T, V) V, \\\\
       G(T, V) &= F(T, V) + P(T, V) V.

    :param temperature: A vector of temperature.
    :param vs: A vector of volumes.
    :param free_energies: A matrix, the free energy as a function of temperature and volume, i.e., :math:`F(T, V)`.
    :param ps: A matrix, the pressure as a function of temperature and volume, i.e., :math:`P(T, V)`.
    :return: A dictionary that contains the enthalpy :math:`H(T, V)`, the internal energy :math:`U(T, V)`,
        and the Gibbs free energy :math:`G` on a :math:`(T, V)` grid. They can be retrieved by ``'U'``, ``'H'``, or
        ``'G'`` keys, respectively.
    """
    g = free_energies + ps * vs  # G(T,V) = F(T,V) + V * P(T,V)

    u = free_energies + entropy(temperature, free_energies) * temperature.reshape(-1, 1)  # U(T,V) = F(T,V) + T * S(T,V)

    h = u + ps * vs  # H(T,V) = U(T,V) + V * P(T,V)

    return {'U': u, 'H': h, 'G': g}


def volume(vs, desired_ps, ps):
    """
    Convert the volumes as a function of temperature and pressure, i.e., on a :math:`(T, P)` grid.

    :param vs: A vector of volumes.
    :param desired_ps: A vector of desired pressures.
    :param ps: A matrix, the pressure as a function of temperature and volume, i.e., :math:`P(T,V)`, in atomic unit.
    :return: A matrix, the volume as a function of temperature and pressure, i.e., :math:`V(T, P)`.
    """
    nt, ntv = ps.shape
    vs = vs.reshape(1, -1).repeat(nt, axis=0)
    return v2p(vs, ps, desired_ps)


def thermal_expansion_coefficient(temperature, vs):
    """
    Calculate the thermal expansion coefficient by

    .. math::

       \\alpha = \\frac{ 1 }{ V }  \\bigg( \\frac{ \\partial V }{ \\partial T } \\bigg)_P.

    :param temperature: A vector of temperature.
    :param vs: A matrix, the volume as a function of temperature and pressure, i.e., :math:`V(T, P)`.
    :return: A matrix, the thermal expansion coefficient as a function of temperature and pressure,
        i.e., :math:`\\alpha(T, P)`.
    """
    # Division is done by element-wise.
    return calculate_derivatives(temperature, vs) / vs


def gruneisen_parameter(vs, bt, alpha, cv):
    """
    Calculate the Grüneisen parameter by

    .. math::

       \\gamma = \\frac{ \\alpha B_T V }{ C_V }.

    :param vs: A matrix, the volume as a function of temperature and pressure, i.e., :math:`V(T, P)`.
    :param bt: A matrix, the isothermal bulk modulus as a function of temperature and pressure,
        i.e., :math:`B_T(T, P)`.
    :param alpha: A matrix, the thermal expansion coefficient as a function of temperature and pressure,
        i.e., :math:`\\alpha(T, P)`.
    :param cv: A matrix, the volumetric heat capacity as a function of temperature and pressure,
        i.e., :math:`C_V(T, P)`.
    :return: A matrix, the thermodynamic Grüneisen parameter as a function of temperature and pressure,
        i.e., :math:`\\gamma(T, P)`.
    """
    gamma = np.empty([vs.shape[0], vs.shape[1]])
    gamma[0] = 0.0
    gamma[1:, :] = vs[1:] * bt[1:] * alpha[1:] / cv[1:]
    # return vs * bt * alpha / cv
    return gamma


def isothermal_bulk_modulus(vs, ps):
    """
    Calculate the isothermal bulk modulus by

    .. math::

       B_T = - V \\bigg( \\frac{ \\partial P }{ \\partial V } \\bigg)_T.

    :param vs: A vector of volumes.
    :param ps: A matrix, the pressure as a function of temperature and volume, i.e., :math:`P(T, V)`.
    :return: A matrix, the isothermal bulk modulus, as a function of temperature and volume, i.e., :math:`B_T(T, V)`.
    """
    return -np.gradient(ps, axis=1) / np.gradient(vs) * vs


def adiabatic_bulk_modulus(bt, alpha, gamma, temperature):
    """
    Calculate the adiabatic bulk modulus by

    .. math::

       B_S = B_T \\big( 1 + \\alpha \\gamma T \\big).

    :param bt: A matrix, the isothermal bulk modulus, as a function of temperature and pressure,
        i.e., :math:`B_T(T, P)`.
    :param alpha: A matrix, the thermal expansion coefficient as a function of temperature and pressure,
        i.e., :math:`\\alpha(T, P)`.
    :param gamma: A matrix, the thermodynamic Grüneisen parameter as a function of temperature and pressure,
        i.e., :math:`\\gamma(T, P)`.
    :param temperature: A vector of temperature.
    :return: A matrix, the adiabatic bulk modulus, as a function of temperature and pressure,
        i.e., :math:`B_S(T,P)`.
    """
    return bt * (1.0 + alpha * gamma * temperature[:, None])


def bulk_modulus_derivative(ps, bt):
    """
    Calculate the first-order derivative of bulk modulus with respect to pressure by

    .. math::

       B_T' = \\bigg( \\frac{ \\partial B_T }{ \\partial P } \\bigg).

    :param ps: A vector of pressures.
    :param bt: A matrix, the isothermal bulk modulus, as a function of temperature and pressure,
        i.e., :math:`B_T(T, P)`.
    :return: A matrix, the isothermal bulk modulus, as a function of temperature and pressure, i.e.,
        :math:`B_T'(T, P)`.
    """
    return calculate_derivatives(ps, bt.T).T


def isobaric_heat_capacity(cv, alpha, gamma, temperature):
    """
    Calculate the isobaric heat capacity by

    .. math::

       C_P = C_V \\big( 1 + \\alpha \\gamma T \\big).

    :param cv: A matrix, the volumetric heat capacity, :math:`C_V(T, P)`.
    :param alpha: A matrix, the thermal expansion coefficient as a function of temperature and pressure,
        i.e., :math:`\\alpha(T, P)`.
    :param gamma: A matrix, the thermodynamic Grüneisen parameter as a function of temperature and pressure,
        i.e., :math:`\\gamma(T, P)`.
    :param temperature: A vector of temperature.
    :return: A matrix, the isobaric specific heat capacity as a function of temperature and pressure,
        i.e., :math:`C_P(T,P)`.
    """
    return cv * (1.0 + alpha * gamma * temperature[:, None])


def volumetric_heat_capacity(temperature, internal_energies):
    """
    Calculate the volumetric heat capacity by

    .. math::

       C_V = \\bigg( \\frac{ \\partial U }{ \\partial T } \\bigg).

    :param temperature: A vector of temperature.
    :param internal_energies: A matrix, the internal energy as a function of temperature and volume,
        i.e., :math:`U(T, V)`.
    :return: A matrix, the volumetric heat capacity as a function of temperature and volume,
        i.e., :math:`C_V(T, V)`.
    """
    return calculate_derivatives(temperature, internal_energies)


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

    # @LazyProperty
    # def cp_tv(self):
    #     return pressure_specific_heat_capacity_tv(self.cv_tv, self.alpha_tv, self.gamma_tv, self.__temperature)

    # @LazyProperty
    # def geotherm(self):
    #     return geotherm(self.alpha_tp, self.cp_tp, self.v_tp, self.__temperature)

    # def get_adiabatic_t_p(self, target_temperature, target_pressure):
    #     if is_monotonic_increasing(target_temperature) is False or is_monotonic_increasing(target_pressure) is False:
    #         raise ValueError('temperature and pressure must be monotonic increasing')
    #     t0 = target_temperature[0]
    #     p0 = target_pressure[0]
    #     t_max = target_temperature[-1]
    #     pressure_gpa = ry_b3_to_gpa(self.__pressure)
    #     all_t = []
    #     all_p = []
    #     geotherm_matrix = self.get_geotherm  # which is actually on tp grid
    #     for i, pressure in enumerate(target_pressure):
    #         geotherm_row_index = find_value(self.__temperature, t0)
    #         geotherm_column_index = find_value(pressure_gpa, p0)
    #         dp = target_pressure[1] - target_pressure[0]
    #         ti = t0 + dp * geotherm_matrix[geotherm_row_index][geotherm_column_index]
    #         if ti >= t_max:
    #             print('%s times of iteration, break' % i)
    #             break
    #         else:
    #             all_t.append(ti)
    #             all_p.append(pressure)
    #             t0 = ti
    #             p0 += dp
    #
    #     return all_t, all_p

    def get_adiabatic_eos(self, temperature, pressure):
        ptv = ry_b3_to_gpa(self.p_tv)
        all_volume = []
        for i, temp in enumerate(temperature):
            row_index = find_value(self.__temperature, temperature[i])
            column_index = find_value(ptv[row_index], pressure[i])
            all_volume.append(self.__volume[column_index])
        return np.array(all_volume)
