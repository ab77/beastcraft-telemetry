#!/usr/bin/env bash

# set initial datetime from GPS
influx -database beastcraft \
  --format csv \
  -execute 'SELECT last("value") FROM "time";' | \
  tail -1 | awk -F',' '{print $3}' | \
  xargs date +%Y-%m-%dT%H:%M:%S.000Z -s
