#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-14

__author__ = 'wujiabin'

"""
only for *nix, not avaliable for windows
"""

from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB

class LockFile(object):
    def __init__(self, path, mod):
        self.fd = open(path, mod)

    def __enter__(self):
        try:
            flock(self.fd, LOCK_EX | LOCK_NB)
            return self.fd
        except Exception as e:
            self.fd.close()
            raise e

    def __exit__(self, *args, **kwargs):
        flock(self.fd, LOCK_UN)
        self.fd.close()


if __name__ == '__main__':
    import time
    import os
    with LockFile('xx', 'w+') as f:
        f.write('blah blah blah')
        time.sleep(3)
    print 'woo~~ ', os.getpid()
