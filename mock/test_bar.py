#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-26

__author__ = 'wujiabin'

from bar import Coin, Wallet
from mock import *


def setUp():
    print "setup"


def tearDown():
    print "teardown"


def test_bar1():
    a = Coin('dollar', 100)
    a.__str__ = Mock(return_value="__str__ magic method")
    assert str(a) == "__str__ magic method"
