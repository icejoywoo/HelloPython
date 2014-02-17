#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-2-17

__author__ = 'icejoywoo'
# http://pymotw.com/2/struct/
# http://docs.python.org/2/library/struct.html

s = 'Hello world'
t = buffer(s, 6, 5)  # 原型 buffer(object[, offset[, size]])
s = bytearray(100)  # 一个大小100的字节数组, 每个元素都是0
s[0] = 1

print t, repr(t), dir(t)
# print s, repr(s), dir(s)

from array import array

a = array('B', [0x7C, 0xF8, 0x65, 0x17, 0x98, 0x7F, 0x1B, 0x3E])
print a, repr(a)

import struct

data = struct.pack("<ii", 90, 20)
print repr(data), len(data)

a1, a2 = struct.unpack("<ii", data)
print a1, a2

print struct.calcsize("<iihl")  # 2*4+2+4=14

from ctypes import create_string_buffer

buf = create_string_buffer(12)
print repr(buf.raw)

struct.pack_into("<iii", buf, 0, 1, 2, -1)  # struct.pack_into(fmt, buffer, offset, v1, v2, ...)¶
print repr(buf.raw)

print struct.unpack_from('<iii', buf, 0)  # struct.unpack_from(fmt, buffer[, offset=0])

# class
s = struct.Struct("<cihl")
data = s.pack('c', 100, 3, 10000)
print data
print s.unpack(data)
