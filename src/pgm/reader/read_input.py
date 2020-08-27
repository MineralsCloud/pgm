#!/usr/bin/env python3
import pathlib
import re
from typing import Iterator, Union, Tuple

import numpy as np
from scientific_string import strings_to_integers
from text_stream import TextStream
from pgm.util.tools import is_monotonic_decreasing


# ===================== What can be exported? =====================
__all__ = ['Input', 'read_input']


class Input:
    """
    A class of pgm input
    """
    def __init__(self, path_to_dir, discrete_temperature):
        #TODO:add path checker
        self.input_path = [path_to_dir % str(x) for x in discrete_temperature]
        self.__temperatures = discrete_temperature
        rs = {}
        for temp in discrete_temperature:
            path = path_to_dir % str(temp)
            rs[temp] = read_input(path)

        self.__rs = rs

    def get_input(self):
        return self.__rs

    def get_temperature(self):
        return self.__temperatures


def read_input(inp: Union[str, pathlib.PurePath]):
    """
    Read the standard "input" file for ``qha``.

    :param inp: The filename or its path.
    :return: The input data. They are

        - the number of formula unit in a unit cell,
        - the number of volumes in *inp*,
        - the static energies of each volume,
        - a 3D array, i.e., the frequencies of each volume of each q-point of each mode, and
        - a vector of weights of each q-point, respectively.
    """
    """
    .. module read_input
       :platform: Unix, Windows, Mac, Linux
       :synopsis: Read file and write calculated value to files.
    .. moduleauthor:: Qi Zhang <qz2280@columbia.edu>
    .. moduleauthor:: Tian Qin <qinxx197@umn.edu>
    """
    text_stream = TextStream(pathlib.Path(inp))
    gen: Iterator[str] = text_stream.generator_telling_position()

    volumes_amount = None
    q_points_amount = None
    modes_per_q_point_amount = None
    formula_unit_number = None
    offset = 0

    # Now we start reading some metadata.
    regex0 = re.compile("\s*(\d+)[\s,]*(\d+)[\s,]*(\d+)[\s,]*(\d+)")

    for line, offset in gen:
        if not line.strip() or line.startswith('#'):
            continue
        match = regex0.search(line)
        if match is None:
            continue
        else:
            volumes_amount, q_points_amount, modes_per_q_point_amount, formula_unit_number = strings_to_integers(
                match.groups())
            break

    # If the metadata is not found, check the *inp*!
    if any(_ is None for _ in (volumes_amount, q_points_amount, modes_per_q_point_amount)):
        raise ValueError("At least one of the desired values 'nv', 'nq', 'np' is not found in file {0}!".format(inp))

    # Generate containers for storing the following data.
    volumes = np.empty(volumes_amount, dtype=float)
    static_energies = np.empty(volumes_amount, dtype=float)
    frequencies = np.empty((volumes_amount, q_points_amount, modes_per_q_point_amount), dtype=float)
    q_weights = np.empty(q_points_amount, dtype=float)

    # We start a new iterator from where we stopped.
    gen = text_stream.generator_starts_from(offset)

    i = 0  # volume count
    j = 0  # q-point index, note it is not count like `i`!

    # Now we start reading the energies, volumes, and frequencies.
    regex1 = re.compile("P\s*=\s*-?\d*\.?\d*\s*V\s*=(\s*\d*\.?\d*)\s*E\s*=\s*(-?\d*\.?\d*)", re.IGNORECASE)

    for line in gen:
        if not line.strip():
            continue

        if '=' in line:
            match = regex1.search(line)
            if match is None:
                raise ValueError("Search of pattern {0} failed in line '{1}!".format(regex1.pattern, line))
            else:
                volumes[i], static_energies[i] = match.groups()
                i += 1
                j = 0
            continue

        sp = line.split()
        if len(sp) == 3:
            for k in range(modes_per_q_point_amount):  # Note `k` is the index of mode, like `j`, not count like `i`.
                line = next(gen)
                frequencies[i - 1, j, k] = line

            j += 1
            continue

        if 'weight' in line.lower():
            break

    # Now we start reading q-point-weights. We start the exact iterator from where we stopped.
    j = 0

    for line in gen:
        if not line.strip():
            continue

        q_weights[j] = line.split()[-1]  # This line has format: q_x q_y q_z weight, and only weight is taken
        j += 1

    if i != volumes_amount:
        raise ValueError('The number of volumes detected is not equal to what specified in head! Check your file!')

    if not is_monotonic_decreasing(volumes):
        raise ValueError('The volumes in the input file is not monotonicly decreasing, please check your input file')

    return formula_unit_number, volumes, static_energies, frequencies, q_weights
