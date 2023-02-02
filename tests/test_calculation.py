from test_interpolation import brute_force_numba
from pgm.reader.read_input import Input
import numpy
import time
import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from scipy.constants import physical_constants as pc
from scipy.integrate import cumtrapz
from pgm.calculator import entropy, integrate

K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]
HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]

if __name__ == "__main__":
    dir = "./examples/casio3/%sK.txt"
    temp = [1500, 2000, 2500, 3000, 3500, 4000]
    interpolated_temp = numpy.linspace(1500, 4000, 250)
    input = Input(dir, temp)
    weight = input.weights[0]  # here of course ensure that all weights are the same
    s_vib = numpy.empty((250, 5))  # S(T,V)
    freq = brute_force_numba(input)
    start = time.time()
    for i in range(len(interpolated_temp)):
        s_vib[i] = entropy(interpolated_temp[i], freq[i], weight)
    end = time.time()
    print("time for calculate s_vib is", end - start, "s")
    start = time.time()
    f_vib = integrate(interpolated_temp, s_vib)
    end = time.time()
    print(f_vib)
    print("time for calculate f_vib is", end - start, "s")