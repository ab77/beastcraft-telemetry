#!/usr/bin/env python

import argparse

from influxdb import InfluxDBClient
import os, time

WAIT_TIME = 60 # seconds

# ls /sys/bus/w1/devices
DS18D20 = [{'name': '28-00000625bd01', 'location': 'under the bed'},
	   {'name': '28-00000626bee8', 'location': 'hab space'},
	   {'name': '28-0000062841eb', 'location': 'boiler cupboard'},
	   {'name': '28-00000628c173', 'location': 'electronics cupboard'},
	   {'name': '28-021564e193ff', 'location': 'outside'}]


def main(host='localhost', port=8086):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    client = InfluxDBClient(host, port, user, password, dbname)

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    while True:            
        l = []
        for ts in DS18D20: 
            temp_sensor = '/sys/bus/w1/devices/%s/w1_slave' % ts['name']

            def temp_raw():
                f = open(temp_sensor, 'r')
                lines = f.readlines()
                f.close()
                return lines

            def read_temp():
                lines = temp_raw()
                while lines[0].strip()[-3:] != 'YES':
                    time.sleep(0.2)
                    lines = temp_raw()

                temp_output = lines[1].find('t=')
                if temp_output != -1:
                    temp_string = lines[1].strip()[temp_output+2:]
                    temp_c = float(temp_string) / 1000.0
                    return temp_c

            temp = read_temp()
            print('sensor_id=%s, temp_c=%s' % (ts['name'], temp))

            t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            json_body = {
                "measurement": "temp",
                "tags": {
                    "sensor": ts['name'],
                    "location": ts['location']
                },
                "time": t,
                "fields": {
                    "value": temp
                }
            }
            l.append(json_body)

        print("Write points: {0}".format(l))
        client.write_points(l)
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
