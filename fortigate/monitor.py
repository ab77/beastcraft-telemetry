#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import argparse


def set_defaut_route(p=None, iface='wifi', gw='0.0.0.0'):
    print 'setting default route iface=%s gw=%s\n' % (iface, gw)
    p.stdin.write('config router static\nedit 1\nset device %s\nset gateway %s\nend\n' % (iface, gw))

    
def main(user='admin', host=None, port=22, iface=None, backup=None, gwip=None):
    # assume interface is online
    iface_status = 'alive'
    # run the shell as a subprocess:
    p = Popen(['ssh', '%s@%s' % (user, host)],
              stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
    # set the O_NONBLOCK flag of p.stdout file descriptor:
    flags = fcntl(p.stdout, F_GETFL) # get current p.stdout flags
    fcntl(p.stdout, F_SETFL, flags | O_NONBLOCK)
    # get the output
    while True:
        # issue command:
        p.stdin.write('diag sys link-monitor status %s\n' % iface)
        # let the shell output the result:
        sleep(5)
        try:
            line = read(p.stdout.fileno(), 1024)
            if line.split()[0] == 'Link':
                print '%s %s %s' % (line.split()[2], line.split()[3], line.split()[4])
                if line.split()[4] == 'die' and iface_status == 'alive':
                    iface_status = line.split()[4]
                    set_defaut_route(p=p, iface=backup, gw=args.gwip)
                if line.split()[4] == 'alive' and iface_status == 'die':
                    set_defaut_route(p=p, iface=iface)
                    iface_status = line.split()[4]
                    
        except OSError:
            # the os throws an exception if there is no data
            sleep(5)


def parse_args():
    parser = argparse.ArgumentParser(description='FortiGate interface monitor')
    parser.add_argument('--host', type=str, required=True, default=None,
                        help='FortiGate appliance hostname or IP')
    parser.add_argument('--port', type=int, required=False, default=22,
                        help='SSH port of the FortiGate appliance')
    parser.add_argument('--user', type=str, required=False, default='admin',
                        help='FortiGate admin username')
    parser.add_argument('--iface', type=str, required=True, default=None,
                        help='FortiGate interface to monitor (e.g. wifi)')
    parser.add_argument('--backup', type=str, required=True, default=None,
                        help='FortiGate interface to fail-over to (e.g. wan2)')
    parser.add_argument('--gwip', type=str, required=True, default=None,
                        help='Backup interface gateway ipaddr')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(user=args.user,
         host=args.host,
         port=args.port,
         iface=args.iface,
         backup=args.backup,
         gwip=args.gwip)
