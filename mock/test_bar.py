#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-26

__author__ = 'wujiabin'

from bar import Coin, Wallet
from mock import *


coins = []


class TestBar():
    def setUp(self):
        print "setup"

    def tearDown(self):
        print "teardown"

    def test_bar1(self):
        a = Coin('dollar', 100)
        a.__str__ = Mock(return_value="__str__ magic method")
        assert str(a) == "__str__ magic method"

    @patch("bar.Wallet.add", MagicMock(side_effect=lambda x: coins.append(x)))
    @patch("bar.Wallet.__str__", MagicMock(side_effect=lambda: str(coins)))
    @patch("bar.Coin.__str__", MagicMock(side_effect=lambda: "Coin"))
    def test_bar2(self):
        '''
        mock a method demo
        @return:
        '''
        a = Coin('dollar', 100)
        b = Coin('dime', 10)
        c = Coin('dollar', 100)
        assert str(a) == "Coin"

        wallet = Wallet()
        wallet.add(a)
        wallet.add(b)
        wallet.add(c)

        assert str(coins) == '[Coin, Coin, Coin]'
        assert str(wallet) == '[Coin, Coin, Coin]'
