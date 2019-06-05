"""
Use VDoS to calculate all vibrational thermodynamics properties
Note this is a different method from reading the q point sampling
"""
import numpy as np
from scipy.integrate import cumtrapz
from scipy.constants import physical_constants as pc
import pandas as pd
from qha.unit_conversion import ry_to_kb

HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]
K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]
def normalize(frequency, intensity, N=2):
    """
    normalize the frequency
    """
    intensity = intensity - min(intensity)
    factor = 3 * N / cumtrapz(intensity, frequency)[-1]
    return frequency, intensity*factor

def n(energy, temperature):
    """
    Compute a bose einstein distribution
    """
    beta = 1 / (K * temperature)
    return 1 / np.expm1(beta * energy) 

def vdos_entropy(frequency, intensity, temperature, N=2):
    """
    Compute vibrational entropy using vdos
    Eq: 3KBint_(0)^(infty) g(e) [(n(e)+1)ln(n(e)+1)-n(e)ln(n(e))] de
    """
    energy = HBAR * frequency
    T = temperature
    rhs = np.array([(n(x, T) + 1) * np.log1p(n(x, T)) - n(x, T) * np.log(n(x, T)) for x in energy])
    rhs = np.nan_to_num(rhs * intensity * K / N)
    return cumtrapz(rhs, frequency)[-1]

if __name__ == "__main__":
    pass