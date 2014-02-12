# ^_^ encoding: utf-8 ^_^
# File: bench.bench
# @date: 2013-11-24
# @author: icejoywoo

import threading
import time


class Record(object):
    def __init__(self, buckets=(0, 10, 20, 30, 40, 50, 100, 200, 300, 400, 500, 1000, 1500, 2000)):
        self.schema = ("timestamp", "is_success", "latency")
        self.data = []
        self.report_data = {"fail": {"count": 0, "latency": []},
                            "succ": {"count": 0, "latency": []}}
        self.lock = threading.Lock()

        self.buckets = []
        self.buckets_counter = {}
        for i in range(len(buckets) - 1):
            self.buckets.append((buckets[i], buckets[i + 1]))
            self.buckets_counter[(buckets[i], buckets[i + 1])] = 0
            # 默认最大的延时为2**32
        self.buckets.append((buckets[-1], 2 ** 32))
        self.buckets_counter[(buckets[-1], 2 ** 32)] = 0

    def add(self, timestamp, is_success, lantency):
        with self.lock:
            self.data.append((timestamp, is_success, lantency))
            bucket = [bucket for bucket in self.buckets if bucket[0] <= lantency <= bucket[1]][0]
            self.buckets_counter[bucket] += 1
            key = "succ" if is_success else "fail"
            self.report_data[key]["count"] += 1
            self.report_data[key]["latency"].append(lantency)

    def report(self, clear=True):
        result = {}
        for key in ("fail", "succ"):
            lantencys = self.report_data[key]["lantency"]
            result[key] = {"min_lantency": min(lantencys), "max_lantency": max(lantencys),
                           "avg_lantency": sum(lantencys) / len(lantencys)}
            # clear the lantency
            if clear:
                self.report_data[key]["lantency"] = []
        return result

    # TODO
    def summary(self):
        pass


class Brake(object):
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


class Task(object):
    def __init__(self, interval, func, **kvargs):
        self.interval = interval
        self.nextTime = time.time() + interval
        self.func = func
        # 方法参数
        self.kvargs = kvargs

    def process(self, manager):
        ''' 处理流程, 包含传来的func, 在前后做统计
        '''
        start_time = time.time()
        if not self.kvargs:
            result = self.func()
        else:
            result = self.func(**self.kvargs)
        lantency = time.time() - start_time
        is_success = True if result else False
        manager.record.add(time.time(), is_success, lantency)
        self.nextTime = time.time() + self.interval

    def __str__(self):
        return "Task {iterval: %f, nextTime: %f}" % (self.interval, self.nextTime)


class Manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.tasks = []
        self.record = Record()
        # self.add_task(1, self.report)

    def add_task(self, interval, func, **kvargs):
        self.tasks.append(Task(interval, func, **kvargs))

    def run(self):
        while self.is_alive():
            tasks = [task for task in self.tasks if task.nextTime <= time.time()]
            for task in tasks:
                assert isinstance(task, object)
                task.process(self)
                # print task, task.nextTime - time.time()
            time.sleep(max(min([task.nextTime for task in self.tasks]) - time.time(), 0.01))

    def report(self):
        print self.record.report()


if __name__ == "__main__":
    import thread

    lock = threading.Lock()
    count = 0

    def test(a=3, b=4):
        print a, b
        with lock:
            global count
            print "Count: %d" % count
            count = 0

    def counter():
        import redis

        r = redis.Redis(host='localhost', port=6379, db=0)
        while True:
            global count
            with lock:
                r.set("name %s" % count, "value %s" % count)
                count += 1
                #time.sleep(random.random()/100)

    manager = Manager()
    manager.add_task(1, test, a=1, b=2)
    # manager.add_task(0.1, test)
    manager.start()
    thread.start_new_thread(counter, ())
    manager.join()
