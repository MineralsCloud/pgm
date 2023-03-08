import pytest
from pgm.reader.read_input import Input

settings = [('examples/casio3/%sK.txt', [1500, 2000, 2500, 3000, 3500, 4000]),
            ('examples/feo/%sK.txt', [0, 1000, 2000, 3000, 4000])]


@pytest.mark.parametrize("input_dir,discrete_temp", [settings[0]])
def test_casio3_example(input_dir, discrete_temp):
    input_instance = Input(input_dir, discrete_temp)
    assert input_instance.frequencies.shape == (6, 5, 8000, 15)
    assert input_instance.frequencies[0, 0, 0, 3] == 279.853100


@pytest.mark.parametrize("input_dir,discrete_temp", [settings[1]])
def test_feo_example(input_dir, discrete_temp):
    input_instance = Input(input_dir, discrete_temp)
    assert input_instance.frequencies.shape == (5, 9, 264, 12)
    assert input_instance.frequencies[4, 0, 0, 3] == 302.3405
