#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-7

import os


# __new__ 在__init__之前调用, 并且创建对象
class Singleton(object):
    def __new__(cls, *args, **kwds):
        # 使用__it__保存单例对象
        print "args:", args, kwds

        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = super(Singleton, cls).__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class MySingleton(Singleton):
    def init(self, *args, **kwds):
        self.a = kwds["a"]
        print "init"

    def __init__(self, *args, **kwds):
        self.b = 1
        print "__init__"


class FileObject(object):
    """ Wrapper for file objects to make sure the file gets closed on deletion.
    """

    def __init__(self, filepath=os.path.dirname(__file__), filename=os.path.basename(__file__)):
        print self.__class__.__name__, "__init__"
        # open a file filename in filepath in read and write mode
        self.file = open(os.path.join(filepath, filename), 'r+')

    def __del__(self):
        print self.__class__.__name__, "__del__"
        self.file.close()
        del self.file


if __name__ == "__main__":
    x = MySingleton(a=1)
    y = MySingleton()
    assert x is y
    print x.a, y.a
    print x.b, y.b

    f = FileObject()
    import time

    time.sleep(1)
    del f
    time.sleep(1)
