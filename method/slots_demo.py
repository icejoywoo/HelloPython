#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 13-12-25

__author__ = 'icejoywoo'

class Person_(object):
    __slots__ = ("name", "age", "gender")
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class Person(object):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

if __name__ == "__main__":
    persons = []
    for i in xrange(500000):
        persons.append(Person("name_%d"%i, i, "male"))

    persons_ = []
    for i in xrange(500000):
        persons_.append(Person_("name_%d"%i, i, "male"))

    import sys
    print "size without slots: %d" % sys.getsizeof(persons)
    print "size with slots: %d" % sys.getsizeof(persons_)