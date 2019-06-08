#!/bin/bash
# Attention!!
# Only run flannel or weavenet not both!!

if [ "$EUID" -ne 1000 ];then
    echo "Please run as user: $(id -un 1000)"
    exit
fi

kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
