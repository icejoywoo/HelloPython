#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-8-18
"""
A simple logging utility.
"""

import logging


def get_logger(name):
    return logging.getLogger(name)
