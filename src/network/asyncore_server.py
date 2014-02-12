#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-12

__author__ = 'icejoywoo'

import asyncore
import socket


class Server(asyncore.dispatcher):
    def __init__(self, host='', port=5007):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(100)

    def handle_accept(self):
        # when we get a client connection start a dispatcher for that
        # client
        socket, address = self.accept()
        print 'Connection by', address
        EchoHandler(socket)


class EchoHandler(asyncore.dispatcher_with_send):
    # dispatcher_with_send extends the basic dispatcher to have an output
    # buffer that it writes whenever there's content
    def handle_read(self):
        self.in_buffer = self.recv(1024)
        if self.in_buffer == "time":
            import time

            self.out_buffer = str(time.time())
        else:
            self.out_buffer = self.in_buffer
        if not self.out_buffer:
            self.close()


s = Server('', 8080)
asyncore.loop()
