#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-7


class AccessCounter(object):
    """ A class that contains a value and implements an access counter.
        The counter increments each time the value is changed.
    """

    def __init__(self, val):
        super(AccessCounter, self).__setattr__('counter', 0)
        super(AccessCounter, self).__setattr__('value', val)

    def __setattr__(self, name, value):
        if name == 'value':
            super(AccessCounter, self).__setattr__('counter', self.counter + 1)
            # Make this unconditional.
        # If you want to prevent other attributes to be set, raise AttributeError(name)
        super(AccessCounter, self).__setattr__(name, value)

    def __delattr__(self, name):
        if name == 'value':
            super(AccessCounter, self).__setattr__('counter', self.counter + 1)
        super(AccessCounter, self).__delattr__(name)


if __name__ == "__main__":
    a = AccessCounter(3)
    a.value = 1
    print a.counter
    del a.value
    print a.counter
