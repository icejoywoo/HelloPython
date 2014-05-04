__author__ = 'icejoywoo'

# http://xlambda.com/gevent-tutorial/

import gevent


def foo():
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')


def bar():
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')


# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar),
# ])

# 执行顺序和传入顺序有关
gevent.joinall([
    gevent.spawn(bar),
    gevent.spawn(foo),
])