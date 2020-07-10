#!/usr/bin/env python3
"""
.. module v2p
   :platform: Unix, Windows, Mac, Linux
   :synopsis:
.. moduleauthor:: Tian Qin <qinxx197@umn.edu>
.. moduleauthor:: Qi Zhang <qz2280@columbia.edu>
.. moduleauthor:: Hongjin Wang <hw2626@columbia.edu>
"""

# import numba
import numpy as np

from pgm.util.tools import find_value, vectorized_find_nearest

# ===================== What can be exported? =====================
__all__ = ['v2p']


# @numba.jit(nopython=True, parallel=True)
def lagrange4(x: float, x0, x1, x2, x3, y0, y1, y2, y3) -> float:
    """
    A third-order Lagrange polynomial function. Given 4 points for interpolation:
    :math:`(x_0, y_0), \\ldots, (x_3, y_3)`, evaluate the Lagrange polynomial on :math:`x`.

    :param x: The x-coordinate of the point to be evaluated.
    :param x0: The x-coordinate of the 1st point.
    :param x1: The x-coordinate of the 2nd point.
    :param x2: The x-coordinate of the 3rd point.
    :param x3: The x-coordinate of the 4th point.
    :param y0: The y-coordinate of the 1st point.
    :param y1: The y-coordinate of the 2nd point.
    :param y2: The y-coordinate of the 3rd point.
    :param y3: The y-coordinate of the 4th po`int.
    :return: The y-coordinate of the point to be evaluated.
    """
    return (x - x1) * (x - x2) * (x - x3) / (x0 - x1) / (x0 - x2) / (x0 - x3) * y0 + \
           (x - x0) * (x - x2) * (x - x3) / (x1 - x0) / (x1 - x2) / (x1 - x3) * y1 + \
           (x - x0) * (x - x1) * (x - x3) / (x2 - x0) / (x2 - x1) / (x2 - x3) * y2 + \
           (x - x0) * (x - x1) * (x - x2) / \
           (x3 - x0) / (x3 - x1) / (x3 - x2) * y3


def v2p(func_of_t_v, p_of_t_v, desired_pressures):
    """
    Obtain :math:`f(T, P)` given :math:`f(T, V)` and :math:`P(T, V)` by doing a fourth-order Lagrangian interpolation.

    :param func_of_t_v: Any function :math:`f` on :math:`(T, V)` grid, which has
        shape: (number of temperature, number of volumes).
    :param p_of_t_v: Pressures on :math:`(T, V)` grid, which has
        shape: (number of temperature, number of volumes).
    :param desired_pressures: A vector of pressures which user wants to apply.
    :return: The interpolated function :math:`f` on :math:`(T, P)` grid.
    """
    # Assume the function is temperature in row and volume in column
    t_amount, v_amount = func_of_t_v.shape

    desired_pressures_amount = len(desired_pressures)

    result = np.empty((t_amount, desired_pressures_amount))

    # Put three parts together
    # third column, function tv, last fourth column
    # TODO: Still confused of the artificial choice of 3 and -4. Why? Can't I just use 0 and -1 lmao?
    # Made a little test, feel like 0 and -1 is fine by me. Stick to 0 -1 for now.
    extended_f = np.hstack(
        (func_of_t_v[:, 0].reshape(-1, 1), func_of_t_v, func_of_t_v[:, -1].reshape(-1, 1)))
    extended_p = np.hstack(
        (p_of_t_v[:, 0].reshape(-1, 1), p_of_t_v, p_of_t_v[:, -1].reshape(-1, 1)))

    # Proceed row by row
    for i in range(t_amount):
        rs = np.zeros(desired_pressures_amount)

        # Search desired pressures in the extended p array
        if (np.min(desired_pressures) > np.max(extended_p[i])) or (np.max(desired_pressures) < np.min(extended_p[i])):
            raise ValueError("Desired pressure is out of bound. Try to change the volume expansion ratio.")
        else:
            vectorized_find_nearest(extended_p[i], desired_pressures, rs)

        for j in range(desired_pressures_amount):
            # The index of found desired pressure in the extended p
            k = int(rs[j])

            x1, x2, x3, x4 = extended_p[i, k: k + 4]
            f1, f2, f3, f4 = extended_f[i, k: k + 4]

            result[i, j] = lagrange4(
                desired_pressures[j], x1, x2, x3, x4, f1, f2, f3, f4)
    return result
