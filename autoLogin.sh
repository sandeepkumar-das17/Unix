#!/usr/bin/expect

#This script will take you through the respective servers by logging into them.

spawn ssh <user_id>@<server-ip>

expect "yes/no" {
    send "yes\r"
    expect "Password" { send "<your-password>\r" }
    } "Password" { send "<your-password>\r" }
expect "$ " { send "ssh <second-level_server>\r" }
expect ": " { send "<your-password>\r" }
expect "$ " { send "sudo su - <user-id>\r" }
expect ": " { send "<your-password>\r" }
expect "$ " { send "TMOUT=\r" }

interact
