#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-2-18

__author__ = 'wujiabin'

from sklearn import linear_model


clf = linear_model.LinearRegression()
print clf.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
print clf.coef_
