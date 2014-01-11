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

    @property
    def count(self):
        return len(self.reporter)

    def loop(self):
        self.run()
        # join会导致主线程hang住, 无法接受信号
        # [t.join() for t in self.all_threads]
        start = time.time()
        tickets_count = 0
        while is_running:
            if (time.time() - start) * 1000 < 1000 and tickets_count < self.kvargs["max_qps"]:
                self.tickets.put(1)
                tickets_count += 1
            else:
                tickets_count = 0
                if (time.time() - start) * 1000 < 1000:
                    time.sleep(1.0 - (time.time() - start))
                start = time.time()
                if self.reporter:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    latencys = [i[1] for i in self.reporter]
                    print "[%s] qps: %d\tmax_latency: %d\tmin_latency: %d\tavg_latency: %d" \
                          % (timestamp, len(self.reporter), max(latencys), min(latencys), sum(latencys) / len(latencys))
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
        latencys = [i[1] for i in self.total_reporter]
        print "operation count: %d\tavg_latency: %d" \
              % (len(latencys), sum(latencys) / len(latencys))


def worker(bench, kvargs):
    import redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    task = 0
    while is_running:
        bench.tickets.get()
        start = time.time()
        ret = r.set("name %s" % task, "value %s" % task)
        latency = (time.time() - start) * 1000000  # ns
        bench.reporter.append((start, latency, ret))
        task += 1
        bench.tickets.task_done()


config = {
    "worker_num": 1,
    "max_qps": 10000,
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

# 极限在20000 qps左右, 可能是queue的锁比较重
with Timer(True):
    b = Benchmark(worker, **config)
    b.loop()
