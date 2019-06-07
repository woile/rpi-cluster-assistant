# Raspberry Cluster Assistant

> Scripts to assist with the creation of a raspberry pi cluster.

## About

This repository will help and guide you on setting up a cluster with multiple raspberries pi.

Currently it can generate a `master` and `N`-`workers` where `N` is the number of nodes chosen in the `conf.json`.

Also it configures a DHCP server making the `master` node start assigning IPs to the worker nodes.
It is expected for the raspberries to be connected to the same switch. The `eth0` interface should be
for the cluster.

The objective of this project is to make it easy to configure a cluster in order
to start playing with Kubernetes.

## Features

- Access using `SSH`
- DHCP Server and `master` node with static IP `10.0.0.1`
- Range of IPs assigned to nodes goes from `10.0.0.2` to `10.0.0.50`
- All the nodes have access to wifi. This might be useful later to play with multi-master nodes
- Includes a series of scripts in `/root` to configure `docker`, `kubernetes` and a pod network.

## Prerequisites

- Linux Debian based OS.

## Usage

### 1. Initialization

```bash
./scripts/init
```

1. Installs OS dependencies (debian) in your machine (the host)
2. Downloads Hypriot OS and `flash`.
3. Creates `conf.json` based on `conf.example.json`.

### 2. Render template

**Before**:

- Update the values in `conf.json`.
- Use the raw wifi password because it will be automatically converted using `wpa_passphrase`.
- If you don't have a ssh key, create one using [this tutorial][ssh_tutorial].

```bash
./scripts/render
```

1. Reads information from `conf.json`.
2. Creates files for Raspberry cluster inside `output` folder.

### 3. Flash to SD cards

**Before**:

- Update `config.json` values
- Run `./scripts/render`

```bash
./scripts/flash-cluster
```

Follow instructions prompted

### Extras

### Flash one

This script will prompt the user for some information and
will only flash one SD card based on the template chosen.

```bash
./scripts/flash-one
```

### Configuration

The configuration file can be created based on the `conf.example.json`

```bash
cp conf.example.json conf.json
```

All the values are required, if you don't know what to put, leave the default.

| Variable           | Description                                                                  | Default                  |
| ------------------ | ---------------------------------------------------------------------------- | ------------------------ |
| `username`         | The username used to log in to the node                                      | `hypriot,`               |
| `wifi_ssid_name`   | The name of your wifi                                                        | `My Wifi Name,`          |
| `wifi_password`    | Raw password of your wifi                                                    | `longandsecurepassword,` |
| `wifi_country`     | Country where you are, [check the codes][wifi_codes]                         | `NL,`                    |
| `ssh_public_key`   | Public [SSH Key][ssh_tutorial] to access from outside the nodes              | `~/.ssh/id_rsa.pub,`     |
| `hostname_prefix`  | Name of the machine. It will look like: `node-1`                             | `node,`                  |
| `number_of_nodes`  | Number of raspberries to be flashed                                          | `4,`                     |
| `node_range_start` | Offset to the number of nodes. Example range: `[5..8]` with range start: `5` | `1,`                     |
| `include_master`   | Decide whether to flash a `master` node or only workers.                     | `true`                   |

[ssh_tutorial]: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
[wifi_codes]: https://github.com/recalbox/recalbox-os/wiki/Wifi-country-code-(EN)
