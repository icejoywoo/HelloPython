#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-8

import time


class case(object):
    counter = 0

    def __init__(self, name=None):
        self.name = name if name else "test %d" % self.__class__.counter
        self.__class__.counter += 1

    def __enter__(self):
        self.start = time.time()
        print "=" * 10, self.name, "=" * 10

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "=" * (20 + len(self.name) + 2)
        print "elapsed: %fs" % (time.time() - self.start)


with case():
    class t(object):
        def __init__(self, start=0, end=None):
            self.index = start
            self.end = end

        def __iter__(self):
            while True:
                if not self.end or (self.end and self.index < self.end):
                    yield self.index, self.index + 1
                else:
                    return
                self.index += 2
            else:
                return

    print (i for i in t(10))
    print [i for i in t(10, 20)]

    i = iter(t(0, 4))
    print i.next()
    print i.next()

with case():
    class MyFib(object):
        def __init__(self):
            self.i = 2

        def __iter__(self):
            return self

        def next(self):
            if self.i > 1000:
                raise StopIteration
            self.i = self.i * self.i
            return self.i

    print [x for x in MyFib()]

    ''' Fibonacci '''

    class fib(object):
        def __init__(self, count=10):
            self.i = 1
            self.j = 1
            self.count = count

        def __iter__(self):
            for _ in xrange(self.count):
                yield self.i
                self.i, self.j = self.j, self.i + self.j

    print (i for i in fib(10))
    print [i for i in fib(10)]

with case():
    # similar with itertools.count
    def gen(start=0):
        index = start
        while True:
            yield index
            index += 1

    def isPrime(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def prime(end=None):
        for i in gen(1):
            if end and i > end:
                return
            if isPrime(i):
                yield i

    for i in prime(100):
        print i
        # time.sleep(0.1)
