#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-8

__author__ = 'wujiabin'

import threading
import time
from time import sleep

def test_func(id):
    time.sleep(1)
    print('thread %d is running \n' % id)

threads = [threading.Thread(target=test_func, args=(i,)) for i in range(3)]

for t in threads:
    t.setDaemon(True)
    t.start()
# for t in threads:
#     t.join()
print "[main]\n"