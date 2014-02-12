#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-14

__author__ = 'wujiabin'

import os
import time

from src.benchmark.benchmark import Benchmark
from src.benchmark.benchmark import worker


# timer 可以在退出的时候打报告什么的
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.start = 0
        self.elapsed_ms = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_ms = (time.time() - self.start) * 1000
        if self.verbose:
            print 'elapsed time: %f ms' % self.elapsed_ms


@worker
def test_worker(kvargs):
    if kvargs["step"] == 1:
        return 0
    else:
        return -1


@worker
class worker_class(object):
    def __init__(self, kvargs):
        self.kvargs = kvargs

    def __call__(self, *args, **kwargs):
        if self.kvargs["step"] == 1:
            return 0
        else:
            return -1


def closure():
    print "reading file..."
    lines = [l.rstrip() for l in file(os.path.abspath(__file__))]
    print "finished"

    @worker
    def _worker(kvargs):
        if lines[0] == 1:
            return 0
        else:
            return -1

    return _worker


# worker_num = 1 时, 计算性能已经很不错了, 如果io比较多的情况下, 可以增加线程数
config = {
    "worker_num": 1,
    "time": 20,
    "max_qps": 1000000,
    "step": 1,  # step 越小 qps控制得越好
}

# 简单测试
with Timer(True):
    # b = Benchmark(test_worker, **config)
    # b = Benchmark(worker_class, **config)
    b = Benchmark(closure(), **config)
    b.loop()
