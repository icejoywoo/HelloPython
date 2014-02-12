#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-8

__author__ = 'icejoywoo'


# refer method/closure.py
class context(object):
    def __init__(self):
        self.data = {}

    def __call__(self, key=None, value=None):
        if key:
            if value:
                self.data[key] = value
            else:
                return self.data.get(key, None)


if __name__ == "__main__":
    c = context()
    print c("test")
    c("test", "value")
    print c("test")
