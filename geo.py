#!/usr/bin/env python 

from influxdb import InfluxDBClient
import sys, os, time, json, gps, argparse, requests, calendar
from pprint import pprint
from datetime import datetime
import numpy as np
import dns.query
import dns.tsigkeyring
import dns.update
import dns.rdatatype

WAIT_TIME = 60 # seconds


def main(host='localhost', port=8086, domain=None, key=None):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    dbclient = InfluxDBClient(host, port, user, password, dbname)
    
    session = gps.gps(host='localhost', port='2947')
    session.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)
    start_time = time.time() - WAIT_TIME
    reports = []
    for report in session:
        report = report.__dict__
        if report['class'] == 'TPV':	
            reports.append(report)
            if time.time() - start_time > WAIT_TIME:                
                write_db(dbclient, summarise_rpt(reports), domain=domain, key=key)
                reports = []
                start_time = time.time()


def average_val(rpts, name):
    l =  [rpt[name] for rpt in rpts]
    return reduce(lambda x, y: x + y, l) / len(l)


def median_val(rpts, name):
    l =  [rpt[name] for rpt in rpts]
    return np.percentile(l, 50)

    
def summarise_rpt(rpts):
    report = dict()
    report['lat'] = median_val(rpts, 'lat')
    report['lon'] = median_val(rpts, 'lon')
    report['epx'] = median_val(rpts, 'epx')
    report['epy'] = median_val(rpts, 'epy')
    report['epv'] = median_val(rpts, 'epv')
    report['ept'] = median_val(rpts, 'ept')
    report['eps'] = median_val(rpts, 'eps')
    report['climb'] = median_val(rpts, 'climb')
    report['alt'] = median_val(rpts, 'alt')
    report['speed'] = median_val(rpts, 'speed')
    report['tag'] = [rpt['tag'] for rpt in rpts][-1]
    report['time'] = [rpt['time'] for rpt in rpts][-1]
    report['device'] = [rpt['device'] for rpt in rpts][-1]
    report['class'] = [rpt['class'] for rpt in rpts][-1]
    report['mode'] = [rpt['mode'] for rpt in rpts][-1]
    report['track'] = [rpt['track'] for rpt in rpts][-1]
    report['geo'] = '%s,%s' % (report['lat'], report['lon'])
    report['epoch'] = calendar.timegm(datetime.strptime(report['time'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())    

    return report

    
def write_db(dbc, rpt, domain=None, key=None):
    l = []
    for measurement, value in rpt.iteritems():
        t = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        if measurement not in ['class', 'tag', 'device']:
          json_body = {
              'measurement': measurement,
              'tags': {
                  'class': rpt['class'],
                  'tag': rpt['tag'],
                  'device': rpt['device']
              },
              'time': t,
              'fields': {
                  'value': value
              }
          }
          l.append(json_body)
    
    print('Write points: {0}'.format(l))
    dbc.write_points(l)
    update_dns(coords=rpt['geo'], domain=domain, key=key)


def update_dns(coords=None, domain=None, key=None):
    if domain and key and coords:
        keyring = dns.tsigkeyring.from_text({
            domain : key
        })  
        
        update = dns.update.Update(domain, keyring=keyring)
        update.replace('geo', 300, dns.rdatatype.TXT, '"%s"' % coords)
    
        return dns.query.tcp(update, 'localhost')
    else:
        return None


def parse_args():
    parser = argparse.ArgumentParser(description='GPSd InfluxDB loader')
    parser.add_argument('--host', type=str, required=False, default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    parser.add_argument('--domain', type=str, required=False, default=None,
                        help='DNS domain to update with geo TXT record')                        
    parser.add_argument('--key', type=str, required=False, default=None,
                        help='DNSSEC key')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host,
         port=args.port,
         domain=args.domain,
         key=args.key)
