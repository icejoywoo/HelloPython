#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-11

__author__ = 'icejoywoo'

# nosetests -v -s

import foo
import mock

# https://nose.readthedocs.org/en/latest/testing_tools.html
from nose.tools import *
import time


def test_production_class_method():
    with mock.patch.object(foo.ProductionClass, 'method', return_value=None) as mock_method:
        thing = foo.ProductionClass()
        thing.method(1, 2, 3)
        thing.method.assert_called_once_with(1, 2, 3)

    mock_method.assert_called_once_with(1, 2, 3)


@mock.patch("foo.emit_line", mock.MagicMock(side_effect=lambda k, v: "%s\t%s" % (k, v)))
def test_emit_line():
    print foo.emit_line("key", "value")
    assert "key\tvalue" == foo.emit_line("key", "value")


@mock.patch("foo.emit_line", mock.MagicMock(return_value="test"))
def test_magic_method():
    assert "test" == foo.emit_line()
    foo.emit_line.__str__ = mock.Mock(return_value="test")
    assert "test" == str(foo.emit_line)


def test_patch_dict():
    foo = {"key": "value"}
    original = foo.copy()
    with mock.patch.dict(foo, {"newkey": "newvalue"}, clear=True):
        assert foo == {"newkey": "newvalue"}
    assert foo == original


@raises(TypeError)
def test_create_autospec():
    mock_function = mock.create_autospec(foo.function, return_value='fishy')
    assert mock_function(1, 2, 3) == "fishy"
    mock_function.assert_called_once_with(1, 2, 3)
    mock_function('wrong arguments')


@timed(.2)
def test_time():
    time.sleep(0.1)

if __name__ == "__main__":
    class a(object):
        pass

    real = a()
    real.method = mock.Mock()
    real.method.return_value = 3
    print real.method(3, 4, 5, key='value')
    # 验证上次调用的参数是否相同
    print real.method.assert_called_with(3, 4, 5, key='value')

    m = mock.Mock(side_effect=KeyError("foo"))
    try:
        m()
    except KeyError, e:
        print e

    values = {'a': 1, 'b': 2, 'c': 3}

    m.side_effect = lambda x: values[x]
    print m('a'), m('b'), m('c')

    m.side_effect = [5, 4, 3, 2, 1]
    print m(), m(), m(), m(), m()  # 不能循环, 只有一次