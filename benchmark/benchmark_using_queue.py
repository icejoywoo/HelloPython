#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-10

__author__ = 'icejoywoo'

import Queue
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
    def __init__(self, worker, **kvargs):
        # 用queue做tickets来做速度控制
        self.tickets = Queue.Queue()
        self.kvargs = kvargs

        self.worker = worker
        self.worker_num = kvargs.get("worker_num", 10)

        self.total_reporter = []
        self.reporter = []
        self.all_threads = []

    def run(self):
        worker_threads = [threading.Thread(target=self.worker, args=(self, self.kvargs)) for _ in
                          xrange(self.worker_num)]
        [(t.setDaemon(True), t.start()) for t in worker_threads]
        self.all_threads += worker_threads

    def loop(self):
        self.run()
        # join会导致主线程hang住, 无法接受信号
        # [t.join() for t in self.all_threads]
        start = time.time()
        tickets_count = self.kvargs["max_qps"]
        while is_running:
            if (time.time() - start) * 1000 < 1000 and tickets_count > 0:
                self.tickets.put(self.kvargs["step"])
                tickets_count -= self.kvargs["step"]
            else:
                tickets_count = self.kvargs["max_qps"]
                if (time.time() - start) * 1000 < 1000:
                    time.sleep(1.0 - (time.time() - start))
                start = time.time()
                if self.reporter:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    latencies = [i[1] for i in self.reporter]
                    print "[%s] qps: %d\tmax_latency: %d\tmin_latency: %d\tavg_latency: %d" \
                          % (timestamp, len(self.reporter), max(latencies), min(latencies),
                             sum(latencies) / len(latencies))
                    self.total_reporter += self.reporter
                    self.reporter = []
        self.summary()

    def stop(self):
        for t in self.all_threads:
            t.kill_received = True
        global is_running
        is_running = False

    def summary(self):
        # summary
        latencies = [i[1] for i in self.total_reporter]
        print "operation count: %d\tavg_latency: %d" \
              % (len(latencies), sum(latencies) / len(latencies))


def worker(func):
    """
    @param func: decorator method's function
    @return: a benchmark worker
    """

    def __worker(bench, kvargs):
        while is_running:
            count = bench.tickets.get()
            for _ in xrange(count):
                start = time.time()
                ret = func(kvargs)
                latency = (time.time() - start) * 1000000  # ns
                bench.reporter.append((start, latency, ret))
            bench.tickets.task_done()

    return __worker


config = {
    "worker_num": 10,
    "max_qps": 1000,
    "step": 1, # step 越小 qps控制得越好
}


# timer 可以在退出的时候打报告什么的
class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.start = 0
        self.elapsed_ms = 0

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed_ms = (time.time() - self.start) * 1000
        if self.verbose:
            print 'elapsed time: %f ms' % self.elapsed_ms


@worker
def test_worker(kvargs):
    if kvargs["step"] == 1:
        return 0
    else:
        return -1


with Timer(True):
    b = Benchmark(test_worker, **config)
    b.loop()
