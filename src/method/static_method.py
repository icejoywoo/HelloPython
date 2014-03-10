#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-2-28

__author__ = 'wujiabin'


class FancyDict(dict):

    @classmethod
    def fromkeys(cls, keys, value=None):
        data = {(key, value) for key in keys}  # set comprehension
        print data
        return cls(data)


class MyDict(FancyDict):
    pass


if __name__ == "__main__":
    print(MyDict.fromkeys([1, 2, 3, 1]))
