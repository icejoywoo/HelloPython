#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-12

__author__ = 'icejoywoo'

import asyncore
import socket


class Client(asyncore.dispatcher_with_send):
    def __init__(self, host, port, message):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.out_buffer = message

    def handle_close(self):
        self.close()

    def handle_read(self):
        print 'Received', self.recv(1024)
        self.close()


c = Client('', 8080, 'Hello, world\r\n')
c = Client('', 8080, 'time\r\n')
asyncore.loop()


