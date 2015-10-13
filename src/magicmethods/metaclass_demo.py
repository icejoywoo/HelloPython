#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 2015/2/3


class SubclassTracker(type):

    def __init__(cls, name, bases, attrs):
        try:
            if TrackedClass not in bases:
                return
        except NameError:
            return
        TrackedClass._registry.append(cls)


class TrackedClass(object):
    __metaclass__ = SubclassTracker
    _registry = []

    def run(self):
        for i in self.__class__._registry:
            i.run()


class ClassOne(TrackedClass):

    @staticmethod
    def run():
        print "I'm class one"

a = TrackedClass()
a.run()
