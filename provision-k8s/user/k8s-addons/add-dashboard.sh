#!/bin/bash

# Apply dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/be4f2813b7cc13f682f2af5025d42813c8e7fbd3/aio/deploy/recommended/kubernetes-dashboard-arm.yaml

# Configure access
kubectl create serviceaccount dashboard -n default
kubectl create clusterrolebinding dashboard-admin -n default \
  --clusterrole=cluster-admin \
  --serviceaccount=default:dashboard
