import matplotlib.pyplot as plt
import numpy

from pgm.data import read_data


class Plot:
    def __init__(self, volume, pressure, temperature, filename, outname):
        self.volume = volume
        self.pressure = pressure
        self.temperature = temperature
        self.filename = filename
        self.outname = outname
        self.check_if_paras_valid()
        self.quantity_name_with_unit = self.get_quantity_name_with_unit()
        self.df = read_data(filename)

    def check_if_paras_valid(self):
        """
        Check whether the parameters are valid
        Rules: Only one quantity(temperature, pressure, or volume) can be chosen.
        If more than one are chosen, raise an error
        """
        if (
            self.volume is not None
            and self.pressure is not None
            and self.temperature is not None
        ):
            raise ValueError("Volume, pressure and temperature are all chosen")
        elif self.volume is not None and self.pressure is not None:
            raise ValueError("Both volume and pressure are chosen")
        elif self.pressure is not None and self.temperature is not None:
            raise ValueError("Both temperature and pressure are chosen")
        elif self.volume is not None and self.temperature is not None:
            raise ValueError("Both temperature and volume are chosen")

    def get_quantity_name_with_unit(self):
        mapping = {
            "alpha": "Thermal expansion coefficient",
            "bs": "Adiabatic bulk modulus (GPa)",
            "cp": r"Isobaric heat capacity ($J\cdot mol/K$)",
            "cv": r"Volumetric heat capacity ($J\cdot mol/K$)",
            "ftv": "Helmholtz free energy (eV)",
            "gamma": "Grüneisen parameter",
            "gtp": "Gibbs Free Energy (eV)",
            "htp": "Enthalpy (eV)",
            "ptv": "Pressure (GPa)",
            "stv": "Entropy (eV/K)",
            "utp": "Internal Energy (eV)",
        }
        for key, value in mapping.items():
            if key in self.filename:
                return value

    def plot(self):
        """
        Plot the target file using parameters provided
        """
        if self.pressure is not None:  # Plot T, P
            plot_temperature = self.df.index.values
            for p in self.pressure:
                line = self.df.loc[:, p].values
                plt.plot(plot_temperature[4:-4], line[4:-4], label=f"{p} GPa")

            plt.xlabel("Temperature (K)")
            plt.ylabel(self.quantity_name_with_unit)
            plt.title(f"{self.filename} at {self.pressure} GPa")
            plt.legend()
            plt.savefig(f"{self.outname}.png", dpi=300)
        elif self.volume is not None:  # Plot T,V
            plot_temperature = self.df.index.values
            """
            The problem with choose V is that the volume might not be exact. 
            So needs to find the closest value to target in volumes
            """
            all_volumes = self.df.columns.values
            for v in self.volume:
                closest_column_index = numpy.abs(all_volumes - v).argmin()
                closest_column_value = self.df.columns[closest_column_index]
                line = self.df[closest_column_value].values
                plt.plot(
                    plot_temperature[4:-4],
                    line[4:-4],
                    label=f"{closest_column_value} $Ang^3$",
                )

            plt.xlabel("Temperature (K)")
            plt.ylabel(self.quantity_name_with_unit)
            plt.title(f"{self.filename} at {self.volume} $Ang^3$")
            plt.legend()
            plt.savefig(f"{self.outname}.png", dpi=300)
        elif self.temperature is not None and "tp" in self.filename:  # Plot T,P
            all_pressure = self.df.columns.values
            for t in self.temperature:
                line = self.df.loc[t].values
                plt.plot(all_pressure[4:-4], line[4:-4], label=f"{t} $K$")
            plt.xlabel("Pressure (GPa)")
            plt.ylabel(self.quantity_name_with_unit)
            plt.title(f"{self.filename} at {self.temperature} K")
            plt.legend()
            plt.savefig(f"{self.outname}.png", dpi=300)
        elif self.temperature is not None and "tv" in self.filename:  # Plot T,V
            all_volumes = self.df.columns.values
            for t in self.temperature:
                line = self.df.loc[t].values
                plt.plot(all_volumes[4:-4], line[4:-4], label=f"{t} $K$")
            plt.xlabel(r"Volume ($Ang^3$)")
            plt.ylabel(self.quantity_name_with_unit)
            plt.title(f"{self.filename} at {self.temperature} K")
            plt.legend()
            plt.savefig(f"{self.outname}.png", dpi=300)

        # Close everything
        plt.close("all")
