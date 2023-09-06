Command Line Tools
==================

This document provides information about the command line tools included with the ``pgm`` package.
The command line tools allow you to perform certain tasks using the command line interface (CLI).

Usage
-----

To use the command line tools, open a command prompt or terminal and navigate to the directory where the package is installed.
Then, run the command with the desired options and arguments.


Available Commands
------------------

The following command line tools are available in the ``pgm`` package:

``run`` Command
~~~~~~~~~~~~~~~~~

The ``run`` command is the main command to initiate the calculation process. Upon completion, the thermodynamic property outputs will be saved to the path designated by the user in the settings file.

.. code-block:: bash

    pgm run your_settings.yaml

This will run the ``pgm`` tool with the ``your_settings.yaml`` settings file of user specified configurations.


``plot`` Command
~~~~~~~~~~~~~~~~~

The ``plot`` command allows users to generate plots based on the output of the ``pgm`` code.

Generating a Plot
-----------------

To generate a plot, use the following command:

.. code-block:: bash

   pgm plot [options] FILENAME

   FILENAME: The original output of the pgm code.

Options
~~~~~~~

The following options are available for generating plots:

- ``-v, --volume``: Specify this option to plot volumes.
- ``-p, --pressure``: Specify this option to plot pressures.
- ``-t, --temperature``: Specify this option to plot temperatures.

Output Name
~~~~~~~~~~~

The user must specify the output name of the generated figure using the ``-o, --outname`` option.

Example Usage
~~~~~~~~~~~~~

To generate a plot for volumes from the output file ``output.txt`` and save it as ``volume_plot.png``, use the following command, and replace the OUTPUT with your desired output file:

.. code-block:: bash

   pgm plot -v -o volume_plot.png OUTPUT

To generate a plot for pressures from the output file ``output.txt`` and save it as ``pressure_plot.png``, use the following command, and replace the OUTPUT with your desired output file:

.. code-block:: bash

   pgm plot -p -o pressure_plot.png OUTPUT

To generate a plot for temperatures from the output file ``output.txt`` and save it as ``temperature_plot.png``, use the following command, and replace the OUTPUT with your desired output file:

.. code-block:: bash

   pgm plot -t -o temperature_plot.png OUTPUT

``pgm`` will then process the data in the specified ``FILENAME`` and create the corresponding plot based on the chosen option.

Note
~~~~

Ensure that you have the necessary data in the ``FILENAME`` to generate the plots successfully.

``FILENAME`` should be in the correct format that the program can understand to plot the desired data.

Make sure to specify a unique and meaningful name for the output figure using the ``-o, --outname`` option.

``pgm`` will save the generated plot in the current working directory.


Conclusion
----------

Congratulations, you now know how to use the command line tools included with the ```pgm`` package!
If you encounter any issues using the command line tools, please consult the documentation or contact the developers for assistance.
