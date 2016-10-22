#!/usr/bin/expect -f
spawn ssh admin@beastgate2
send "exec shutdown\r"
expect "Do you want to continue? (y/n)"
send "y\r"
expect "System is shutting down..."
