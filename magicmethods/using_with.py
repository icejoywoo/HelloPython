#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-8

__author__ = 'icejoywoo'

# http://www.python.org/dev/peps/pep-0343/

class Closer:
    '''A context manager to automatically close an object with a close method
    in a with statement.'''

    def __init__(self, obj):
        self.obj = obj

    def __enter__(self):
        return self.obj # bound to target

    def __exit__(self, exception_type, exception_val, trace):
        try:
            self.obj.close()
        except AttributeError: # obj isn't closable
            print 'Not closable.'
            return True # exception handled successfully


if __name__ == "__main__":
    with Closer(file(__file__)) as f:
        print [line for line in f]
    assert f.closed is True

    with Closer(5) as a:
        print a
