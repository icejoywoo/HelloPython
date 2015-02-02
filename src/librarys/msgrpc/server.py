#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/2/2

__author__ = 'wujiabin'

import msgpackrpc


class SumServer(object):

    def sum(self, x, y):
        return x + y

server = msgpackrpc.Server(SumServer())
server.listen(msgpackrpc.Address("localhost", 18800))
server.start()
