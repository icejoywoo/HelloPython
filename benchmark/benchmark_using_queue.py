#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-10

__author__ = 'icejoywoo'

import Queue
import random
import signal
import threading
import time

is_running = True


def signal_handler(signum, frame):
    """
    接收两种信号后退出,SIGINT + SIGTERM
    """
    global is_running
    is_running = False
    return


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
try:
    # 忽略SIGPIPE
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except:
    pass


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

        # [t.join() for t in self.all_threads]

    def stop(self):
        for t in self.all_threads:
            t.kill_received = True


def data_loader(queue, reporter, kvargs):
    start = time.time()
    count = 0
    while is_running:
        for i in file(kvargs["data_file"]):
            if time.time() - start < 1.0 and count < kvargs["max_qps"]:
                while queue.qsize() > 100:
                    print "qsize: %d" % queue.qsize()
                    time.sleep(0.000001)
                queue.put(i.lstrip("\n"))
                count += 1
            else:
                if (time.time() - start) * 1000 < 1000:
                    time.sleep(1.0 - (time.time() - start))
                print "=======", time.time() - start, count
                count = 0
                start = time.time()


def worker(queue, reporter, kvargs):
    while is_running:
        task = queue.get()
        assert isinstance(task, str)
        #time.sleep(random.randrange(0, 5) / 1000)
        queue.task_done()


config = {
    "worker_num": 50,
    "data_file": "test",
    "max_qps": 100000,
}


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs

# 极限在2000 qps左右, 可能是queue的锁比较重
with Timer(True):
    b = Benchmark(data_loader, worker, **config)
    b.run()
    while True:
        time.sleep(1)
