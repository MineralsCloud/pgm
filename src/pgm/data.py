import pandas as pd
import numpy as np
import gc
# from geothermpy import bind, Point
from scipy.optimize import curve_fit


def read_tp(filename='TP'):
    return pd.read_csv(filename, delim_whitespace=True, names=['T', 'P', 'dT/dP'])


def read_data(filename: str, index_col) -> pd.DataFrame:
    """
    read from a csv file, basicly qha output style
    """
    return pd.read_csv(filename, delim_whitespace=True, index_col=index_col)


# def generate_adiabatic_tp(geotherm, index, columns, init_p = 55, init_t = 1717):
#     """
#     generate adiabatic temperature vs pressure from a geotherm matrix
#     """
#     gg = pd.DataFrame(geotherm, index = index, columns =columns)
#     trace = bind.generate_trace(gg, Point(init_p, init_t), h=0.02, n=100000)
#     xs, ys = np.array([p.x for p in trace]), np.array([p.y for p in trace])
#     return xs, ys

def save_data(quantities, index, column, filename):
    """
    save a matrix quantity to csv
    The saved files can be easily parsed using
    pandas.read_table("PATH_TO_FILE", sep=',', header=0, index_col=0)
    """
    df = pd.DataFrame(quantities, index=index, columns=column)
    df.to_csv(filename)
    gc.collect()


def save_line(filename, xlabel, ylabel, x, y):
    """
    save a 2d line to csv
    """
    d = {xlabel: x, ylabel: y}
    df = pd.DataFrame(data=d)
    df.to_csv(filename)
    gc.collect
