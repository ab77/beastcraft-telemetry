#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

# run the shell as a subprocess:
p = Popen(['ssh', '%s'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# set the O_NONBLOCK flag of p.stdout file descriptor:
flags = fcntl(p.stdout, F_GETFL) # get current p.stdout flags
fcntl(p.stdout, F_SETFL, flags | O_NONBLOCK)
# get the output
while True:
    # issue command:
    p.stdin.write('diag sys link-monitor status wifi\n')
    # let the shell output the result:
    sleep(2)
    try:
        print read(p.stdout.fileno(), 1024),
    except OSError:
        # the os throws an exception if there is no data
        sleep(10)
