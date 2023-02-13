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
from pgm.interpolate import Interpolation, FrequencyInterpolation
from pgm.util.unit_conversion import ry_to_ev, b3_to_a3
import pandas

K = pc['Boltzmann constant in eV/K'][0] / pc['Rydberg constant times hc in eV'][0]
HBAR = 100 / pc['electron volt-inverse meter relationship'][0] / pc['Rydberg constant times hc in eV'][0]

if __name__ == "__main__":
    dir = "./examples/casio3/%sK.txt"
    temp = [1500, 2000, 2500, 3000, 3500, 4000]
    interpolated_temp = numpy.linspace(1500, 4000, 251)
    input = Input(dir, temp)
    weight = input.weights[0]  # here of course ensure that all weights are the same
    s_vib = numpy.empty((251, 5))  # S(T,V)
    # freq = brute_force_numba(input)  # runtime is 4.795620918273926 s
    inter = FrequencyInterpolation(input)
    freq = inter.numba_polyfit(interpolated_temp, DEBUG=True)
    start = time.time()
    # Very slow here
    for i in range(len(interpolated_temp)):
        s_vib[i] = entropy(interpolated_temp[i], freq[i], weight)
    end = time.time()
    print("time for calculate s_vib is", end - start, "s")
    # time for calculate s_vib is 61.31389832496643 s
    start = time.time()
    f_vib = integrate(interpolated_temp, s_vib)
    end = time.time()
    # print(f_vib)
    print("time for calculate f_vib is", end - start, "s")
    # time for calculate f_vib is 0.00027251243591308594 s
    raw_E = input.static_energy[0]  # E(V) from input
    raw_V = input.volumes  # V
    inter = Interpolation(raw_V, num=151, ratio=1.2)
    # E = inter.fitting(raw_E)
    F_total = f_vib + raw_E - 1500 * s_vib[0]
    F_total_fitted = numpy.empty((251, 151))
    start = time.time()
    for i in range(len(interpolated_temp)):
        F_total_fitted[i] = inter.fitting(F_total[i])
    end = time.time()
    print("time for interpolate F total along volume is", end - start, "s")
    # time for interpolate F total along volume is 0.007174015045166016 s
    print(F_total_fitted)

    # plot final F(T,V) results_old against previous method
    df = pandas.read_table("./examples/casio3/results_old/ftv_ev_a3", sep=',', header=0, index_col=0)
    df_v = numpy.array(df.columns.values, dtype=float)
    v = inter.fitting(raw_V)
    # print(df_v - b3_to_a3(v))
    for t in range(5):
        i = numpy.random.randint(0, 251)
        plt.plot(df_v, df.values[i], color='black')
        plt.plot(b3_to_a3(v), ry_to_ev(F_total_fitted[i]), color='r', linestyle='dashed')
    # print(df)
    plt.savefig('interpolation_calculation.png')
