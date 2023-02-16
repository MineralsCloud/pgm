import click
from pathlib import Path

with open(Path(__file__).parent / "../version.py") as fp: exec(fp.read())

@click.group()
@click.version_option(version=__version__, package_name="pgm")
def main():
    pass

from pgm.cli.main import main as _run
main.add_command(_run, "run")

# from cli.cli.help import main as _help
# main.add_command(_help, "help")
#
# from cli.cli.version import main as _version
# main.add_command(_version, "version")
#
# from cij.cli.fill import main as _fill
# main.add_command(_fill, "fill")
#
# from cij.cli.extract import main as _extract
# main.add_command(_extract, "extract")
#
# from cij.cli.geotherm import main as _geotherm
# main.add_command(_geotherm, "extract-geotherm")
#
# from cij.cli.modes import main as _modes
# main.add_command(_modes, "modes")
#
# from cij.cli.plot import main as _plot
# main.add_command(_plot, "plot")

main.context_settings["max_content_width"] = 9999

if __name__ == "__main__":
    main()