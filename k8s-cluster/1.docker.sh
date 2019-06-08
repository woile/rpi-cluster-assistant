#!/bin/bash
# Install and hold docker to the latest tested version

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt update
apt -y install docker-ce=18.06.3~ce~3-0~raspbian --allow-downgrades
apt-mark hold docker-ce
