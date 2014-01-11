#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-11

__author__ = 'icejoywoo'

from mock import Mock
from mock import patch


@patch('test_module.ClassName1')
@patch('test_module.ClassName2')
def test_method(self, MockClass2, MockClass1):
    test_module.ClassName1()
    test_module.ClassName2()

    self.assertTrue(MockClass1.called, "ClassName1 not patched")
    self.assertTrue(MockClass2.called, "ClassName2 not patched")


class Test():
    pass


real = Test()
real.method = Mock()
real.method.return_value = 3
print real.method(3, 4, 5, key='value')

test_method()
