#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-8

__author__ = 'icejoywoo'

from functools import partial


def add(a, b):
    print a, b
    return a + b


if __name__ == "__main__":
    f = partial(add, b=3)
    print f(5)
    f = partial(add, 3)
    print f(5)

    basetwo = partial(int, base=2)
    basetwo.__doc__ = 'Convert base 2 string to an int.'
    print basetwo('10010')
    print help(basetwo)
