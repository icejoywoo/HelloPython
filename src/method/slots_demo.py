#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 13-12-25

# refer: http://stackoverflow.com/questions/1816483/python-how-does-inheritance-of-slots-in-subclasses-actually-work

__author__ = 'icejoywoo'
import sys


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
        __slots__ = 'a', 'b', 'c'

    w = WithSlots()
    n.a = n.b = n.c = 23
    w.a = w.b = w.c = 23
    print sys.getsizeof(n)
    print sys.getsizeof(w)

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
    print "size with slots: %d" % sum([sys.getsizeof(p) for p in persons_])
