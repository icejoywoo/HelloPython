__author__ = 'wujiabin'

from collections import OrderedDict

ordered_dict = OrderedDict([('first', 1), ('second', 2), ('third', 3)])
ordered_dict2 = OrderedDict([('third', 3), ('first', 1), ('second', 2)])
d = dict([('first', 1), ('second', 2), ('third', 3)])

assert d == ordered_dict
assert ordered_dict != ordered_dict2

print "Methods:", dir(ordered_dict)

for k, v in ordered_dict.viewitems():
    print k, v
#################################################
a = "a 1\nb 2\nc 3"
d = dict([i.split(' ') for i in a.split('\n')])
print d
#################################################
a = "a b c\n1 2 3"
d = dict(zip(*[i.split(' ') for i in a.split('\n')]))
print d