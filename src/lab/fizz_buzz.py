#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-2-14

__author__ = 'wujiabin'

# 写一个程序，打印数字1到100，3的倍数打印“Fizz”来替换这个数，5的倍数打印“Buzz”，
# 对于既是3的倍数又是5的倍数的数字打印“FizzBuzz”。
# 这个解法很精辟啊
simple = ["fizz"[x % 3 * 4::] + "buzz"[x % 5 * 4::] or x for x in range(1, 101)]
print simple

result = []
for i in range(1, 101):
    x, y = i % 3 == 0, i % 5 == 0
    if x and y:
        result.append("fizzbuzz")
    elif x:
        result.append("fizz")
    elif y:
        result.append("buzz")
    else:
        result.append(i)

print result
assert result == simple
