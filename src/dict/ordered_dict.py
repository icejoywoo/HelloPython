#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 13-12-24

from collections import OrderedDict

ordered_dict = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
ordered_dict2 = OrderedDict([('third', 3), ('first', 1), ('second', 2)])
d = dict([('first', 1), ('third', 3), ('second', 2)])

assert d == ordered_dict
assert ordered_dict != ordered_dict2

print "Methods:", dir(ordered_dict)

for k, v in ordered_dict.viewitems():
    print k, v
