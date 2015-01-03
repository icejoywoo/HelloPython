#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14/11/25

__author__ = 'icejoywoo'


import random


def produce(comsumer):
    data = random.sample(range(9), 1)[0]
    print comsumer.send(data)


def comsumer():
    while True:
        data = yield 1
        print data

if __name__ == "__main__":
    comsumer = comsumer()
    comsumer.send(None)
    produce(comsumer)
    produce(comsumer)
    #comsumer.close()
