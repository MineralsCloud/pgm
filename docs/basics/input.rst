Input Files
===========

The pgm code has two types of input files as described in the following contents: 

1. a user-specified control file ``settings.yaml``
2. a series of data files ``input-*K``



.. table:: Table 3: Files needed for using the code

    +-----------------+-------------------------------------------------+
    | File name       | Description                                     |
    +=================+=================================================+
    | settings.yaml   | | Settings file for pgm calculation, the user   |
    |                 | | can set the temperatures, pressures, input    |
    |                 | | file structures, and output files.            |
    +-----------------+-------------------------------------------------+
    |                 | | Each input data file contains the volumes,    |
    | | input-0K,     | | static total energies, and frequencies from   |
    | | input-300K,   | | ab initio calculations at its temperature as  |
    | | input-1000K…  | | specified in the input file name.             |
    +-----------------+-------------------------------------------------+


Configuration File ``settings.yaml``
-----------------------------------

The configuration file is a ``YAML`` file that contains various parameters and settings used by the program. The format of the configuration file is as follows:

.. code-block:: text

    # This is the example of FeO
    # examples/feo/feo.yaml

    NV: 201
    NT: 41
    folder: './%sK.txt'
    initP : 200
    finalP : 400
    ratio : 1.2
    output_directory : './results/'
    temperature :
                - 0
                - 1000
                - 2000
                - 3000
                - 4000
    pressure : True
    entropy : True
    internal_energy : True
    enthalpy : True
    gibbs_free_energy : True
    thermal_expansion_coefficient : True
    isothermal_bulk_modulus : True
    gruneisen_parameter : True
    adiabatic_bulk_modulus : True
    volumetric_heat_capacity : True
    isobaric_heat_capacity : True
    

The following parameters must be specified in the configuration file:

.. table:: Table 4: Parameters in the settings.yaml file in YAML syntax.

    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | Parameters                       | Type                  | Description                                                                                     |
    +==================================+=======================+=================================================================================================+
    | NV                               | Integer               | Number of volumes (same as pressures) on the grid                                               |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | NT                               | Integer               | Number of temperatures on the grid                                                              |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | folder                           | String                | | The folder or data file name containing the placeholder for the temperatures,                 |
    |                                  |                       | | i.e., ‘/%sK/input.txt’, ‘./%sK.txt’                                                           |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | initP                            | Integer/Float         | The desired initial pressure in the unit of GPa for calculations                                |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | finalP                           | Integer/Float         | The desired final pressure in the unit of GPa for calculations                                  |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | temperature                      | List of Integer/Float | | The list of temperatures of the inputs in the unit of Kelvin which are put into               |
    |                                  |                       | | the placeholder specified in the folder parameter.                                            |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | output_directory                 | String                | The path to save the output data. The default path is ‘./results/’.                             |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | pressure                         | Boolean type value    | Determine whether to output pressure vs. temperature and volume results                         |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | entropy                          | Boolean type value    | Determine whether to output entropy vs. temperature and volume results.                         |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | internal_energy                  | Boolean type value    | Determine whether to output internal energy vs. temperature and pressure results                |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | enthalpy                         | Boolean type value    | Determine whether to output enthalpy vs. temperature and pressure results.                      |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | gibbs_free_energy                | Boolean type value    | Determine whether to output Gibbs free energy vs. temperature and pressure results.             |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | thermal_expansion_coefficient    | Boolean type value    | Determine whether to output thermal expansion coefficient vs. temperature and pressure results. |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | isothermal_bulk_modulus          | Boolean type value    | Determine whether to output isothermal bulk modulus vs. temperature and pressure results.       |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | gruneisen_parameter              | Boolean type value    | Determine whether to output the Grüneisen parameter vs. temperature and pressure results.       |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | adiabatic_bulk_modulus           | Boolean type value    | Determine whether to output adiabatic bulk modulus vs. temperature and pressure results.        |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | volumetric_heat_capacity         | Boolean type value    | Determine whether to output volumetric heat capacity vs. temperatureand pressure results.       |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+
    | isobaric_heat_capacity           | Boolean type value    | Determine whether to output isobaric heat capacity vs. temperature and pressure results.        |
    +----------------------------------+-----------------------+-------------------------------------------------------------------------------------------------+


QHA Input Data File
-------------------

The QHA input data file is a text file that contains data used by the program to perform Quasi Harmonic Approximation (QHA) calculations. 

We use the same file structure used in the Python package ``qha`` to store phonon calculation information to optimize compatibility, see `QHA’s input data <https://mineralscloud.github.io/qha/tutorials/run.html#how-to-make-input-data>`_.



How to Build Input Files
------------------------

To build the input files for this program, follow these steps:

1. Create a new YAML file for the configuration file.
2. Open the configuration file and specify the required parameters and settings.
3. Save the configuration file.
4. Create a new text file for the QHA input data file.
5. Open the QHA input data file and specify the required data.
6. Save the QHA input data file.

Note: The format of the input files must match the examples provided above.
