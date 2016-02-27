#!/usr/bin/env python

from influxdb import InfluxDBClient
import os, time, PyNUT, argparse

WAIT_TIME = 60 # seconds


def main(host='localhost', port=8086, ups='upsoem'):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    dbclient = InfluxDBClient(host, port, user, password, dbname)

    nutclient = PyNUT.PyNUTClient()
    
    while True:
        nutstats = nutclient.GetUPSVars(ups)

        for k,v in nutstats.iteritems():
            try:
                nutstats[k] = float(v)
            except ValueError:
                pass

            try:
                nutstats[k] = int(v)
            except ValueError:
                pass

        l = []
        for measurement, value in nutstats.iteritems():
            t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            json_body = {
                'measurement': measurement,
                'tags': {
                    'ups': ups,
                },
                'time': t,
                'fields': {
                    'value': value
                }
            }
            l.append(json_body)

        print("Write points: {0}".format(l))
        dbclient.write_points(l)
        time.sleep(WAIT_TIME)


def parse_args():
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--ups', type=str, required=False, default='upsoem',
                        help='UPS name as defined in /etc/nut.conf')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port, ups=args.ups)
