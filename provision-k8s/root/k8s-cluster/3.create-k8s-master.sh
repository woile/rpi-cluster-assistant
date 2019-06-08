#!/bin/bash
# Create a new kubernetes cluster
# Pod Network supported: flannel, weavenet

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


POD_NETWORK=${POD_NETWORK:-flannel}

printf "Creating kubernetes cluster\n"
printf "Target pod network: %s\n" $POD_NETWORK

if [ $POD_NETWORK == "flannel" ]; then

  kubeadm init --kubernetes-version 1.14.1 \
      --pod-network-cidr 10.244.0.0/16 \
      --apiserver-advertise-address=10.0.0.1 | tee kubeadm-init.out

elif [ $POD_NETWORK == "weavenet" ]; then

  kubeadm init --kubernetes-version 1.14.1 \
      --apiserver-advertise-address=10.0.0.1 | tee kubeadm-init.out

fi