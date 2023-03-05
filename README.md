# <i>pgm</i>: phonon gas model
Calculate thermodynamic properties of matter using phonon gas model(PGM)

[![GitHub Actions](https://github.com/MineralsCloud/pgm/actions/workflows/documentation.yml/badge.svg)](https://mineralscloud.github.io/pgm/index.html)

[![pypi](https://img.shields.io/pypi/v/pgm.svg)](https://pypi.org/project/pgm/)
[![pypi](https://img.shields.io/pypi/dm/pgm.svg)](https://pypi.org/project/pgm/)

## Contributors
![](https://img.shields.io/github/contributors/MineralsCloud/pgm)

This repository is authored and maintained by [Hongjin Wang][1] and [Jingyi Zhuang][2].

[1]: https://github.com/underhill1886

[2]: https://github.com/jappoker


## Installation
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
See details [Installation of pgm](https://mineralscloud.github.io/pgm/basics/installation.html).


## How to use
Here we provide two examples inside the example folder. One is CaSiO3, and one is Hcp Iron

Simply run

``cd examples/casio3``

``pgm run casio3.yaml``

See details [Command Line Tool of pgm](https://mineralscloud.github.io/pgm/basics/cli.html).

## Use your own example
First, you need to prepare a set of phonon calculations calculated at different temperatures.

Convert them as standard qha input files(for now use input converter in qha pkg), and put the input files like in the case of CaSiO3 or hcp iron

Compose your own `settings.yaml` file, enjoy.

Details TBD.

## Documentation

See [GitHub pages of pgm][3].

[3]: https://mineralscloud.github.io/pgm/


## How to cite
... TBD
 
