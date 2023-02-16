# pgm
Calculate thermodynamic properties of matter using phonon gas model(PGM)

## Install
``pip install -r requirements.txt``

``pip install .``


## How to use
Here we provide two examples inside the example folder. One is CaSiO3, and one is Hcp Iron

Simply run

``cd examples/casio3``

``pgm run casio3.yaml``

## Use your own example
First, you need to prepare a set of phonon calculations calculated at different temperatures.

Convert them as standard qha input files(for now use input converter in qha pkg), and put the input files like in the case of CaSiO3 or hcp iron

Compose your own `settings.yaml` file, enjoy.

 
