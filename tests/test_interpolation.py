import jax.numpy as jnp
import numpy
import numpy as np
import matplotlib
import time
import matplotlib.pyplot as plt
from pgm.reader.read_input import Input
from numba import njit, prange, jit

matplotlib.use('Agg')


@jit(nopython=True)
def _coeff_mat(x, deg):
    mat_ = np.zeros(shape=(x.shape[0], deg + 1))
    const = np.ones_like(x)
    mat_[:, 0] = const
    mat_[:, 1] = x
    if deg > 1:
        for n in range(2, deg + 1):
            mat_[:, n] = x ** n
    return mat_


@jit(nopython=True)
def _fit_x(a, b):
    # linalg solves ax = b
    det_ = np.linalg.lstsq(a, b)[0]
    return det_


@jit(nopython=True)
def fit_poly(x, y, deg):
    a = _coeff_mat(x, deg)
    p = _fit_x(a, y)
    # Reverse order so p[0] is coefficient of highest order
    return p[::-1]


@jit(nopython=True)
def eval_polynomial(P, x):
    '''
    Compute polynomial P(x) where P is a vector of coefficients, highest
    order coefficient at P[0].  Uses Horner's Method.
    '''
    result = np.zeros_like(x)
    for coeff in P:
        result = x * result + coeff
    return result


def brute_force(input: Input):
    start = time.time()
    interpolated_freq = numpy.zeros((250, 5, 8000, 15))
    interpolated_temp = numpy.linspace(1500, 4000, 250)
    temp = numpy.array([1500, 2000, 2500, 3000, 3500, 4000])
    for i in range(5):
        for j in range(8000):
            for k in range(15):
                x = temp
                y = input.frequencies[:, i, j, k]
                z = numpy.polyfit(x, y, 2)  # quadratic form
                interpolated_freq[:, i, j, k] = numpy.polyval(z, interpolated_temp)
    print(interpolated_freq.size * interpolated_freq.itemsize, "bytes")
    end = time.time()
    print("runtime is", (end - start), "s")
    return interpolated_freq


def brute_force_numba(input: Input):
    start = time.time()
    interpolated_freq = numpy.zeros((250, 5, 8000, 15))
    interpolated_temp = numpy.linspace(1500, 4000, 250)
    temp = numpy.array([1500, 2000, 2500, 3000, 3500, 4000])
    for i in range(5):
        for j in range(8000):
            for k in range(15):
                x = temp
                y = input.frequencies[:, i, j, k]
                p_coeffs = fit_poly(x, y, 2)  # quadratic form
                interpolated_freq[:, i, j, k] = eval_polynomial(p_coeffs, interpolated_temp)
    print(interpolated_freq.size * interpolated_freq.itemsize, "bytes")
    end = time.time()
    print("runtime is", (end - start), "s")
    return interpolated_freq


def brute_force_jax():
    NotImplemented
    start = time.time()
    interpolated_freq = numpy.zeros((250, 5, 8000, 15))
    interpolated_temp = jnp.linspace(1500, 4000, 250)
    temp = jnp.array([1500, 2000, 2500, 3000, 3500, 4000], dtype=float)
    for i in range(5):
        for j in range(8000):
            for k in range(15):
                x = temp
                y = jnp.array(input.frequencies[:, i, j, k])
                z = jnp.polyfit(x, y, 2)  # quadratic form
                interpolated_freq[:, i, j, k] = jnp.polyval(z, interpolated_temp)
    print(interpolated_freq.size * interpolated_freq.itemsize, "bytes")
    end = time.time()
    print("runtime is", (end - start), "s")
    return interpolated_freq


def numba_numpy():
    NotImplemented
    start = time.time()
    # interpolated_freq = numpy.empty((250, 5, 8000, 15))
    interpolated_freq = []
    interpolated_temp = numpy.linspace(1500, 4000, 250)
    temp = numpy.array([1500, 2000, 2500, 3000, 3500, 4000])
    freq = input.frequencies

    @njit(parallel=True)
    def numba_loop():
        for i in prange(5):
            for j in prange(8000):
                for k in prange(15):
                    x = temp
                    y = freq[:, i, j, k]
                    p_coeffs = fit_poly(x, y, 2)  # quadratic form
                    # eval_polynomial(p_coeffs, interpolated_temp)
                    print(p_coeffs)
                    # rs.append(eval_polynomial(p_coeffs, interpolated_temp))
                    # interpolated_freq.append(eval_polynomial(p_coeffs, interpolated_temp))
                    interpolated_temp = numpy.vectorize(eval_polynomial)(temp)

    numba_loop()
    # numpy reshape
    interpolated_freq = numpy.array(interpolated_freq)
    interpolated_freq.reshape((250, 5, 8000, 15))
    print(interpolated_freq.size * interpolated_freq.itemsize, "bytes")
    end = time.time()
    print("runtime is", (end - start), "s")
    return interpolated_freq


if __name__ == "__main__":
    dir = "./examples/casio3/%sK.txt"
    temp = [1500, 2000, 2500, 3000, 3500, 4000]
    input = Input(dir, temp)
    # rs = input.get_input()
    # print(rs[2000][3])
    print(input.frequencies.size * input.frequencies.itemsize, "bytes")
    # freq = brute_force(input)
    freq = brute_force_numba(input)

    # plot random freq interpolation results
    interpolated_temp = numpy.linspace(1500, 4000, 250)
    for t in range(10):
        i, j, k = numpy.random.randint([0, 0, 0], [5, 8000, 15])
        plt.plot(interpolated_temp, freq[:, i, j, k])
        plt.scatter(temp, input.frequencies[:, i, j, k])
    plt.savefig('interpolation_test.png')
