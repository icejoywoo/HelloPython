#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-19

__author__ = 'icejoywoo'


def get_from_context(a=None, history=[]):
    if not a:
        return history
    if a not in history:
        history.append(a)
    return a


if __name__ == "__main__":
    get_from_context("a")
    print get_from_context()
    get_from_context("b")
    print get_from_context()
    get_from_context("b")
    print get_from_context()
