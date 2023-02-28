Input Files
===========

This program requires several input files to run. The following input files are required:

Configuration File ``settings.yaml``
-----------------------------------

The configuration file is a ``YAML`` file that contains various parameters and settings used by the program. The format of the configuration file is as follows:

.. code-block:: text

    # This is a comment

    # Parameters
    parameter1 = value1
    parameter2 = value2
    ...

    # Settings
    setting1 = value1
    setting2 = value2
    ...

The following parameters must be specified in the configuration file:

- `parameter1`: A description of parameter1.
- `parameter2`: A description of parameter2.

The following settings may be specified in the configuration file:

- `setting1`: A description of setting1.
- `setting2`: A description of setting2.

QHA Input Data File
-------------------

The QHA input data file is a text file that contains data used by the program to perform Quasi Harmonic Approximation (QHA) calculations. The format of the QHA input data file is as follows:

.. code-block:: text

    # This is a comment

    # Data
    data1 data2 data3 ...
    data4 data5 data6 ...
    ...

The following data must be specified in the QHA input data file:

- `data1`: A description of data1.
- `data2`: A description of data2.
- `data3`: A description of data3.
- `data4`: A description of data4.
- `data5`: A description of data5.
- `data6`: A description of data6.
- ...

How to Build Input Files
------------------------

To build the input files for this program, follow these steps:

1. Create a new text file for the configuration file.
2. Open the configuration file and specify the required parameters and settings.
3. Save the configuration file.
4. Create a new text file for the QHA input data file.
5. Open the QHA input data file and specify the required data.
6. Save the QHA input data file.

Note: The format of the input files must match the examples provided above.
