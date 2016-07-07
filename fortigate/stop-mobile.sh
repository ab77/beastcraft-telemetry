#!/usr/bin/env bash

printf "stopping link-monitor...\n"
printf "conf sys link-monitor\nedit wan2\nset status disable\nend\n" \ |
  ssh admin@beastgate2.beastcraft.belodedenko.me

printf "diabling mobile network...\n"
curl 'http://dash.beastcraft.belodedenko.me/goform/goform_set_cmd_process?isTest=false&notCallback=true&goformId=DISCONNECT_NETWORK'

printf "\nstopping fgmon service...\n"
supervisorctl stop fgmon
