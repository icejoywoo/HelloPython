#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-2-12

"""
官网文档的解释:
CPython implementation detail: Objects of different types except numbers are ordered by their type names; objects of the same types that don’t support proper comparison are ordered by their address.

CPython的实现细节汇总:

规则1: 除数字类型外不同类型的对象是按照类型的名字来排序的.

规则2: 不支持比较操作的相同类型的对象是按照地址来排序的.

规则3: 比较两个字符串或两个数字类型, 比较结果是符合预期的(字符串是字典顺序, 整型是数字大小的顺序)
原文: When you order two strings or two numeric types the ordering is done in the expected way (lexicographic ordering for string, numeric ordering for integers).

规则4:比较数字类型和非数字类型的时候, 数字类型在前(就是数字类型 < 非数字类型)
原文: When you order a numeric and a non-numeric type, the numeric type comes first.

规则1的例外: 旧风格的类小于新风格的类.
原文: One exception is old-style classes that always come before new-style classes.
"""
# http://docs.python.org/2/library/stdtypes.html#comparisons
# http://stackoverflow.com/questions/3270680/how-does-python-compare-string-and-int


class Foo(object):
    pass


class Bar(object):
    pass

# 规则1
print Foo() > Bar()

# 规则2
a, b = Foo(), Foo()
print id(a) > id(b), id(a), id(b)
print a > b

# 规则3
print 100 > 1
print 'b' > 'a'


class Foo:
    pass


class Bar(object):
    pass

# 规则4
print Foo > 1000  # classobj > int
f = Foo()
print id(f) < id(1000), id(f), id(1000), id(1000)
print f < 1000  # old-style class instance > int 应该是 Foo() > 1000, 这不符合规则4, Foo是old-style类
print Bar() > 1000  # new-style class instance > int

print 'a' > 1000  # str > int
print {} > 1000  # dict > int
print [] > 1000  # list > int
print (1,) > 1000  # tuple > int

# 规则1的例外
print Foo() < Bar()  # old-style class < new-style class
