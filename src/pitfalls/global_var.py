#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 13-12-25

# details to refer:
#   http://docs.python.org/2/faq/programming.html#why-am-i-getting-an-unboundlocalerror-when-the-variable-has-a-value

__author__ = 'wujiabin'

x = 10


def foo():
    global x  # without this declaration, raise a UnboundLocalError: local variable 'x' referenced before assignment
    print(x)
    x += 1


foo()

x = 10


def foo():
    # can work without `global` declaration
    print(x)


foo()
