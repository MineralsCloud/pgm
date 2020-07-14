import matplotlib.pyplot as plt
from pgm.util.unit_conversion import gpa_to_ry_b3, ry_b3_to_gpa, ry_to_j_mol
from pgm.calculator import pgm, spline_interpolation, qha, FreeEnergyCalculation
from pgm.thermo import ThermodynamicProperties
import numpy as np
from pgm.settings import Settings

# science_p = np.array([36.0000,43.3000,44.0000,50.5000,54.7000,51.1000,54.6000,60.0000,71.0000,72.8000,73.3, 39.0000, 57.5000, 46.5000, 47.2000, 57.9000, 54.6000, 54.1000, 58.1000])
# science_p_error = np.array([2.0000,2.2000,2.0000,2.5000,2.7000,2.6000,2.7000,1.3000,1.8000,1.8000, 2.3000, 3.0000, 3.6000, 2.8000, 3.2000, 3.2000, 3.5000, 3.2000, 3.4000])
# science_t = np.array([300,300,300,300,300,300,300,300,300,700.0000, 880.0000,1000.0000,1000.0000,1100.0000,1100.0000,1200.0000,1300.0000,1500.0000,1700.0000])
# science_t_error = np.ones(10) * 100
# science_s = np.array([2.4250,2.5120,2.4780,2.3600,2.2840,2.4000,2.3270,2.2990,2.2710,4.7540,5.3830,5.9830,5.8050,6.2980,6.2980,6.3930,6.6720,7.5880,7.7730])
# science_s_error = np.array([0.0710,0.1180,0.0630,0.0630,0.0780,0.1700,0.0960,0.1190,0.0760,0.0930])
# shen_p = np.array([6.0000, 20.0000, 29.0000, 29.0000, 0,6.0000, 29.0000])
# shen_p_error = np.array([0.5000,1.0000,2.0000,2.0000,0,0.5000,2.0000])
# shen_t = np.array([920.0000,720.0000,430.0000,720.0000,300,300,300])
# shen_t_error = np.array([28.0000,24.0000,18.0000,35.0000])
# shen_s = np.array([6.6800,5.5500,3.6800,5.2500,3.1330,3.3000,2.6600])
# shen_s_error = np.array([0.0800,0.1100,0.1200,0.2300,0.0090,0.0400,0.0600])
# lubber_s = np.array([3.0700,3.0000,2.3100,2.1200,2.06000])
# lubber_s_error = np.array([0,0.0500,0.0500,0.0500,0.0500])
# lubber_p = np.array([0.0000,0.0000,20.0000,32.0000,42.0000])
# murphy_s = np.array([2.63, 2.57, 2.38, 2.24, 2.20, 2.10, 2.01, 1.92, 1.87, 1.81, 1.70])
# murphy_p = np.array([30, 36, 53, 69, 77, 90, 106, 121, 133, 151, 171])
# murphy_p_error = np.array([2, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5])
# murphy_s_error = np.array([0.02, 0.03, 0.03, 0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02])
# mao_s = [2.772151898734177, 2.7088607594936702, 2.2784810126582276, 2.2405063291139244, 1.9746835443037982, 1.962025316455696, 1.9367088607594942]
# mao_p = [25, 36, 50, 70, 112, 133, 153]

if __name__ == "__main__":
    para = {
        'NV': 450,
        'NT': 801,
        'folder': 'data/epaw0/1500GPa/%sK/input.txt',
        'initP': 30,
        'finalP': 400,
        'ratio': 2,
        'output_directory': './results/',
        'temperature': [0, 300, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
    }
    setting = Settings(para)

    calc = FreeEnergyCalculation(setting)
    total_free_energies, vib_entropies, volumes, desired_pressure, continuous_temperature = calc.calculate()
    temperature = setting.continuous_temperature

    # the following three instances are tqha, sqha, and static results.
    # thermodynamics can be computed by using the apis in pgm.thermo
    # tqha = ThermodynamicProperties(tqha_volumes[0], temperature, gpa_to_ry_b3(desired_pressure), tqha_total_free_energies)
    thermo = ThermodynamicProperties(volumes, temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)
    # static = ThermodynamicProperties(sqha_volume, temperature, gpa_to_ry_b3(desired_pressure), static_free_energies)

    ptv = ry_b3_to_gpa(thermo.p_tv)
    bt = ry_b3_to_gpa(thermo.bt_tp)
    alpha = thermo.alpha_tp
    cp = thermo.cp_tp
    cv = thermo.cv_tp

    # save_data(bt, temperature, desired_pressure, 'bt_tp')
    # save_data(cv, temperature, desired_pressure, 'cv_tp')
    # save_data(cp, temperature, desired_pressure, 'cp_tp')
    # save_data(alpha, temperature, desired_pressure, 'alpha_tp')
    # save_data(total_free_energies, temperature, volumes, 'ftv')
    # save_data(ptv, temperature, volumes, 'ptv')
