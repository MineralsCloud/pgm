import matplotlib.pyplot as plt
from pgm.data import read_data
import numpy


class Plot:
    def __init__(self, volume, pressure, temperature, filename):
        self.volume = volume
        self.pressure = pressure
        self.temperature = temperature
        self.filename = filename
        self.check_if_paras_valid()
        self.df = read_data(filename)

    def check_if_paras_valid(self):
        """
        Check whether the parameters are valid
        Rules: the code would plot one or more T/P T/V lines
        If the temperatures has more than one value, pressures/volumes cannot be, vice versa.
        """
        # if self.volume is not None:  # T/V
        #     if len(self.volume) > 1 and len(self.temperature) > 1:
        #         raise ValueError('Temperature and volume cannot both be array!')
        #     if 'tv' not in self.filename:
        #         raise ValueError(f'{self.filename} is not in T/V space!')
        # if self.pressure is not None:  # T/P
        #     if len(self.pressure) > 1 and len(self.temperature) > 1:
        #         raise ValueError('Temperature and pressure cannot both be array!')
        #     if 'tp' not in self.filename:
        #         raise ValueError(f'{self.filename} is not in T/P space!')
        pass

    def plot(self):
        """
        Plot the target file using parameters provided
        """
        line = self.df.loc[:, str(self.pressure[0])].values
        plt.plot(numpy.array(self.df.index.values[4:-4], dtype=float), line[4:-4])

        plt.savefig('test.png')
        print(self.df.columns.values)
        print(self.df.index.values)
