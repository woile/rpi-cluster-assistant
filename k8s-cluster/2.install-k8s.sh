#!/bin/bash
# Install and hold kubernetes to the latest tested version

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt update
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
apt update
apt install -y kubeadm=1.14.1-00 kubelet=1.14.1-00 kubectl=1.14.1-00 --allow-downgrades
apt-mark hold kubeadm kubelet kubectl
