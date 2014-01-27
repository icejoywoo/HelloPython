#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-26

__author__ = 'wujiabin'

from bar import Coin, Wallet
from mock import *
from nose.tools import *

# global
coins = []
# 测试前缀, 不会用
patch.TEST_PREFIX = 'foo'


class TestBar():
    def setUp(self):
        print "setup"

    def tearDown(self):
        print "teardown"

    @with_setup(setUp, tearDown)
    def test_bar1(self):
        a = Coin('dollar', 100)
        # new-style class must use 'Coin' class, old-style class can use 'a' instance
        Coin.__str__ = Mock(return_value="__str__ magic method")
        assert str(a) == "__str__ magic method"

        # side_effect
        Coin.__str__ = Mock(side_effect=["test1", "test2"])
        assert str(a) == "test1"
        assert str(a) == "test2"

    @with_setup(setUp, tearDown)
    @patch("bar.Wallet.add", MagicMock(side_effect=lambda x: coins.append(x)))
    @patch("bar.Wallet.__str__", MagicMock(side_effect=lambda: str(coins)))
    @patch("bar.Coin.__str__", MagicMock(side_effect=lambda: "Coin"))
    def test_bar2(self):
        '''
        test_bar2: mock a method demo
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
        print wallet

    @patch.object(Wallet, '__str__', return_value="test")
    def test_bar3(self, mock_method):
        w = Wallet()
        print w
        # 断言调用参数是否符合预期
        mock_method.assert_called_with()

    def test_bar4(self):
        foo = {}
        with patch.dict(foo, {'newkey': 'newvalue'}):
            assert foo == {'newkey': 'newvalue'}
        assert foo == {}

        mock = Mock()
        mock.__enter__ = Mock(return_value="foo")
        mock.__exit__ = Mock(return_value=False)
        with mock as m:
            assert m == "foo"
        mock.__enter__.assert_called_with()
        mock.__exit__.assert_called_with(None, None, None)

    @raises(Exception)
    def test_bar5(self):
        Wallet.add = Mock(side_effect=Exception("mock exception"))
        w = Wallet()
        w.add(Coin('dollar', 100))

    @nottest
    #@istest
    def foo_bar6(self):
        import os
        os.popen = Mock()
        # mock.return_value is a new Mock, a call chain
        os.popen.return_value.read.return_value.split.return_value = 'mock'
        assert os.popen('date').read().split(':') == 'mock'
