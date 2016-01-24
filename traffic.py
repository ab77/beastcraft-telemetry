#!/usr/bin/env python

from subprocess import Popen, PIPE
from influxdb import InfluxDBClient
import os, time, argparse

def main(cmd=None, host=None, port=None):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    client = InfluxDBClient(host, port, user, password, dbname)

    popen = Popen(cmd, stdout=PIPE)
    lines_iterator = iter(popen.stdout.readline, b'')
    for line in lines_iterator:
        l = line.replace('\n', '').strip().split(',')
        t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        
        fields = ['sample', 'agent']
        if l[0] in 'CNTR':
            names = ['ifIndex',
                     'ifType',
                     'ifSpeed',
                     'ifDirection',
                     'ifStatus',
                     'ifInOctets',
                     'ifInUcastPkts',
                     'ifInMulticastPkts',
                     'ifInBroadcastPkts',
                     'ifInDiscards',
                     'ifInErrors',
                     'ifInUnknownProtos',
                     'ifOutOctets',
                     'ifOutUcastPkts',
                     'ifOutMulticastPkts',
                     'ifOutBroadcastPkts',
                     'ifOutDiscards',
                     'ifOutErrors',
                     'ifPromiscuousMode']

        if l[0] in 'FLOW':
            names = ['inputPort',
                     'outputPort',
                     'src_MAC',
                     'dst_MAC',
                     'ethernet_type',
                     'in_vlan',
                     'out_vlan',
                     'src_IP',
                     'dst_IP',
                     'IP_protocol',
                     'ip_tos',
                     'ip_ttl',
                     'tcp_udp_src_port_icmp_code',
                     'tcp_udp_dst_port_icmp_code',
                     'tcp_flags',
                     'packet_size',
                     'IP_size',
                     'sampling_rate']
            
        for name in names: fields.append(name)
        d = dict(zip(fields, l))

        l = []
        for k,v in d.iteritems():
            if k not in ('sample', 'agent'):
                json_body = {
                    'measurement': k,
                    'tags': {
                        'sample': d['sample'],
                        'agent': d['agent']                    
                    },
                    'time': t,
                    'fields': {
                        'value': v
                    }
                }
                l.append(json_body)

        print('Write points: {0}'.format(l))
        client.write_points(l)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--sflowcmd', type=str, required=False, default=['/usr/local/bin/sflowtool', '-4', '-p', '6343', '-l'],
                        help='sflowtool command')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(cmd=args.sflowcmd, host=args.host, port=args.port)
