import pytest
import numpy
from pgm.plot.plotter import Plot

error_paras = [(None, numpy.array([10.0, 20.0, 30.0]), numpy.array([10.0, 20.0, 30.0]), 'tests/data/cp_tp_jmol_K_gpa'),
               (numpy.array([10.0, 20.0, 30.0]), None, numpy.array([10.0, 20.0, 30.0]), 'tests/data/cp_tp_jmol_K_gpa'),
               (numpy.array([10.0]), None, numpy.array([1500.0, 1600.0, 1700.0]), 'tests/data/cp_tp_jmol_K_gpa'),
               (None, numpy.array([10.0]), numpy.array([1500.0, 1600.0, 1700.0]), 'tests/data/ftv_ev_a3')
               ]

correct_paras = [(None, numpy.array([30.0]), None, 'tests/data/cp_tp_jmol_K_gpa'),

                 ]


# @pytest.mark.parametrize("volume, pressure, temperature, filename", [error_paras[0]])
# def test_check_if_paras_valid_one(volume, pressure, temperature, filename):
#     with pytest.raises(ValueError, match='Temperature and pressure cannot both be array!'):
#         plot_instance = Plot(volume, pressure, temperature, filename)
#
#
# @pytest.mark.parametrize("volume, pressure, temperature, filename", [error_paras[1]])
# def test_check_if_paras_valid_two(volume, pressure, temperature, filename):
#     with pytest.raises(ValueError, match='Temperature and volume cannot both be array!'):
#         plot_instance = Plot(volume, pressure, temperature, filename)
#
#
# @pytest.mark.parametrize("volume, pressure, temperature, filename", [error_paras[2]])
# def test_check_if_paras_valid_three(volume, pressure, temperature, filename):
#     with pytest.raises(ValueError, match=r'not in T/V space!'):
#         plot_instance = Plot(volume, pressure, temperature, filename)
#
#
# @pytest.mark.parametrize("volume, pressure, temperature, filename", [error_paras[3]])
# def test_check_if_paras_valid_four(volume, pressure, temperature, filename):
#     with pytest.raises(ValueError, match=r'not in T/P space!'):
#         plot_instance = Plot(volume, pressure, temperature, filename)


@pytest.mark.parametrize("volume, pressure, temperature, filename", [correct_paras[0]])
def test_tp_plot(volume, pressure, temperature, filename):
    plot_instance = Plot(volume, pressure, temperature, filename)
    plot_instance.plot()
