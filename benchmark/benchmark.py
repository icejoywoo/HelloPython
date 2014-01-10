#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-10

__author__ = 'icejoywoo'

import Queue
import random
import threading
import time


class Benchmark(object):
    def __init__(self, data_loader, worker, **kvargs):
        self.queue = Queue.Queue()

        self.data_loader = data_loader
        self.kvargs = kvargs

        self.worker = worker
        self.worker_num = kvargs.get("worker_num", 10)

        self.reporter = []
        self.all_threads = []

    def run(self):
        data_loader_thread = threading.Thread(target=self.data_loader, args=(self.queue, self.reporter, self.kvargs))
        data_loader_thread.setDaemon(True)
        data_loader_thread.start()
        self.all_threads.append(data_loader_thread)

        worker_threads = [threading.Thread(target=self.worker, args=(self.queue, self.reporter, self.kvargs)) for _ in
                          xrange(self.worker_num)]
        [(t.setDaemon(True), t.start()) for t in worker_threads]
        self.all_threads += worker_threads

        [t.join() for t in self.all_threads]

        print "run done"


def data_loader(queue, reporter, kvargs):
    start = time.time()
    count = 0
    for i in file(kvargs["data_file"]):
        if time.time() - start < 1.0 and count < kvargs["max_qps"]:
            queue.put(i.lstrip("\n"))
            count += 1
        else:
            print "=======", time.time() - start, count
            count = 0
            if time.time() - start < 1.0:
                time.sleep(1.0 - (time.time() - start))
            start = time.time()


def worker(queue, reporter, kvargs):
    while True:
        task = queue.get()
        assert isinstance(task, str)
        time.sleep(random.randrange(0, 5) / 1000)
        queue.task_done()


config = {
    "worker_num": 20,
    "data_file": "test",
    "max_qps": 10000,
}

try:
    b = Benchmark(data_loader, worker, **config)
    b.run()
except KeyboardInterrupt, e:
    print e