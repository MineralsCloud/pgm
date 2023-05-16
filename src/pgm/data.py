import gc

import numpy as np
import pandas as pd


def read_data(filename: str) -> pd.DataFrame:
    """
    read from a csv file, basicly qha output style
    """
    df = pd.read_table(filename, sep=",", header=0, index_col=0)
    df.columns = df.columns.astype(float)
    df.index = df.index.astype(float)
    return df


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
