#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from pkg_resources import require, VersionConflict
from setuptools import setup, find_packages

with open(Path(__file__).parent / "src" / "pgm" / "version.py") as fp: exec(fp.read())
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

try:
    require('setuptools>=38.3')
except VersionConflict:
    print("Error: version of setuptools is too old (<38.3)!")
    sys.exit(1)

setup(
    name='pgm',
    version=__version__,
    description='Free energy calculation using phonon gas model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hongjin Wang',
    author_email='hw2626@columbia.edu',
    url='https://github.com/MineralsCloud/pgm/',
    packages=find_packages('src'),
    package_dir={'':'src'},
    install_requires=[
        "cycler",
        "lazy-property",
        "numba",
        "numpy",
        "pandas",
        "pyparsing",
        "python-dateutil",
        "pytz",
        "PyYAML",
        "scientific-string",
        "scipy",
        "six",
        "text-stream",
    ],
    entry_points={
        'console_scripts': [
            'pgm=pgm.cli.cli:main',
            'pgm-run=pgm.cli.main:main',
        ],
    }
)

if __name__ == "__main__":
    pass
