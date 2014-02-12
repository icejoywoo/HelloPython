#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-12

__author__ = 'icejoywoo'

import asynchat
import asyncore
import socket
import time


class Server(asyncore.dispatcher):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((self.ip, self.port))
        self.listen(128)

    def handle_accept(self):
        channel, address = self.accept()
        print "connected by", address
        RequestChannel(channel)


class RequestChannel(asynchat.async_chat):
    def __init__(self, channel):
        asynchat.async_chat.__init__(self, channel)
        self.set_terminator("\r\n")
        self.in_buffer = []
        self.out_buffer = []

    def handle_close(self):
        self.close()

    def handle_expt(self):
        self.close()

    def collect_incoming_data(self, data):
        self.in_buffer.append(data)

    def found_terminator(self):
        line = "".join(self.in_buffer)
        words = line.split()
        command = words[0]
        processors = {
            "time": str(time.time()) + "\r\n",
        }
        if command in processors:
            self.push(processors[command])
        else:
            self.push(line)


Server('localhost', 8080)
asyncore.loop(timeout=5, use_poll=True)
