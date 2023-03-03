Output Files
============

The output file of ``pgm`` is a plain text file, containing a comma-separated value (CSV) table, with the name of the file following the rule of ``<property><grid_type>_<unit>``.

- ``<property>`` 
    the abbreviation of the property in lower case, i.e., ``g`` for Gibbs free energy, as will be explained in details in the table below.
-  ``<grid_type>`` 
    - ``<tp>`` the index of the columns is the list of the pressures, and the index of the rows is the list of the temperatures, specified by the user
    - ``<tv>`` the index of the columns is the list of the volumes, and the index of the rows is the list of the temperatures, specified by the user
- ``<unit>``
    by default, the outputs are using energy unit of eV, temperature unit of K, pressure unit of GPa, volume unit of Å³.

Output parameters
-----------------

.. table:: Table 5: A list of the important output properties as functions of temperature and pressure or volume.

    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Property name                          | Output        | Description                                                    |
    +========================================+===============+================================================================+
    | Free Energy :math:`F`                  | ftv_ev_a3     | | Helmholtz free energy (T, V) result.                         |
    |                                        |               | | Free energy in unit of ev, volumes in ang3                   |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Pressure :math:`P`                     | ptv_gpa_K_a3  | | Pressure (T, V) result.                                      |
    |                                        |               | | Pressure in the unit of GPa, temperature in Kelvin,          |
    |                                        |               | | volumes in ang3.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Entropy :math:`S`                      | stv_ev_K_a3   | | Entropy (T, V) result.                                       |
    |                                        |               | | entropy in unit of ev/k, temperature in Kelvin,              |
    |                                        |               | | volumes in ang3.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Internal energy :math:`U`              | utp_ev_K_gpa  | | Internal energy (T, P) result.                               |
    |                                        |               | | Internal energy in the unit of eV, temperature in Kelvin,    |
    |                                        |               | | pressure in GPa.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Enthalpy :math:`H`                     | htp_ev_T_gpa  | | Enthalpy (T, P) result.                                      |
    |                                        |               | | Enthalpy in the unit of eV, temperature in Kelvin,           |
    |                                        |               | | pressure in GPa.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Gibbs free energy :math:`G`            | gtp_ev_T_gpa  | | Gibbs Free Energy (T, P) result.                             |
    |                                        |               | | Gibbs Free Energy in the unit of eV, temperature in Kelvin,  |
    |                                        |               | | pressure in GPa.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Thermal expansion coefficient :math:`α`| alpha_K_gpa   | | Thermal expansion coefficient (T, P) result.                 |
    |                                        |               | | Thermal expansion coefficient in the unit of 1/K,            |
    |                                        |               | | temperature in Kelvin, pressure in GPa.                      |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Isothermal bulk modulus :math:`B_T`    | bt_gpa_K_gpa  | | Isothermal bulk modulus (T, P) result.                       |
    |                                        |               | | Isothermal bulk modulus in the unit of GPa,                  |
    |                                        |               | | temperature in Kelvin, pressure in GPa.                      |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Grüneisen parameter :math:`γ`          | gamma_K_gpa   | | Grüneisen parameter (T, P) result.                           |
    |                                        |               | | Temperature in the unit of Kelvin,                           |
    |                                        |               | | pressure in GPa.                                             |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Adiabatic bulk modulus :math:`B_S`     | bs_gpa_K_gpa  | | Adiabatic bulk modulus (T, P) result.                        |
    |                                        |               | | Adiabatic bulk modulus in the unit of GPa,                   |
    |                                        |               | | temperature in the unit of Kelvin, pressure in GPa.          |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Volumetric heat capacity :math:`C_V`   | cv_jmol_K_gpa | | Volumetric heat capacity (T, P) result.                      |
    |                                        |               | | Volumetric heat capacity in the unit of J·mol/K,             |
    |                                        |               | | temperature in the unit of Kelvin, pressure in GPa.          |
    +----------------------------------------+---------------+----------------------------------------------------------------+
    | Isobaric heat capacity :math:`C_P`     | cp_jmol_K_gpa | | Isobaric heat capacity (T, P) result.                        |
    |                                        |               | | Isobaric heat capacity in the unit of J·mol/K,               |
    |                                        |               | | temperature in the unit of Kelvin, pressure in GPa.          |
    +----------------------------------------+---------------+----------------------------------------------------------------+