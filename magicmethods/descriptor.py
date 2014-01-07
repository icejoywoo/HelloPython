#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-8

__author__ = 'icejoywoo'


class Meter(object):
    '''Descriptor for a meter.'''

    def __init__(self, value=0.0):
        self.value = float(value)

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = float(value)


class Foot(object):
    '''Descriptor for a foot. Depends on meter.'''

    def __get__(self, instance, owner):
        return instance.meter * 3.2808

    def __set__(self, instance, value):
        instance.meter = float(value) / 3.2808


class Distance(object):
    '''Class to represent distance holding two descriptors for feet and
    meters.'''
    meter = Meter()
    foot = Foot()


if __name__ == "__main__":
    d = Distance()
    d.meter = 1
    d.foot = 3
    print d.foot
    print d.meter
