#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-26

__author__ = 'wujiabin'

import traceback


class Coin(object):
    def __init__(self, _name, _value):
        self._name = _name
        self._value = _value

    @property
    def name(self):
        '''
        property: http://docs.python.org/2/library/functions.html#property
        '''
        return self._name

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        if self.name == other.name and self.value == other.value:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.value))

    def __str__(self):
        return '%s[Name: %s, Value: %s]' % (self.__class__.__name__, self.name, self.value)

    def __repr__(self):
        return self.__str__()


class Wallet(object):
    def __init__(self):
        self.coins = []
        (filename, line_number, function_name, text) = traceback.extract_stack()[-2]
        self._name = text[:text.find('=')].strip()

    def add(self, _c):
        self.coins.append(_c)

    def __str__(self):
        result = ["wallet [%s]:" % self._name]
        for i in set(self.coins):
            result.append("\t%s (%d cents): %d" % (i.name, i.value, len([j for j in self.coins if j == i])))
        return "\n".join(result)

    def __iter__(self):
        for i in self.coins:
            yield i

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    a = Coin('dollar', 100)
    b = Coin('dime', 10)
    c = Coin('dollar', 100)

    myWallet = Wallet()
    myWallet.add(a)
    myWallet.add(b)
    myWallet.add(c)

    for coin in myWallet:
        print coin
    print

    print myWallet
