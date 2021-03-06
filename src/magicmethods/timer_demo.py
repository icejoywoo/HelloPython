#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-8

import time


class Timer(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exception_type, exception_val, trace):
        self.elapsed = time.time() - self.start
        print "elapsed:", self.elapsed


if __name__ == "__main__":
    with Timer():
        [i for i in xrange(10000000)]

try:
    dict_file = open(__file__)
    for line in dict_file:
        print line,  # do something
finally:
    dict_file.close()

with open(__file__) as dict_file, open(__file__) as d2:
    for line in dict_file:
        print line,  # do something
