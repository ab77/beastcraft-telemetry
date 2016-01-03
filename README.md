# beastcraft-telemetry
`DS19B20` one-wire temperature monitoring with Grafana and Python on a Raspberry Pi 2 inside a motorhome.

### Installation
I've built all the pre-requisites (except [Go](http://www.aymerick.com/2013/09/24/go_language_on_raspberrypi.html)) thanks to [InfluxDB, Telegraf and Grafana on a Raspberry Pi 2](http://www.aymerick.com/2015/10/07/influxdb-telegraf-grafana-raspberry-pi.html) guide.

    # install InfluxDB
    sudo dpkg -i ./influxdb-armhf/influxdb_0.9.6_armhf.deb
    sudo service influxdb start
    sudo update-rc.d grafana-server defaults 95 10

Install pre-built Node.js for Raspberry Pi using the handy (Adafruit)[https://learn.adafruit.com/node-embedded-development/installing-node-dot-js] guide.

    # install Grafana
    sudo dpkg -i ./grafana-armhf/grafana_3.0.0-pre1_armhf.deb
    sudo service grafana-server start
    sudo update-rc.d grafana-server defaults 95 10
    
### Configuration
This repository contains configuration specific to my environment, with five `DS18B20` sensors in total. To personalise it:

1. run `pip install -r requirement.txt`
2. update `DS18B201 sensor list and database name in `w1_thermy.py`
3. [create database](https://influxdb.com/docs/v0.9/query_language/database_management.html#create-a-database-with-create-database) (e.g. grafana) for your metrics by running `influx -execute 'CREATE DATABASE grafana;`
4. [create retention policy](https://influxdb.com/docs/v0.9/query_language/database_management.html#retention-policy-management) by running `CREATE RETENTION POLICY 'grafana_retention_policy' ON 'grafana' DURATION '4w' REPLICATION 3 DEFAULT`
5. schedule `w1_therm.py` to run every x minutes using cron (e.g. `*/5 * * * * /opt/beastcraft-telemetry/w1_therm.py`)
6. go to [http://localhost:3000](http://localhost:3000), add a new datasource and configure other options
7. import BeastCraft.json dashboard and modify it to suit your needs

-- ab1
