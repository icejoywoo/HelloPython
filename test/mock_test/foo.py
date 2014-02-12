#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-18

__author__ = 'icejoywoo'

import sys

this_module = sys.modules[__name__]

this_module.__str__ = lambda: "Test"
print str(this_module)


# 待测类
class ProductionClass():
    def __init__(self):
        pass

    def method(self):
        pass


# 待测方法
def emit_line(key, value):
    pass


def function(a, b, c):
    pass