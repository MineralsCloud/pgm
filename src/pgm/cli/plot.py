import sys
from glob import glob
import click
import numpy
from pgm.plot.plotter import Plot


def process_input(ctx, param, value):
    if value is None:
        return value  # This is needed if volume or pressure is not provided.
    try:
        # If it's a single value it will be converted to an array with one element.
        # If it's a string of comma-separated floats, it will be converted to an array of those floats.
        return numpy.array([float(val) for val in value.split(',')])
    except ValueError:
        return numpy.array([float(value)])


@click.command("plot")
@click.option('-v', '--volume', callback=process_input,
              help='Comma seperated volume(s) to be plotted. ')
@click.option('-p', '--pressure', callback=process_input,
              help='Comma seperated pressure(s) to be plotted.')
@click.option('-t', '--temperature', callback=process_input,
              help='Comma seperated temperature(s) to be plotted. ')
@click.argument('filename', type=click.Path(exists=True))
@click.pass_context
def main(volume, pressure, temperature, filename):
    """
    \b
    Plot pgm calculation thermodynamics results.
    Specify either temperature/pressure or temperature/volume to be plotted.
    Choice of T/P or T/V must match the file storing pgm calculation results.
    """
