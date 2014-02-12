#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-2-7

__author__ = 'wujiabin'
# 函数式编程: http://coolshell.cn/articles/10822.html


class Pipe(object):
    def __init__(self, func):
        self.func = func

    def __ror__(self, other):
        def generator():
            for obj in other:
                if obj is not None:
                    yield self.func(obj)
        return generator()


@Pipe
def even_filter(num):
    return num if num % 2 == 0 else None


@Pipe
def multiply_by_three(num):
    return num*3


@Pipe
def convert_to_string(num):
    return 'The Number: %s' % num


@Pipe
def echo(item):
    print item


nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
[_ for _ in (nums | even_filter | multiply_by_three | convert_to_string | echo)]
print (nums | even_filter | multiply_by_three | convert_to_string | echo)