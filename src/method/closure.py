#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 13-12-24

__author__ = 'wujiabin'


# closure
def context():
    data = {}

    def _context(key, value=None):
        if value:
            data[key] = value
            return data
        else:
            return data.get(key, None), data

    return _context


c = context()
print c("key")
print c("key", "value")
print c("key")


# method default argument
def d(key, value=None, data={}):
    if value:
        data[key] = value
        return data
    else:
        return data.get(key, None), data


print d("key")
print d("key", "value")
print d("key")


# class implementation
class e(object):
    def __init__(self):
        self.data = {}

    def __call__(self, key, value=None):
        if value:
            self.data[key] = value
            return self.data
        else:
            return self.data.get(key, None), self.data


f = e()
print f("key")
print f("key", "value")
print f("key")