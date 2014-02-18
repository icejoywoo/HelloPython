#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-2-18

__author__ = 'wujiabin'

import time


def mapper():
    for line in open(__file__):
        # do something with line
        time.sleep(.1)
        yield line

if __name__ == "__main__":
    print mapper()
    for i in mapper():
        print i,
    print list(mapper())  # 将结果转为list
