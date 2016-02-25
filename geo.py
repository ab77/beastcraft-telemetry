#!/usr/bin/env python 

from influxdb import InfluxDBClient
import os, time, json, gps, argparse, requests
from pprint import pprint

SLEEP_WAIT = 300 # seconds wait between readings


def main(host='localhost', port=8086):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    dbclient = InfluxDBClient(host, port, user, password, dbname)
    
    session = gps.gps(host='localhost', port='2947')

    session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
    for report in session:
      report = report.__dict__
      if report['class'] == 'TPV':
        report['geo'] = '%s,%s' % (report['lat'], report['lon'])
	l = []
        for measurement, value in report.iteritems():
            t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            if measurement not in ['class', 'tag', 'device']:
              json_body = {
                  'measurement': measurement,
                  'tags': {
                      'class': report['class'],
                      'tag': report['tag'],
                      'device': report['device']
                  },
                  'time': t,
                  'fields': {
                      'value': value
                  }
              }
              l.append(json_body)

        print('Write points: {0}'.format(l))
        dbclient.write_points(l)
        time.sleep(SLEEP_WAIT)


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
