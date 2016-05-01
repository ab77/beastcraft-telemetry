#!/usr/bin/env python

import argparse, requests

from influxdb import InfluxDBClient
import os, time
from pprint import pprint

WAIT_TIME = 60 # seconds


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def main(host='localhost', port=8086):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    dbclient = InfluxDBClient(host, port, user, password, dbname)

    host = '192.168.1.1'
    url = 'http://%s/cgi-bin/diagnostic_report' % host
    
    while True:
        try:
            r = requests.get(url)
            res = r.text

            l = res.split('\n')[3:12]
            fields = [el.split(' : ')[0].strip().replace(' ', '_') for el in l]
            data = [el.split(' : ')[1].strip() for el in l]
            d = dict(zip(fields, data))

            l = res.split('\n')[16:22]
            fields = [el.split(' : ')[0].strip().replace(' ', '_') for el in l]
            data = [el.split(' : ')[1].strip() for el in l]
            d = merge_dicts(d, dict(zip(fields, data)))    

            l = res.split('\n')[92:108]
            fields = [el.split(': ')[0].strip().replace(' ', '_') for el in l]
            data = [el.split(': ')[1].strip() for el in l]
            d = merge_dicts(d, dict(zip(fields, data)))

            for k,v in d.iteritems():
                try:
                    d[k] = float(v)
                except ValueError:
                    pass
                
                try:
                    d[k] = int(v)
                except ValueError:
                    pass

            l = []
            for measurement, value in d.iteritems():
                t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                if not value: continue
                json_body = {
                    "measurement": measurement,
                    "tags": {
                        "modem": host,
                    },
                    "time": t,
                    "fields": {
                        "value": value
                    }
                }
                l.append(json_body)

            print("Write points: {0}".format(l))
            dbclient.write_points(l)
            time.sleep(WAIT_TIME)
            
        except Exception, e:
            print '%s retrieving satellite modem stats, retrying in %d seconds' % (repr(e), WAIT_TIME)
            time.sleep(WAIT_TIME)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
