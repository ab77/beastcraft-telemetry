# beastcraft-telemetry
`DS18B20` one-wire temperature monitoring with Grafana and Python on a Raspberry Pi 2 inside a motorhome.

### Installation
I've built all the pre-requisites (except [Go](http://www.aymerick.com/2013/09/24/go_language_on_raspberrypi.html)) thanks to [InfluxDB, Telegraf and Grafana on a Raspberry Pi 2](http://www.aymerick.com/2015/10/07/influxdb-telegraf-grafana-raspberry-pi.html) guide. Still took a good part of two days.

    # install InfluxDB
    sudo dpkg -i ./influxdb-armhf/influxdb_0.9.6_armhf.deb
    sudo service influxdb start
    sudo update-rc.d influxdb defaults 95 10

Install pre-built Node.js for Raspberry Pi using the handy (Adafruit)[https://learn.adafruit.com/node-embedded-development/installing-node-dot-js] guide.

    # install Grafana
    sudo dpkg -i ./grafana-armhf/grafana_3.0.0-pre1_armhf.deb
    sudo service grafana-server start
    sudo update-rc.d grafana-server defaults 95 10
    
### Configuration
This repository contains configuration specific to my environment, with five `DS18B20` sensors in total. To personalise it:

1. run `pip install -r requirement.txt`
2. update `DS18B201` sensor list and database name in `w1_thermy.py`
3. [create database](https://influxdb.com/docs/v0.9/query_language/database_management.html#create-a-database-with-create-database) (e.g. grafana) for your metrics by running `influx -execute 'CREATE DATABASE grafana;`
4. [create retention policy](https://influxdb.com/docs/v0.9/query_language/database_management.html#retention-policy-management) by running `CREATE RETENTION POLICY 'grafana_retention_policy' ON 'grafana' DURATION '4w' REPLICATION 3 DEFAULT`

#### Temperature Dashboard

1. schedule `w1_therm.py` to run every x minutes using cron (e.g. `*/5 * * * * /opt/beastcraft-telemetry/w1_therm.py`)
2. go to [http://localhost:3000](http://localhost:3000), add a new datasource and configure other options
3. import `temp.json` dashboard and modify it to suit your needs or build your own from scratch (change URLs to suit your environment)

#### UPS/Inverter Dashboard

1. ensure [Network UPS Tools](http://www.networkupstools.org/) is correctly configured to work with the UPS (use `blazer_ser` driver)
2. edit `ups.py` and adjust the default `upsname` (mine is `upsoem`) or pass from the command line using `--ups` parameter
3. schedule `usp.py` to run every x minutes using cron (e.g. `*/5 * * * * /opt/beastcraft-telemetry/ups.py`)
4. import `ups.json` dashboard and modify it to suit your needs or build your own from scratch (change URLs to suit your environment)

#### Traffic Dashboard
TBC

#### Mobile Broadband Dashboard

1. update `host` variable in `mobilebroadband.py` to match your ZTE MF823 modem IP address
2. schedule `mobilebroadband.py` to run every x minutes using cron (e.g. `*/1 * * * * /opt/beastcraft-telemetry/mobilebroadband.py`)
3. install `Nginx` and configure it as a reverse proxy for both Grafana and ZTE web GUIs (the later is required to set the `Referer` header)
4. import `mobilebroadband.json` dashboard and modify it to suit your needs or build your own from scratch (change URLs to suit your environment)

````
pi@localhost ~ $ cat /etc/nginx/sites-enabled/grafana
server {

	listen 80;
	server_name <your_host_name>;

	location / {
		proxy_pass http://localhost:3000/;
	}

	location /public/ {
		alias /usr/share/grafana/public/;
	}

	location /goform/ {
		proxy_set_header Referer http://<your_ZTE-MF823_modem_IP>/;
		proxy_pass http://<your_ZTE-MF823_modem_IP>:80/goform/;
	}
}
````

The ZTE MF823 has a REST API apart from the web GUI, which we are using to communicate with the modem from within the Grafana dashboard. The full list of command sisn't published, but looking at the modem's web interface with Chrome Developer Tools, the following commands were evident.

```
# connect mobile network (HTTP GET)
http://<modem_IP>/goform//goform_set_cmd_process?isTest=false&notCallback=true&goformId=CONNECT_NETWORK

# disconnect mobile network (HTTP GET)
http://<modem_IP>/goform//goform_set_cmd_process?isTest=false&notCallback=true&goformId=DISCONNECT_NETWORK

# modem state (HTTP GET)
http://<modem_IP>/goform/goform_get_cmd_process?multi_data=1&isTest=false&sms_received_flag_flag=0&sts_received_flag_flag=0&cmd=modem_main_state%2Cpin_status%2Cloginfo%2Cnew_version_state%2Ccurrent_upgrade_state%2Cis_mandatory%2Csms_received_flag%2Csts_received_flag%2Csignalbar%2Cnetwork_type%2Cnetwork_provider%2Cppp_status%2CEX_SSID1%2Cex_wifi_status%2CEX_wifi_profile%2Cm_ssid_enable%2Csms_unread_num%2CRadioOff%2Csimcard_roam%2Clan_ipaddr%2Cstation_mac%2Cbattery_charging%2Cbattery_vol_percent%2Cbattery_pers%2Cspn_display_flag%2Cplmn_display_flag%2Cspn_name_data%2Cspn_b1_flag%2Cspn_b2_flag%2Crealtime_tx_bytes%2Crealtime_rx_bytes%2Crealtime_time%2Crealtime_tx_thrpt%2Crealtime_rx_thrpt%2Cmonthly_rx_bytes%2Cmonthly_tx_bytes%2Cmonthly_time%2Cdate_month%2Cdata_volume_limit_switch%2Cdata_volume_limit_size%2Cdata_volume_alert_percent%2Cdata_volume_limit_unit%2Croam_setting_option%2Cupg_roam_switch%2Chplmn

# ConnectionMode (dial mode auto|manual)
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=ConnectionMode

# enable roaming
http://<modem_IP>/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=SET_CONNECTION_MODE&roam_setting_option=on

# disable roaming
http://<modem_IP>/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=SET_CONNECTION_MODE&roam_setting_option=off

# enable auto-dial
http://<modem_IP>/goform/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=SET_CONNECTION_MODE&ConnectionMode=auto_dial

# disable auto-dial
http://<modem_IP>/goform/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=SET_CONNECTION_MODE&ConnectionMode=manual_dial

# upgrade_result
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=upgrade_result

# current_upgrade_state
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=current_upgrade_state

# sms_data_total
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=500&mem_store=1&tags=10&order_by=order+by+id+desc

# sms_capacity_info
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=sms_capacity_info

# sms_parameter_info
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=sms_parameter_info

# pbm_init_flag
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=pbm_init_flag

# pbm_capacity_info&pbm_location=pbm_sim
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=pbm_capacity_info&pbm_location=pbm_sim

# mem__data_total
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&mem_store=2&cmd=pbm_data_total&page=0&data_per_page=2000&orderBy=name&isAsc=true

# m_ssid_enable
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=m_ssid_enable%2CSSID1%2CAuthMode%2CHideSSID%2CWPAPSK1%2CMAX_Access_num%2CEncrypType%2Cm_SSID%2Cm_AuthMode%2Cm_HideSSID%2Cm_WPAPSK1%2Cm_MAX_Access_num%2Cm_EncrypType&multi_data=1

# pbm_capacity_info&pbm_location=pbm_native
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=pbm_capacity_info&pbm_location=pbm_native

# sim_imsi
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&multi_data=1&cmd=sim_imsi%2Csim_imsi_lists

# wifi_coverage
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=wifi_coverage%2Cm_ssid_enable%2Cimei%2Cweb_version%2Cwa_inner_version%2Chardware_version%2CMAX_Access_num%2CSSID1%2Cm_SSID%2Cm_HideSSID%2Cm_MAX_Access_num%2Clan_ipaddr%2Cwan_active_band%2Cmac_address%2Cmsisdn%2CLocalDomain%2Cwan_ipaddr%2Cipv6_wan_ipaddr%2Cipv6_pdp_type%2Cpdp_type%2Cppp_status%2Csim_iccid%2Csim_imsi%2Crmcc%2Crmnc%2Crssi%2Crscp%2Clte_rsrp%2Cecio%2Clte_snr%2Cnetwork_type%2Clte_rssi%2Clac_code%2Ccell_id%2Clte_pci%2Cdns_mode%2Cprefer_dns_manual%2Cstandby_dns_manual%2Cprefer_dns_auto%2Cstandby_dns_auto%2Cipv6_dns_mode%2Cipv6_prefer_dns_manual%2Cipv6_standby_dns_manual%2Cipv6_prefer_dns_auto%2Cipv6_standby_dns_auto%2Cmodel_name&multi_data=1

# current_network_mode
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=current_network_mode%2Cm_netselect_save%2Cnet_select_mode%2Cm_netselect_contents%2Cnet_select%2Cppp_status%2Cmodem_main_state%2Clte_band_lock%2Cwcdma_band_lock&multi_data=1

# APN_config0
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=APN_config0%2CAPN_config1%2CAPN_config2%2CAPN_config3%2CAPN_config4%2CAPN_config5%2CAPN_config6%2CAPN_config7%2CAPN_config8%2CAPN_config9%2CAPN_config10%2CAPN_config11%2CAPN_config12%2CAPN_config13%2CAPN_config14%2CAPN_config15%2CAPN_config16%2CAPN_config17%2CAPN_config18%2CAPN_config19%2Cipv6_APN_config0%2Cipv6_APN_config1%2Cipv6_APN_config2%2Cipv6_APN_config3%2Cipv6_APN_config4%2Cipv6_APN_config5%2Cipv6_APN_config6%2Cipv6_APN_config7%2Cipv6_APN_config8%2Cipv6_APN_config9%2Cipv6_APN_config10%2Cipv6_APN_config11%2Cipv6_APN_config12%2Cipv6_APN_config13%2Cipv6_APN_config14%2Cipv6_APN_config15%2Cipv6_APN_config16%2Cipv6_APN_config17%2Cipv6_APN_config18%2Cipv6_APN_config19%2Cm_profile_name%2Cprofile_name%2Cwan_dial%2Capn_select%2Cpdp_type%2Cpdp_select%2Cpdp_addr%2Cindex%2CCurrent_index%2Capn_auto_config%2Cipv6_apn_auto_config%2Capn_mode%2Cwan_apn%2Cppp_auth_mode%2Cppp_username%2Cppp_passwd%2Cdns_mode%2Cprefer_dns_manual%2Cstandby_dns_manual%2Cipv6_wan_apn%2Cipv6_pdp_type%2Cipv6_ppp_auth_mode%2Cipv6_ppp_username%2Cipv6_ppp_passwd%2Cipv6_dns_mode%2Cipv6_prefer_dns_manual%2Cipv6_standby_dns_manual&multi_data=1

# lan_ipaddr
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=lan_ipaddr%2Clan_netmask%2Cmac_address%2CdhcpEnabled%2CdhcpStart%2CdhcpEnd%2CdhcpLease_hour&multi_data=1

# DMZEnable
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=DMZEnable%2CDMZIPAddress&multi_data=1

# PortMapEnable
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=PortMapEnable%2CPortMapRules_0%2CPortMapRules_1%2CPortMapRules_2%2CPortMapRules_3%2CPortMapRules_4%2CPortMapRules_5%2CPortMapRules_6%2CPortMapRules_7%2CPortMapRules_8%2CPortMapRules_9&multi_data=1

# IPPortFilterEnable
http://<modem_IP>/goform/goform_get_cmd_process?isTest=false&cmd=IPPortFilterEnable%2CDefaultFirewallPolicy%2CIPPortFilterRules_0%2CIPPortFilterRules_1%2CIPPortFilterRules_2%2CIPPortFilterRules_3%2CIPPortFilterRules_4%2CIPPortFilterRules_5%2CIPPortFilterRules_6%2CIPPortFilterRules_7%2CIPPortFilterRules_8%2CIPPortFilterRules_9%2CIPPortFilterRulesv6_0%2CIPPortFilterRulesv6_1%2CIPPortFilterRulesv6_2%2CIPPortFilterRulesv6_3%2CIPPortFilterRulesv6_4%2CIPPortFilterRulesv6_5%2CIPPortFilterRulesv6_6%2CIPPortFilterRulesv6_7%2CIPPortFilterRulesv6_8%2CIPPortFilterRulesv6_9&multi_data=1
```

All the API requests require the `Referer: http://<your_ZTE-MF823_modem_IP>/` request header present. No additional headers are required.

-- ab1
