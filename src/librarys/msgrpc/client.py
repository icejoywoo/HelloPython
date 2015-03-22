#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/2/2

__author__ = 'wujiabin'

import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('sum', 1, 2)  # = > 3
print result
