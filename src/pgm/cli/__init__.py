#!/usr/bin/env python3
"""
.. module cli
   :platform: Unix, Windows, Mac, Linux
.. moduleauthor:: Chenxing Luo <chenxing.luo@columbia.edu>
.. moduleauthor:: Tian Qin <qinxx197@umn.edu>
"""

from .parser import ArgumentParser
from .runner import PgmRunner


def main():
    parser = ArgumentParser()

    runner = PgmRunner()
    parser.register_handler('run', runner)

    parser.load_plugins()

    namespace = parser.parse_args()
    parser.invoke_handler(namespace)


if __name__ == '__main__':
    main()