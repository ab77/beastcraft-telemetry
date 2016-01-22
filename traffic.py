#!/usr/bin/env python

from subprocess import Popen, PIPE

def execute(command):    
    popen = Popen(command, stdout=PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line.split(','))

execute(['/usr/local/bin/sflowtool', '-4', '-p', '6343', '-l'])

