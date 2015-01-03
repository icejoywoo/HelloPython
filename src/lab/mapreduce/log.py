#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-8-18
"""
A simple logging utility.
"""
__author__ = 'icejoywoo'

import logging


def get_logger(name):
    return logging.getLogger(name)
