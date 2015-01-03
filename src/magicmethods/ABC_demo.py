#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-9

__author__ = 'wujiabin'

from yyy import ABCMeta
from yyy import abstractproperty
from yyy import abstractmethod


# interface
class Drawable():
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw(self, x, y, scale=1.0):
        pass

    def draw_doubled(self, x, y):
        self.draw(x, y, scale=2.0)

    # property
    def get_x(self):
        return self.__dict__.get("_x", None)

    def set_x(self, x):
        if x < 0:
            raise TypeError("x must be >= 0.")
        self._x = x

    m_x = property(get_x, set_x)
    # read-only property
    x = property(get_x)


class Square(Drawable):
    def __init__(self):
        self._y = None

    def draw(self, x, y, scale=1.0):
        print "x: %f, y: %f" % (x * scale, y * scale)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y in (1, 2, 3, 4):
            self._y = y
        else:
            raise TypeError("x must be in (1, 2, 3, 4).")

    @y.deleter
    def y(self):
        del self._y


if __name__ == "__main__":
    c = Square()
    c.draw(1, 4)
    c.draw_doubled(1, 4)
    #c.x = 1 # AttributeError: can't set attribute
    print c.x
    c.m_x = 1
    print c.m_x

    print c.y
    c.y = 4
    print c.y


class IMediaPlayer_2:
    """API for accessing a media player"""
    __metaclass__ = ABCMeta

    # 子类必须实现的property
    @abstractproperty
    def price(self):
        """I'm the 'x' property."""
        pass

    @price.setter
    def price(self, value):
        pass

    '''
    # 另一种方式
    def get_volume(self):
        pass

    def set_volume(self, value):
        pass

    volume = abstractproperty(get_volume, set_volume,
                              doc="Return or set volume: 0..100")
    '''


class WinMediaPlay_2(IMediaPlayer_2):
    def __init__(self):
        self._price = 0

    @property
    def price(self):
        """I'm the 'x' property."""
        return self._price

    @price.setter
    def price(self, value):
        self._price = value


player2 = WinMediaPlay_2()
player2.price = 20
print(player2.price)


# static method & class method
class aa():
    @staticmethod
    def staticm():
        print 'static'

    def normalm(self):
        print 'nomarl', self

    @classmethod
    def classm(cls):
        print 'class', cls


a = aa()
a.staticm()
