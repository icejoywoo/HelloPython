#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-3-25

__author__ = 'icejoywoo'

# http://stackoverflow.com/questions/5911362/pipe-large-amount-of-data-to-stdin-while-using-subprocess-popen
import subprocess
from select import select
import os
import shlex


def run_command(cmd, bufsize=1024):
    proc = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            shell=False, universal_newlines=True)
    stdout, stderr = [], []
    while True:
        rlist, wlist, xlist = [proc.stdout, proc.stderr], [], []
        rlist, wlist, xlist = select(rlist, wlist, xlist)
        if proc.stdout in rlist:
            out1 = os.read(proc.stdout.fileno(), bufsize)
            stdout.append(out1)
        if proc.stderr in rlist:
            out2 = os.read(proc.stdout.fileno(), bufsize)
            stderr.append(out2)
        if not out1 and not out2:
            break
    return "".join(stdout), "".join(stderr)

if __name__ == "__main__":
    stdout, stderr = run_command("ls -R ../..")
    print stdout