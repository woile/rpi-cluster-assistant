#!/bin/bash
# Attention!!
# Only run flannel or weavenet not both!!

if [ "$EUID" -ne 1000 ];then
    echo "Please run as user: $(id -un 1000)"
    exit
fi

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/62e44c867a2846fefb68bd5f178daf4da3095ccb/Documentation/kube-flannel.yml
