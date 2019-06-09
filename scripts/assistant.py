#!/usr/bin/env python3
import json
from pathlib import Path
from getpass import getpass
from typing import Dict
from distutils.util import strtobool


def load_conf() -> Dict:
    conf_path = Path("conf.json")
    if not conf_path.is_file():
        conf_path = Path("conf.example.json")
    with conf_path.open() as f:
        conf = json.load(f)
    return conf


conf = load_conf()
username: str = (
    input(f"Username of the host machines [{conf['username']}]:\n") or conf["username"]
)
wifi_ssid_name: str = input(
    f"\nWiFi network name [{conf['wifi_ssid_name']}]:\n"
) or conf["wifi_ssid_name"]

wifi_password: str = getpass(
    f"\nWiFi password [{'*' * len(conf['wifi_password'])}]:\n"
) or conf["wifi_password"]

print(f"\nCountry code of your wifi [{conf['wifi_country']}]")
print(
    "More info: https://github.com/recalbox/recalbox-os/wiki/Wifi-country-code-%28EN%29"
)
wifi_country: str = input() or conf["wifi_country"]

print(f"\nSSH Public key path [{conf['ssh_public_key']}]")
print("Used to access to the nodes through the local network")
print(
    "Create a new one: "
    "https://help.github.com/en/articles/generating-a-new-ssh-key-"
    "and-adding-it-to-the-ssh-agent"
)
ssh_public_key: str = input() or conf["ssh_public_key"]

print(f"\nHostname prefix for the nodes [{conf['hostname_prefix']}]")
print(
    f"Your hostnames will look like: "
    f"{conf['hostname_prefix']}-1 {conf['hostname_prefix']}-2"
)
hostname_prefix: str = input() or conf["hostname_prefix"]

print(f"\nNumber of machines [{conf['number_of_nodes']}]")
print("Or in other words, the number of raspberries you have")
number_of_nodes: int = int(input() or conf["number_of_nodes"])

print(f"\nInclude a k8s master ready node? [Y]/n")
include_master: bool = bool(strtobool(input() or "y"))

print(f"\nNode range beginning [{conf['node_range_start']}]")
print(
    "Offset applied to the number of nodes, let's say you have 4 nodes\n"
    "and you already have 3 machines, if you set the offset to 3\n"
    "the newely created nodes will have this range: [4..7]"
)
node_range_start: int = int(input() or conf["node_range_start"])

print(f"Pod network [{conf['pod_network']}]")
print("Used as the underlying layer for the pods to communicate across machines")
print("Choices: flannel, weavenet")
pod_network: str = input() or conf["pod_network"]

conf.update(
    {
        "username": username,
        "wifi_ssid_name": wifi_ssid_name,
        "wifi_password": wifi_password,
        "wifi_country": wifi_country,
        "ssh_public_key": ssh_public_key,
        "hostname_prefix": hostname_prefix,
        "number_of_nodes": number_of_nodes,
        "include_master": include_master,
        "node_range_start": node_range_start,
        "pod_network": pod_network,
    }
)

with Path("conf.json").open("w") as f:
    json.dump(conf, f, indent=2)

print("New configuration created!")
print("This file is not being tracked by git.")
print("Location './conf.json'")
