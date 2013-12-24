#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 13-12-24

__author__ = 'wujiabin'

# parse to a dict
# dict([(k1, v1), (k2, v2)...])
#################################################
a = "a 1\nb 2\nc 3"
d = dict([i.split(' ') for i in a.split('\n')])
print d

# zip
#################################################
a = "a b c\n1 2 3"
d = dict(zip(*[i.split(' ') for i in a.split('\n')]))
print d

# D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
[d.setdefault(chr(65 + i % 26), i) for i in xrange(100)]
print d

# D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
print [d.get(i, "default") for i in xrange(10)]
