#!/usr/bin/env python

import argparse, requests

from influxdb import InfluxDBClient
import os, time, json
from pprint import pprint

def main(host='localhost', port=8086):
    user = 'admin'
    password = 'admin'
    dbname = 'beastcraft'
    client = InfluxDBClient(host, port, user, password, dbname)

    host = '172.17.0.1'
    url = 'http://%s/goform/goform_get_cmd_process' % host
    
    qs = {'multi_data': 1,
          'isTest': 'false',
          'sms_received_flag_flag': 0,
          'sts_received_flag_flag': 0,
          'cmd': 'modem_main_state,pin_status,loginfo,new_version_state,current_upgrade_state,is_mandatory,sms_received_flag,sts_received_flag,signalbar,network_type,network_provider,ppp_status,EX_SSID1,ex_wifi_status,EX_wifi_profile,m_ssid_enable,sms_unread_num,RadioOff,simcard_roam,lan_ipaddr,station_mac,battery_charging,battery_vol_percent,battery_pers,spn_display_flag,plmn_display_flag,spn_name_data,spn_b1_flag,spn_b2_flag,realtime_tx_bytes,realtime_rx_bytes,realtime_time,realtime_tx_thrpt,realtime_rx_thrpt,monthly_rx_bytes,monthly_tx_bytes,monthly_time,date_month,data_volume_limit_switch,data_volume_limit_size,data_volume_alert_percent,data_volume_limit_unit,roam_setting_option,upg_roam_switch,hplmn'}

    hdrs = {'Referer': 'http://%s/' % host}

    r = requests.get(url,
                     params=qs,
                     headers=hdrs)

    res = json.loads(r.text, strict=False)

    l = []
    for measurement, value in res.iteritems():
        t = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
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
