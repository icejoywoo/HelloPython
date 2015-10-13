#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 13-12-25

# refer: http://stackoverflow.com/questions/1816483/python-how-does-inheritance-of-slots-in-subclasses-actually-work

import sys

from guppy import hpy


class Person_(object):
    __slots__ = ("name", "age", "gender")

    def __init__(self):
        pass


class Person(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    class NoSlots(object):
        pass

    n = NoSlots()

    class WithSlots(object):
        __slots__ = 'a', 'b', 'c', 'd', 'e', 'f'

    w = WithSlots()
    n.a, n.b, n.c, n.d, n.e, n.f = 1, 2, 23, 4, 5, 6
    w.a, w.b, w.c, w.d, w.e, w.f = 1, 2, 23, 4, 5, 6
    print sys.getsizeof(n), sys.getsizeof(n.__dict__)
    print sys.getsizeof(w)

    import collections

    s = collections.namedtuple("s", "a,b,c")
    s.a, s.b, s.c = 1, 2, 23
    l = []
    l.append(1)
    l.append(2)
    l.append(23)
    print sys.getsizeof(s)
    print sys.getsizeof(l)

    persons = []
    for i in xrange(100000):
        p = Person()
        p.name = "name_%d" % i
        p.age = i
        p.gender = "female"
        persons.append(p)

    persons_ = []
    for i in xrange(100000):
        p = Person_()
        p.name = "name_%d" % i
        p.age = i
        p.gender = "female"
        persons_.append(p)

    print "size without slots: %d" % sum([sys.getsizeof(p) for p in persons])
    print "size of the __dict__ without slots: %d" % sum([sys.getsizeof(p.__dict__) for p in persons])
    print "size of the __weakref__ without slots: %d" % sum([sys.getsizeof(p.__weakref__) for p in persons])
    print "size with slots: %d" % sum([sys.getsizeof(p) for p in persons_])

    h = hpy()
    print h.heap()
