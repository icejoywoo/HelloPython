#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-2-13

__author__ = 'wujiabin'
# http://blog.jobbole.com/23773/

import time


class Timer(object):
    def __init__(self):
        pass

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exception_type, exception_val, trace):
        print "elapsed:", time.time() - self.start


# case 1
def main():
    for _ in xrange(10 ** 8):
        pass


with Timer():
    main()

# case 2
with Timer():
    for _ in xrange(10 ** 8):
        pass
