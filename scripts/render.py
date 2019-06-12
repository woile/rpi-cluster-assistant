#!/usr/bin/env python3
import os
import sys
import json
import base64
import subprocess
import urllib.request

from string import Template
from typing import List

TEMPLATE_MASTER = "templates/cloud-init-config-template.master.yml"
OUTPUT_MASTER = "output/cloud-init-config.master.yaml"

TEMPLATE_WORKER = "templates/cloud-init-config-template.worker.yml"
OUTPUT_WORKER = "output/cloud-init-config.worker.yaml"

MASTER_FILES = [
    "provision-k8s/root/k8s-cluster/1.docker.sh",
    "provision-k8s/root/k8s-cluster/2.install-k8s.sh",
    "provision-k8s/root/k8s-cluster/3.create-k8s-master.sh",
    "provision-k8s/user/k8s-config/1.configure-user.sh",
    "provision-k8s/user/k8s-config/2.add-flannel-pod-network.sh",
    "provision-k8s/user/k8s-config/2.add-weavenet-pod-network.sh",
    "provision-k8s/user/k8s-addons/add-dashboard.sh",
    "provision-k8s/user/k8s-utils/get-dashboard-token.sh",
]

WORKER_FILES = [
    "provision-k8s/root/k8s-cluster/1.docker.sh",
    "provision-k8s/root/k8s-cluster/2.install-k8s.sh",
]


with urllib.request.urlopen("https://ipapi.co/timezone") as response:
    TIMEZONE = response.read().decode()

with open("./conf.json", "r") as f:
    config = json.load(f)


def filter_pod_network(value: str, pod_network: str) -> bool:
    if "pod-network" in value:
        return pod_network in value
    return True


def generate_base64(file_path: str, username: str) -> str:
    with open(file_path, "rb") as f:
        encoded_content = base64.b64encode(f.read())
    node_file_path = file_path.replace("provision-k8s", "").replace(
        "user", f"home/{username}"
    )
    return f"""
  - encoding: b64
    content: {encoded_content.decode()}
    path: {node_file_path}
    permissions: '0755'"""


def get_wpa_passphrase(wifi_name: str, wifi_password: str) -> str:
    cmd = f"wpa_passphrase {wifi_name} {wifi_password}"
    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if stderr:
        sys.exit()
    out = stdout.decode().split()[3]
    return out


def create_config(input_file: str, output_file: str, cluster_scripts: List[str]):

    ssh_location = config["ssh_public_key"]

    with open(os.path.expanduser(ssh_location), "r") as f:
        ssh_public = f.read()
    username = config["username"]
    pod_network = config["pod_network"]
    cluster_scripts = list(filter(
        lambda value: filter_pod_network(value, pod_network), cluster_scripts
    ))

    write_files = "".join(
        [generate_base64(filepath, username) for filepath in cluster_scripts]
    )
    wifi_passphrase = get_wpa_passphrase(
        config["wifi_ssid_name"], config["wifi_password"]
    )
    variables = {
        "USERNAME": username,
        "WIFI_SSID_NAME": config["wifi_ssid_name"],
        "WIFI_PASSWORD": wifi_passphrase,
        "WIFI_COUNTRY": config["wifi_country"],
        "SSH_PUBLIC_KEY": ssh_public,
        "WRITE_FILES": write_files,
        "TIMEZONE": TIMEZONE,
    }
    with open(input_file, "r") as f:
        src = Template(f.read())
        file_path = os.path.dirname(output_file)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(output_file, "w") as g:
            g.write(src.safe_substitute(variables))


create_config(TEMPLATE_MASTER, OUTPUT_MASTER, MASTER_FILES)
create_config(TEMPLATE_WORKER, OUTPUT_WORKER, WORKER_FILES)
