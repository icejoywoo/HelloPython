#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 13-12-25

__author__ = 'icejoywoo'

# define a var using this module
import sys

this_module = sys.modules[__name__]

#this_module.__dict__["a"] = 10
this_module.a = 10
print dir(this_module)

print a

# define a var using locals() or globals()

locals()["aa"] = "locals_aa"
print aa

globals()["bb"] = "global_bb"
print bb
