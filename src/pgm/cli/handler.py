#!/usr/bin/env python3
"""
.. module cli.handler
   :platform: Unix, Windows, Mac, Linux
"""

import abc
import argparse


class CommandHandler(abc.ABC):
    @abc.abstractmethod
    def init_parser(self, parser: argparse.ArgumentParser):
        ...

    @abc.abstractmethod
    def run(self, namespace):
        ...