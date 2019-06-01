#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pgm.skeleton import fib

__author__ = "underhill1886"
__copyright__ = "underhill1886"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
