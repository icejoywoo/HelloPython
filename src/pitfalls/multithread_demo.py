#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-3-24

# from multiprocessing.dummy import Pool
from multiprocessing import Pool
import time


def output(s):
    # time.sleep(1)
    for i in xrange(10000000):
        pass
    return s


def test1(i):
    results = map(output, i)
    return results


def test2(i):
    pool = Pool()
    results = pool.map(output, i)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    i = range(10)

    start = time.time()
    print test1(i)
    end = time.time()
    print end - start

    start = time.time()
    print test2(i)
    end = time.time()
    print end - start
