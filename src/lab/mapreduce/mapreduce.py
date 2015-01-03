#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-8-18

__author__ = 'icejoywoo'

import multiprocessing


class MapReduceJob(object):
    def __init__(self, mapper, reducer, **kwargs):
        self._mapper = mapper
        self._reducer = reducer

        num_workers = kwargs.get('num_workers', None)
        self._pool = multiprocessing.Pool(num_workers)

        # map reduce的个数
        self._map_num = kwargs.get('map_num', None)
        self._red_num = kwargs.get('red_num', None)

        # tmp dirs
        self._tmp_dirs = kwargs.get('tmp_dirs', None)

    def map(self, inputs):
        """
        a mapper decorator
        @param func:
        @return:
        """
        self._map_num = len(inputs)
        outputs = self._pool.imap(self._mapper, inputs)
        return outputs

    def partition(self, inputs):
        inputs = list(inputs)
        outputs = []
        while inputs:
            for index, value in enumerate(inputs):
                if value.ready():
                    if value.successful():
                        pass

    def sort(self, inputs):
        pass

    def reduce(self):
        pass

    def __call__(self, *args, **kwargs):
        pass
