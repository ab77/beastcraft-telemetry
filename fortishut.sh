#!/usr/bin/expect -f
spawn ssh admin@10.10.1.254
send "exec shutdown\r"
expect "Do you want to continue? (y/n)"
send "y\r"
expect "System is shutting down..."
