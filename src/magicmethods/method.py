#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-8


# refer method/closure.py
class Context(object):
    def __init__(self):
        self.data = {}

    def __call__(self, key=None, value=None):
        if key:
            if value:
                self.data[key] = value
            else:
                return self.data.get(key, None)


if __name__ == "__main__":
    c = Context()
    print c("test")
    c("test", "value")
    print c("test")
