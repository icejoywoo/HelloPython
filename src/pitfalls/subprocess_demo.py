#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-3-25

import datetime
import subprocess
import time


# 无法解决stdout和stderr输出过大, 导致pipe满的问题
# 参考 http://noops.me/?p=92
def timeout_command(command, timeout):
    start = datetime.datetime.now()
    process = subprocess.Popen(command, bufsize=10000, stdout=subprocess.PIPE, close_fds=True)
    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            try:
                process.terminate()
            except:
                return None
        return None
    out = process.communicate()[0]
    if process.stdin:
        process.stdin.close()
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()
    try:
        process.kill()
    except OSError:
        pass
    return out

