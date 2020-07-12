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