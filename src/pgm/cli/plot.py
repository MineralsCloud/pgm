import sys
from glob import glob
import click


@click.command("plot", help="Plot pgm calculation thermodynamics results")
@click.argument("patterns", nargs=-1)
def main():
    pass
