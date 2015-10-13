#!/bin/env python
# encoding: utf-8
# @author: icejoywoo
# @date: 15-1-3


def fp_hd(l):
    return l[0]


def fp_tl(l):
    return l[1:]


def fp_map(f, l):
    """ fp-like map
    :param f:
    :param l:
    :return:
    """
    if l:
        return [f(fp_hd(l))] + fp_map(f, fp_tl(l))
    else:
        return []


print fp_map(lambda x: x + 1, [1, 2, 3])


def fp_fold(f, acc, l):
    if l:
        return f(acc, fp_hd(l)) + fp_fold(f, acc, fp_tl(l))
    else:
        return acc

print fp_fold(lambda acc, x: acc + x, 0, [1, 2, 3])


def fp_foldr(f, acc, l):
    if l:
        return f(acc, fp_hd(l)) + fp_fold(f, acc, fp_tl(l))
    else:
        return acc


def fp_filter(f, l):
    if l:
        head = fp_hd(l)
        if f(head):
            return [head] + fp_filter(f, fp_tl(l))
        else:
            return fp_filter(f, fp_tl(l))
    else:
        return []

print fp_filter(lambda x: x > 0, [-1, 3, 0, -4, 5, 9])


def fp_currying(f, *args, **kwargs):
    saved_args = list(args)
    saved_kwargs = kwargs

    def _f(*_args, **_kwargs):
        saved_kwargs.update(_kwargs)
        return f(*tuple(saved_args + list(_args)), **saved_kwargs)

    return _f


def t(a, b, c, d=1, e=2):
    print a, b, c, d, e
    return a + b + c + d + e

fp_curried_t = fp_currying(t, 1, 2, d=3)

print fp_curried_t(4, e=3)


def fp_compose(f, g):

    def _wrapper(*args, **kwargs):
        return f(g(*args, **kwargs))

    return _wrapper


a = lambda x: x + 1

b = fp_compose(a, a)

print b(10)


def fp_forloop(f, l):
    if l:
        f(fp_hd(l))
        fp_forloop(f, fp_tl(l))
    else:
        pass


def echo(x):
    print x,

fp_forloop(echo, [1, 2, 3, 4, 5])
