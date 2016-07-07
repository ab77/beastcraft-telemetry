#!/usr/bin/env bash

printf "enabling mobile network...\n"
curl 'http://dash.beastcraft.belodedenko.me/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=CONNECT_NETWORK'

printf "\nstarting link-monitor...\n"
printf "conf sys link-monitor\nedit wan2\nset status enable\nend\n" \ |
  ssh admin@beastgate2.beastcraft.belodedenko.me

printf "starting fgmon service...\n"
supervisorctl start fgmon
