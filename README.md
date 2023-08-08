# <i>pgm</i>: A Python package for free energy calculations within the phonon gas model
Calculate thermodynamic properties of matter using phonon gas model(PGM)

[![GitHub Actions](https://github.com/MineralsCloud/pgm/actions/workflows/documentation.yml/badge.svg)](https://mineralscloud.github.io/pgm/index.html)
[![pypi](https://img.shields.io/pypi/v/phonon-gas-model.svg)](https://pypi.org/project/phonon-gas-model/)
[![pypi](https://img.shields.io/pypi/dm/phonon-gas-model.svg)](https://pypi.org/project/phonon-gas-model/)

## Contributors

This repository is authored and maintained by [Hongjin Wang][1] and [Jingyi Zhuang][2].

[1]: https://github.com/underhill1886

[2]: https://www.jappoker.com/

## How to cite

The associated paper is published [online here](https://authors.elsevier.com/c/1hQ5e_FEhOCgU).

Please cite this article as: 

Hongjin Wang, Jingyi Zhuang, Zhen Zhang, Qi Zhang, Renata M. Wentzcovitch, pgm: A Python package for free energy calculations within the phonon gas model, Computer Physics Communications (2023), Volume 291, 2023, 108845, [https://doi.org/10.1016/j.cpc.2023.108845](https://doi.org/10.1016/j.cpc.2023.108845).

If you are unable to access the full text of this article, please contact the authors.

## Installation
### Install from PyPI
You can install the package directly from PyPI:
```shell
$ pip install phonon-gas-model
```


### Manual install
To install the ``pgm`` package, first clone the code repository using ``git``:
```shell
$ git clone https://github.com/MineralsCloud/pgm.git
```

After cloning the code repository, change to the code directory using ``cd``:
``` shell
$ cd pgm
```

After changing to the code directory, install the required Python packages using ``pip``:
```shell
$ pip install -r requirements.txt
```

Finally, install the pgm package using ``pip``:
```shell
$ pip install .
```
See details in [Installation of pgm](https://mineralscloud.github.io/pgm/basics/installation.html).


## How to use
Here we provide two examples inside the example folder. One is CaSiO₃, and one is B8-FeO.

For the case of CaSiO₃, simply run the following commands from the root path of the package:

```shell
$ cd examples/casio3
```

```shell
$ pgm run casio3.yaml
```

and for another case, B8-FeO,

run the following commands from the root path of the package:

```shell
$ cd examples/feo
```

```shell
$ pgm run feo.yaml
```

See details [Command Line Tool of pgm](https://mineralscloud.github.io/pgm/basics/cli.html).

## Use your own example
First, you need to prepare a set of phonon calculations calculated at different temperatures.

Convert them as standard qha input files(for now use input converter in qha pkg), and put the input files like in the case of CaSiO₃ or B8-FeO

Compose your own `settings.yaml` file, enjoy.

Details will be provide shortly.

## Documentation

See [GitHub pages of pgm][3].

[3]: https://mineralscloud.github.io/pgm/

 
