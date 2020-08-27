import numpy as np


def find_value(value, target_list):
    """
    find index of the value in a target list
    """
    target_list = np.array(target_list)
    return np.argmin(np.abs(target_list - value))

def vectorized_find_nearest(array, values, result):
    """
    A vectorized version of function ``find_nearest``.
    :param array: An array of monotonic increasing real numbers.
    :param values: An array of values, each of which is one between two of the consecutive elements in *array*.
    :param result: An array of indices. It is suggested to generate a vector of zeros by ``numpy`` package.
    :return: The *result*, an array of indices mentioned above.
    """
    n: int = len(array)

    if len(values) != len(result):
        raise ValueError('The *values* and *result* arguments should have same length!')

    for i in range(len(values)):

        if values[i] <= array[0]:
            result[i] = 0
        elif values[i] >= array[-1]:
            result[i] = n - 2

        j_low = 0  # Initialize lower limit.
        j_up = n - 1  # Initialize upper limit.

        while j_up - j_low > 1:  # If we are not yet done,
            j_mid: int = (j_up + j_low) // 2  # compute a midpoint,
            if values[i] >= array[j_mid]:
                j_low = j_mid  # and replace either the lower limit
            else:
                j_up = j_mid  # or the upper limit, as appropriate.
            # Repeat until the test condition is satisfied.

        result[i] = j_low


def is_monotonic_decreasing(array) -> bool:
    """
    Check whether the *array* is monotonic decreasing or not.
    For example, in QHA calculation, the volumes should be listed as a decreasing array,
    while the pressures should be monotonic increasing.
    This function can be used to check whether the volumes are in the right order.
    .. doctest::
        >>> is_monotonic_decreasing([1, 2, 4, 5, 9])
        False
        >>> is_monotonic_decreasing([2, -5, -10, -20])
        True
    :param array: The array to be evaluated.
    :return: ``True`` if the argument *array* is monotonic decreasing, otherwise ``False``.
    """
    dx = np.diff(array)
    return np.all(dx <= 0)


def is_monotonic_increasing(array) -> bool:
    """
    Check whether the *array* is monotonic increasing or not.
    For example, in QHA calculation, the volumes should be listed as decreasing array,
    and the pressures should be monotonic increasing.
    This function can be used to check whether the pressures are in the right order.
    .. doctest::
        >>> is_monotonic_increasing([1, 2, 4, 5, 9])
        True
        >>> is_monotonic_increasing([2, -5, -10, -20])
        False
    :param array: The array to be evaluated.
    :return: ``True`` if the argument *array* is monotonic increasing, otherwise ``False``.
    """
    dx = np.diff(array)
    return np.all(dx >= 0)