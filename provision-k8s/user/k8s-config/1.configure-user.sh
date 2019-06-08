#!/bin/bash

if [ "$EUID" -ne 1000 ];then
    echo "Please run as user: $(id -un 1000)"
    exit
fi

printf "Actions:\n\n"
printf "1. Configure kubectl.\n"
printf "2. Add autocomplete for kubectl.\n"

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo "source <(kubectl completion bash)" >> ~/.bashrc

printf "Done.\n"
