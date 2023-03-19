from pathlib import Path

import click
from pgm.cli.main import main as _run
from pgm.cli.plot import main as _plot

with open(Path(__file__).parent / "../version.py") as fp:
    exec(fp.read())


@click.group()
@click.version_option(version=__version__, package_name="pgm")
def main():
    pass


main.add_command(_run, "run")

main.add_command(_plot, "plot")

main.context_settings["max_content_width"] = 9999

if __name__ == "__main__":
    main()
