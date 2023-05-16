import pytest
import numpy
from pgm.plot.plotter import Plot

error_paras = [
    (None, numpy.array([10.0, 20.0, 30.0]), numpy.array([10.0, 20.0, 30.0]), 'tests/data/cp_tp_jmol_K_gpa', 'outname'),
    (numpy.array([10.0, 20.0, 30.0]), None, numpy.array([10.0, 20.0, 30.0]), 'tests/data/cp_tp_jmol_K_gpa', 'outname'),
    (numpy.array([10.0]), numpy.array([1500.0, 1600.0, 1700.0]), None, 'tests/data/cp_tp_jmol_K_gpa', 'outname'),
    (numpy.array([10.0]), numpy.array([10.0]), numpy.array([1500.0, 1600.0, 1700.0]), 'tests/data/ftv_ev_a3', 'outname')
]

correct_paras = [(None, numpy.array([30.0, 60.0, 100.0, 140.0]), None, 'tests/data/cp_tp_jmol_K_gpa', 'casio3_cp_vs_t'),
                 (numpy.array([50.01, 45.0, 38.01]), None, None, 'tests/data/ftv_ev_a3', 'ftv_out_vs_t'),
                 (None, None, numpy.array([2000.0, 2500.0, 3000.0]), 'tests/data/cp_tp_jmol_K_gpa', 'casio3_cp_vs_p'),
                 (None, None, numpy.array([2000.0, 2500.0, 3000.0]), 'tests/data/ftv_ev_a3', 'ftv_out_vs_v'),
                 ]


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [error_paras[0]])
def test_check_if_paras_valid_one(volume, pressure, temperature, filename, outname):
    with pytest.raises(ValueError):
        plot_instance = Plot(volume, pressure, temperature, filename, outname)


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [error_paras[1]])
def test_check_if_paras_valid_two(volume, pressure, temperature, filename, outname):
    with pytest.raises(ValueError):
        plot_instance = Plot(volume, pressure, temperature, filename, outname)


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [error_paras[2]])
def test_check_if_paras_valid_three(volume, pressure, temperature, filename, outname):
    with pytest.raises(ValueError):
        plot_instance = Plot(volume, pressure, temperature, filename, outname)


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [error_paras[3]])
def test_check_if_paras_valid_four(volume, pressure, temperature, filename, outname):
    with pytest.raises(ValueError):
        plot_instance = Plot(volume, pressure, temperature, filename, outname)


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [correct_paras[0]])
def test_tp_plot_one(volume, pressure, temperature, filename, outname):
    plot_instance = Plot(volume, pressure, temperature, filename, outname)
    plot_instance.plot()


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [correct_paras[1]])
def test_tp_plot_two(volume, pressure, temperature, filename, outname):
    plot_instance = Plot(volume, pressure, temperature, filename, outname)
    plot_instance.plot()


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [correct_paras[2]])
def test_tp_plot_three(volume, pressure, temperature, filename, outname):
    plot_instance = Plot(volume, pressure, temperature, filename, outname)
    plot_instance.plot()


@pytest.mark.parametrize("volume, pressure, temperature, filename, outname", [correct_paras[3]])
def test_tp_plot_four(volume, pressure, temperature, filename, outname):
    plot_instance = Plot(volume, pressure, temperature, filename, outname)
    plot_instance.plot()
