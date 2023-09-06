Installation
=============

This document provides instructions for installing the pgm package.
pgm Code is a code to calculate thermodynamic properties of matter 
using phonon gas model (PGM) in Python.

The installation process is straightforward and requires only a few steps.

Install Directly from PyPI
--------------------------

You can install the `pgm` package directly from PyPI without having to clone the repository.

.. code-block:: bash

    $ pip install phonon-gas-model

For those who wish to clone the repository and install manually, the following steps will guide you.

Clone the repository
--------------------

To install the ``pgm`` package, first clone the code repository using ``git``:

.. code-block:: bash

    $ git clone https://github.com/MineralsCloud/pgm.git

Change to the code directory
----------------------------

After cloning the code repository, change to the code directory using ``cd``:

.. code-block:: bash

    $ cd pgm

This will change the current working directory to the ``pgm`` directory where the code is located.


Install the requirements
------------------------

After changing to the code directory, install the required Python packages using ``pip``:

.. code-block:: bash

    $ pip install -r requirements.txt

This will read the ``requirements.txt`` file in the current directory (i.e., the ``pgm`` directory) and install all the required packages.

Install the package
-------------------

Finally, install the ``pgm`` package using ``pip``:

.. code-block:: bash

    $ pip install .

This will install the package into your Python environment and make it available for use in your Python code.

Conclusion
----------

Congratulations, you have successfully installed the ``pgm`` Python package!
If you encounter any issues during the installation process, please consult the documentation or contact the developers for assistance.
