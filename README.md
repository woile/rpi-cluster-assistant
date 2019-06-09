# Raspberry Cluster Assistant

> Scripts to assist with the creation of a raspberry pi kubernetes cluster.

## About

This repository will help and guide you on setting up a cluster with multiple raspberries pi.

Currently it can generate a `master` and `N`-`workers` where `N` is the number of
nodes chosen in the `conf.json`.

It configures a DHCP server making the `master` node start assigning IPs to the worker nodes.
It is expected for the raspberries to be connected to the same switch.
The `eth0` interface should be reserved for the cluster.

The objective of this project is to make it easy to configure a cluster in order
to start playing with Kubernetes.

## Quickstart

```bash
git clone https://github.com/Woile/rpi-cluster-assistant.git
cd rpi-cluster-assistant/
```

```bash
./scripts/init
./scripts/flash-cluster
```

## Features

- Access using `SSH` to the nodes.
- DHCP Server and `master` node with static IP `10.0.0.1`
- Range of IPs assigned to nodes goes from `10.0.0.2` to `10.0.0.50`
- All the nodes have access to wifi. This might be useful later to play with multi-master nodes.
- Provision a `kubernetes` cluster
- Support for multiple pod networks: `flannel`, `weavenet`
- Include kubernetes addons, currently only dashboard.
- Prompt asking for the configuration of the cluster.

## Prerequisites

- Linux Debian based OS.

## Usage

### 1. Initialization

**Execute**:

```bash
./scripts/init
```

**Explanation**:

1. Installs OS dependencies (debian) in your machine (the host).
1. Downloads `Hypriot OS` and `flash`.
1. Create 'conf.json' using the assistant if file is not present.

### 2. Flash to SD cards

**Before**:

- Update `config.json` values.

**Execute**:

```bash
./scripts/flash-cluster
```

**Explanation**:

1. Show information of what is going to happen and ask for confirmation.
1. Render cluster files.
1. If master node is true, it will be the first to be flashed.
1. The worker nodes will be flashed.

### Extras

### Assistant

**Execute**:

```bash
./scripts/assistant.py
```

**Explanation**:

1. Questions about the cluster are prompted.
1. A `conf.json` file is generated.

### Flash one

**Before**:

- Update `config.json` values.

**Execute**:

```bash
./scripts/flash-one
```

**Explanation**:

1. Prompt the user for some information.
1. Render cluster files.
1. Flash one SD card based on the node type (`master` or `worker`) chosen.

### Render template

**Before**:

- Update the values in `conf.json`.
- Use the raw wifi password because it will be automatically converted using `wpa_passphrase`.
- If you don't have a ssh key, create one using [this tutorial][ssh_tutorial].

**Execute**:

```bash
./scripts/render.py
```

**Explanation**:

1. Reads information from `conf.json`.
1. Creates files for Raspberry cluster inside `output` folder.

### Configuration

The configuration file can be created based on the `conf.example.json`

```bash
cp conf.example.json conf.json
```

All the values are required, if you don't know what to put, leave the default.

| Variable           | Description                                                                  | Default             |
| ------------------ | ---------------------------------------------------------------------------- | ------------------- |
| `username`         | The username used to log in to the node                                      | `hypriot`           |
| `wifi_ssid_name`   | The name of your wifi                                                        | -                   |
| `wifi_password`    | Raw password of your wifi                                                    | -                   |
| `wifi_country`     | Country where you are, [check the codes][wifi_codes]                         | `NL`                |
| `ssh_public_key`   | Public [SSH Key][ssh_tutorial] to access from outside the nodes              | `~/.ssh/id_rsa.pub` |
| `hostname_prefix`  | Name of the machine. It will look like: `node-1`                             | `node`              |
| `number_of_nodes`  | Number of raspberries to be flashed                                          | `4`                 |
| `node_range_start` | Offset to the number of nodes. Example range: `[5..8]` with range start: `5` | `1`                 |
| `include_master`   | Decide whether to flash a `master` node or only workers.                     | `true`              |
| `pod_network`      | [Pod Network][pod_network]. Options: `weavenet`, `flannel`                   | `flannel`           |

### Provisioning kubernetes cluster

#### Master node

1. As root follow the steps located in `/root/k8s-cluster`.
1. As normal user follow the steps located in `/home/<user>/k8s-config`

**Notes**:

- Observe the output located in `/root/k8s-cluster/kubeadm-init.out` because you will
- have to run the `kubeadm join ...` after provisioning the worker nodes.

#### Worker nodes

Remember that this must be executed after running all the scripts above

1. As root follow the steps located in `/root/k8s-cluster`.
1. Run `kubeadm join ...` command which appears in the master node.

#### Finally

You can run the [addons][k8s_addons] included in `/home/<user>/k8s-addons`.

[ssh_tutorial]: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
[wifi_codes]: https://github.com/recalbox/recalbox-os/wiki/Wifi-country-code-(EN)
[pod_network]: https://kubernetes.io/docs/concepts/cluster-administration/addons/#networking-and-network-policy
[k8s_addons]: https://kubernetes.io/docs/concepts/cluster-administration/addons/
