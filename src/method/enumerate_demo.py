#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-12

a = ["a", "b", "c", "d"]

# simple iterate
for i in a:
    print i

# bad
for i in xrange(len(a)):
    print i, a[i]

# iterate with index
for i, el in enumerate(a):
    print i, el

# iterate with index
for i, el in enumerate(a, 1):
    print i, el

print "=" * 40

d = dict(zip(("a", "b", "c", "d"), (1, 2, 3, 4)))
# d = {'a': 1, 'c': 3, 'b': 2, 'd': 4}

for k in d:
    print k

# d.viewkeys()
for k in d.iterkeys():
    print k

print type(d.viewkeys()), type(d.iterkeys())
print d.viewkeys(), d.iterkeys()

# d.viewvalues()
for v in d.itervalues():
    print v

print type(d.viewvalues()), type(d.itervalues())
print d.viewvalues(), d.itervalues()

# d.viewitems()
for k, v in d.iteritems():
    print k, v

print type(d.viewitems()), type(d.itervalues())
print d.viewitems(), d.itervalues()
