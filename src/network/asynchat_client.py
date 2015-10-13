#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-1-12

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


response = []
ClientHandler("localhost", 8080, "time\r\n", response)
asyncore.loop(timeout=1, use_poll=True, count=5)
print response
