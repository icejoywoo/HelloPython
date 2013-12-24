#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 13-12-24

__author__ = 'wujiabin'

def context():
    data = {}
    def _context(key, value = None):
        if value:
            data[key] = value
        else:
            return data.get(key, None)
    return _context

c = context()
print c("key")
print c("key", "value")
print c("key")