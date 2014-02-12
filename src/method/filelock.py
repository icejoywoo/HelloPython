#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-14

__author__ = 'wujiabin'

import os
import errno

try:
    from fcntl import flock, LOCK_EX, LOCK_UN, LOCK_NB

    class LockFile(object):
        """
        only for *nix, not avaliable for windows
        """

        def __init__(self, path, mod):
            self.fd = open(path, mod)

        def __enter__(self):
            try:
                flock(self.fd, LOCK_EX | LOCK_NB)
                return self.fd
            except Exception as e:
                self.fd.close()
                raise e

        def __exit__(self, *args, **kwargs):
            flock(self.fd, LOCK_UN)
            self.fd.close()

    if __name__ == '__main__':
        import time

        with LockFile('xx', 'w+') as f:
            f.write('blah blah blah')
            time.sleep(3)
        print 'woo~~ ', os.getpid()
except:
    pass


class FileLockException(Exception):
    pass


class FileLock(object):
    """ A file locking mechanism that has context-manager support so
        you can use it in a with statement. This should be relatively cross
        compatible as it doesn't rely on msvcrt or fcntl for the locking.
    """

    def __init__(self, file_name, timeout=10, delay=.05):
        """ Prepare the file locker. Specify the file to lock and optionally
            the maximum timeout and the delay between each attempt to lock.
        """
        self.is_locked = False
        self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
        self.file_name = file_name
        self.timeout = timeout
        self.delay = delay

    def acquire(self):
        """ Acquire the lock, if possible. If the lock is in use, it check again
            every `wait` seconds. It does this until it either gets the lock or
            exceeds `timeout` number of seconds, in which case it throws
            an exception.
        """
        start_time = time.time()
        while True:
            try:
                # 独占式打开文件 refer: http://www.tutorialspoint.com/python/os_open.htm
                # os.O_EXCL: error if create and file exists
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException("Timeout occured.")
                time.sleep(self.delay)
        self.is_locked = True

    def release(self):
        """ Get rid of the lock by deleting the lockfile.
            When working in a `with` statement, this gets automatically
            called at the end.
        """
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False

    def __enter__(self):
        """ Activated when used in the with statement.
            Should automatically acquire a lock to be used in the with block.
        """
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        if self.is_locked:
            self.release()

    def __del__(self):
        """ Make sure that the FileLock instance doesn't leave a lockfile
            lying around.
        """
        self.release()


if __name__ == "__main__":
    import time

    with FileLock("lock") as l:
        print "lock success"
        time.sleep(5)
