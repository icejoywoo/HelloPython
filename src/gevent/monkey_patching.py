#!/bin/env python
# encoding: utf-8
# @author: icejoywoo

import socket
from gevent import monkey
import select

print(socket.socket)

print("After monkey patch")

monkey.patch_socket()
print(socket.socket)


print(select.select)
monkey.patch_select()
print("After monkey patch")
print(select.select)
