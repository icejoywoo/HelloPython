#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-14

"""
http://stackoverflow.com/questions/6704151/python-equivalent-of-rubys-method-missing
http://stackoverflow.com/questions/6954116/rubys-method-missing-in-python
"""

import unittest
from functools import partial


class MyRubylikeThing(object):
    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            print "A missing method was called."
            print "The object was %r, the method was %r. " % (self, name)
            print "It was called with %r and %r as arguments" % (args, kwargs)

        return _missing


r = MyRubylikeThing()
r.hello("there", "world", also="bye")


class MethodMissing:
    def method_missing(self, name, *args, **kwargs):
        '''please implement'''
        raise NotImplementedError('please implement a "method_missing" method')

    def __getattr__(self, name):
        return partial(self.method_missing, name)


class Wrapper(object, MethodMissing):
    def __init__(self, item):
        self.item = item

    def method_missing(self, name, *args, **kwargs):
        if name in dir(self.item):
            method = getattr(self.item, name)
            if callable(method):
                return method(*args, **kwargs)
            else:
                raise AttributeError(' %s has not method named "%s" ' % (self.item, name))


class Item(object):
    def __init__(self, name):
        self.name = name

    def test(self, string):
        return string + ' was passed on'


class EmptyWrapper(object, MethodMissing):
    """ not implementing a missing_method
    """
    pass


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.item = Item('test')
        self.wrapper = Wrapper(self.item)
        self.empty_wrapper = EmptyWrapper()

    def test_proxy_method_call(self):
        string = self.wrapper.test('message')
        self.assertEqual(string, 'message was passed on')

    def test_normal_attribute_not_proxied(self, ):
        with self.assertRaises(AttributeError):
            print "=====", self.wrapper.name
            print self.wrapper.name()

    def test_empty_wrapper_raises_error(self, ):
        with self.assertRaises(NotImplementedError):
            self.empty_wrapper.test('message')


if __name__ == '__main__':
    unittest.main()
