import matplotlib as mpl
import matplotlib.pyplot as plt
from pgm.util.unit_conversion import gpa_to_ry_b3, ry_b3_to_gpa, ry_to_j_mol, ry_to_ev, b3_to_a3
from pgm.util.tools import find_value
from pgm.calculator import pgm, spline_interpolation, qha, FreeEnergyCalculation
from pgm.thermo import ThermodynamicProperties
from pgm.data import save_data
from pgm.reader.read_input import Input
import numpy as np

color_list=[(0.37254901960784315, 0.27450980392156865, 0.5647058823529412), (0.11372549019607843, 0.4117647058823529, 0.5882352941176471), (0.2196078431372549, 0.6509803921568628, 0.6470588235294118), (0.058823529411764705, 0.5215686274509804, 0.32941176470588235), (0.45098039215686275, 0.6862745098039216, 0.2823529411764706), (0.9294117647058824, 0.6784313725490196, 0.03137254901960784), (0.8823529411764706, 0.48627450980392156, 0.0196078431372549), (0.8, 0.3137254901960784, 0.24313725490196078), (0.5803921568627451, 0.20392156862745098, 0.43137254901960786), (0.43529411764705883, 0.25098039215686274, 0.4392156862745098), '#93C088']

if __name__ == "__main__":
    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 22}

    # mpl.rc('font', **font)
    mpl.rcParams['axes.linewidth'] = 1.8
    # mpl.rcParams['mathtext.fontset'] = 'stix'

    NV = 501
    NT = 251
    folder = 'data/casio3/%sK.txt'
    initP = 0
    finalP = 150
    ratio = 1.2  # must be the same as qha input


    discrete_temperatures = [1500, 2000, 2500, 3000, 3500, 4000]
    temperature = np.linspace(1500, 4000, NT)

    temp_list = list(temperature)

    desired_pressure = np.linspace(0, 500, NV)
    # folder = 'data/output/%sK/input.txt'


    calc = FreeEnergyCalculation(NV, NT, initP, finalP, ratio, discrete_temperatures, folder)
    total_free_energies, vib_entropies, volumes, desired_pressure, continuous_temperature = calc.calculate()
    interpolation = ThermodynamicProperties(volumes, temperature, gpa_to_ry_b3(desired_pressure), total_free_energies)
    sqha_volume = b3_to_a3(volumes)

    # energies[0] = energies[1]

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    vols = b3_to_a3(sqha_volume)
    plt.figure(figsize=(5, 4))

    v = 44.39
    index_v = find_value(vols, v)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V1")

    plt.scatter(discrete_temperatures, [-42.55006652, - 43.92111448, -
    45.44998553, - 47.10515852, - 48.86583903, - 50.71736489])

    v = 40.258321495537544
    index_v = find_value(vols, v)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V2")

    plt.scatter(discrete_temperatures, [-41.89413855, - 43.17445305, -
    44.61424974, - 46.1817799, - 47.85587506, - 49.62144974])

    v = 36.7689539353574
    index_v = find_value(vols, v)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V3")

    plt.scatter(discrete_temperatures, [-40.58847835, - 41.79457502, -
    43.15998955, - 44.65348588, - 46.25422376, - 47.94737818])

    v = 34.34308402343736
    index_v = find_value(vols, v)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V4")

    plt.scatter(discrete_temperatures, [-39.05674738, - 40.20836091, -41.51877576, - 42.9571361, - 44.5028067, - 46.14109688])

    v = 32.487552716802675
    index_v = find_value(vols, v)

    plt.plot(temperature[0:], ry_to_ev(
        total_free_energies[:, index_v][0:]), lw=3, label="V5")

    plt.scatter(discrete_temperatures, [-37.42369011, - 38.533426, -
    39.802252, - 41.19922512, - 42.70347289, - 44.30001018])

    plt.xlabel("$T$ (K)")
    plt.ylabel("$F$ (eV)")
    plt.title(
        "Helmholtz free energy of CaSiO$_3$\nby entropy integration (lines) and Zhen's (dots)")

    plt.legend(frameon=False)
    plt.savefig("5-3-check-new-U.png", dpi=300)

    plt.close('all')

    # for i in [2000,3000,4000]:
    #     plt.plot(desired_pressure, 10**5*(
    #             interpolation.alpha_tp[find_value(temperature, i)]),label = i)
    #     plt.plot(ry_b3_to_gpa(
    #         interpolation.p_tv[find_value(temperature, i)]), vols,ls="dotted")
    #     plt.plot(desired_pressure, b3_to_a3(
    #         interpolation.v_tp[find_value(temperature, i)]), label=i)
    # plt.ylim(32,46)
    # plt.xlim(0,200)

    # print(_interpolation.alpha_tp)
    fig = plt.figure(figsize=(8, 7))

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    for ind, i in enumerate([30, 60, 100, 140]):
        c = 2 * ind + 1
        # plt.plot(temperature, 10**5*(
        #     tqha.alpha_tp[:, find_value(desired_pressure, i)]), label=i)

        ax1.plot(temperature[5:-5], 10 ** 5 * (
                                                  interpolation.alpha_tp[:, find_value(desired_pressure, i)])[5:-5],
                 label=i, color=color_list[c])
        ax1.set_ylim(0.5, 3.5)
        ax1.set_xlim(1500, 4000)
        ax1.set_xlabel("T (K)")
        ax1.set_ylabel("$\\alpha$ (10$^5$ K$^{-1}$)")

        # plt.plot(temperature, b3_to_a3(
        #     interpolation.v_tp[:, find_value(desired_pressure, i)]), label=i)

        ax2.plot(temperature[5:-5], ry_to_j_mol(
            interpolation.cp_tp[:, find_value(desired_pressure, i)])[5:-5], label="%s GPa" % (i), color=color_list[c])

        ax2.plot(temperature[5:-5], ry_to_j_mol(
            interpolation.cv_tp[:, find_value(desired_pressure, i)])[5:-5], ls="dashed", color=color_list[c])
        # ax2.hlines(125, 1500, 4000, ls="dotted",color="k")
        ax2.set_ylim(105, 150)
        ax2.set_xlim(1500, 4000)
        ax2.set_ylabel("Cp (solid) Cv(dashed) (J mol$^{-1}$ K$^{-1}$)")
        ax2.set_xlabel("T (K)")

        ax3.plot(temperature[5:-5],
                 interpolation.gamma_tp[:, find_value(desired_pressure, i)][5:-5], label="%s GPa" % (i),
                 color=color_list[c])

        ax3.set_xlim(1500, 4000)
        ax3.set_ylim(1.1, 1.6)
        ax3.set_ylabel("$\\gamma$")
        ax3.set_xlabel("T (K)")

        ax4.plot(temperature[5:-5], ry_b3_to_gpa(
            interpolation.bs_tp[:, find_value(desired_pressure, i)])[5:-5], label="%s GPa" % (i), color=color_list[c])
        ax4.set_ylim(200, 800)
        ax4.set_xlim(1500, 4000)
        ax4.set_ylabel("Ks (GPa")
        ax4.set_xlabel("T (K)")

        # plt.plot(temperature[10:-11], np.diff( ry_to_ev(
        #     interpolation.u_tp[:, find_value(desired_pressure, i)])[10:-10]), label="%s %s GPa" % ("dU", i))

        # plt.plot(temperature[10:-11], np.diff(ry_to_ev(
        #     interpolation.s_tp[:, find_value(desired_pressure, i)])[10:-10]), label="%s %s GPa" % ("S", i))

        # plt.plot(temperature[10:-10], (ry_to_ev(
        #     interpolation.s_tp[:, find_value(desired_pressure, i)])[10:-10]), label="%s %s GPa" % ("S", i))

    for ax in [ax1, ax2, ax3, ax4]:
        ax.legend(frameon=False, fontsize=7)
    plt.savefig("tmp.png", dpi=300)
