#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-12

__author__ = 'icejoywoo'

import asynchat
import asyncore
import socket


class ClientHandler(asynchat.async_chat):
    def __init__(self, ip, port, request, response, map=None):
        asynchat.async_chat.__init__(self, map=map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((ip, port))
        self.in_buffer = []
        self.request = request
        self.response = response

    def handle_connect(self):
        self.push(self.request)
        self.set_terminator("\r\n")

    def collect_incoming_data(self, data):
        self.in_buffer.append(data)

    def found_terminator(self):
        self.response.append("".join(self.in_buffer))
        self.close()
        self.del_channel()


client_info = {}
response = []
ClientHandler("localhost", 8080, "time\r\n", response, map=client_info)
asyncore.loop(timeout=1, use_poll=True, map=client_info)
print response
