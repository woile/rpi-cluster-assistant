#!/bin/bash
# Create a new kubernetes cluster
# Pod Network supported: flannel

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

kubeadm init --kubernetes-version 1.14.1 \
    --pod-network-cidr 10.244.0.0/16 \
    --apiserver-advertise-address=10.0.0.1 | tee kubeadm-init.out
