#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for pgm.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 3.1.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
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
    install_requires=[
        "bigfloat",
        "cycler",
        "kiwisolver",
        "lazy-property",
        "llvmlite",
        "numba",
        "numpy",
        "pandas",
        "pyparsing",
        "python-dateutil",
        "pytz",
        "PyYAML",
        "scientific-string",
        "scipy",
        "seaborn",
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
    setup(use_pyscaffold=True)
