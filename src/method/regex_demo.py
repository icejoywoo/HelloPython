#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-18

__author__ = 'wujiabin'

import re

# 去掉不是11这样重复的一对数字, 就是45
pattern = re.compile(r"(.)(\1)")
print ",".join(["".join(i) for i in pattern.findall("11223345667788")])

# 如果是多个数字重复的话该怎么做, 如果知道长度还好, 定长重复
pattern = re.compile(r"(.{3})(\1)")
print ",".join(["".join(i) for i in pattern.findall("1231232222223345667788")])
