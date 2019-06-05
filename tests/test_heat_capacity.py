from pgm.heat_capacity import *
import numpy as np
import matplotlib.pyplot as plt
if __name__ == "__main__":
    dis_temp = [300, 1000, 2000, 3000,4000, 5000, 6000, 7000, 8000]
    temperature = np.linspace(300, 8000, 771)
    temp_list = list(temperature)
    pressure = np.linspace(51, 449, 450)

    cv, v = cvqha(450, 1.2, dis_temp, temperature, path='data/epaw0/upto_400GPa/%sK/input.txt')
    all_cv = []
    murphy_volumes = np.array([5.92, 5.81, 5.56, 5.36, 5.27, 5.15, 5, 4.89, 4.81, 4.70, 4.58])
    murphy_s = np.array([2.63, 2.57, 2.38, 2.24, 2.20, 2.10, 2.01, 1.92, 1.87, 1.81, 1.70])
    murphy_cv = np.array([2.62, 2.60, 2.54, 2.49, 2.47, 2.44, 2.40, 2.36, 2.33, 2.30, 2.25])
    plt.plot(v/2, ry_to_kb(cv[0])/2, label = 'SQHA')
    plt.scatter(cm3_mol_to_b3(murphy_volumes), murphy_cv, label = 'Murphy')
    plt.xlabel('Volume(cm$^3$/mol)')
    plt.ylabel('C$_V$(K$_B$)')
    plt.legend()
    plt.show()