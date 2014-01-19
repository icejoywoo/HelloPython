#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-19

__author__ = 'icejoywoo'


def get_from_context(a=None, history=[]):
    if not a:
        return history
    if a not in history:
        history.append(a)
    return history


# l will not be shared by calls
def f(a, l=None):
    if not l:
        l = []
    l.append(a)
    return l


if __name__ == "__main__":
    print get_from_context("a")
    print get_from_context("b")
    print get_from_context("b")
    print get_from_context(history=[])
    print get_from_context()
    print dir(get_from_context), type(get_from_context)
    print get_from_context.func_defaults

    print f("test")
    print f("a")


