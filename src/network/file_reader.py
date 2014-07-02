#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-7-2

__author__ = 'wujiabin'

import asyncore
import os

class FileReader(asyncore.file_dispatcher):

    def writable(self):
        return False

    def handle_read(self):
        data = self.recv(256)
        print 'READ: (%d) "%s"' % (len(data), data)

    def handle_expt(self):
        # Ignore events that look like out of band data
        pass

    def handle_close(self):
        self.close()

lorem_fd = os.open('lorem.txt', os.O_RDONLY)
reader = FileReader(lorem_fd)
asyncore.loop()
