#!/usr/bin/env python3
import os
import json
import base64
import urllib.request

from string import Template
from typing import List

TEMPLATE_MASTER = "templates/cloud-init-config-template.master.yml"
OUTPUT_MASTER = "output/cloud-init-config.master.yaml"

TEMPLATE_WORKER = "templates/cloud-init-config-template.worker.yml"
OUTPUT_WORKER = "output/cloud-init-config.worker.yaml"

MASTER_FILES = [
    "k8s-cluster/1.docker.sh",
    "k8s-cluster/2.install-k8s.sh",
    "k8s-cluster/3.create-k8s-master.sh",
    "k8s-cluster/4.get-flannel.sh",
]


WORKER_FILES = ["k8s-cluster/1.docker.sh", "k8s-cluster/2.install-k8s.sh"]


with urllib.request.urlopen("https://ipapi.co/timezone") as response:
    TIMEZONE = response.read().decode()

with open("./conf.json", "r") as f:
    config = json.load(f)


def generate_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        encoded_content = base64.b64encode(f.read())
    return f"""
  - content: "{encoded_content.decode()}"
    encoding: b64
    path: /root/{file_path}
    permissions: '0755'
    """


def create_config(input_file: str, output_file: str, cluster_scripts: List[str]):

    ssh_location = config["ssh_public_key"]

    with open(os.path.expanduser(ssh_location), "r") as f:
        ssh_public = f.read()

    write_files = "".join([generate_base64(filepath) for filepath in cluster_scripts])

    variables = {
        "USERNAME": config["username"],
        "WIFI_SSID_NAME": config["wifi_ssid_name"],
        "WIFI_PASSWORD": config["wifi_password"],
        "WIFI_COUNTRY": config["wifi_country"],
        "SSH_PUBLIC_KEY": ssh_public,
        "WRITE_FILES": write_files,
        "TIMEZONE": TIMEZONE,
    }
    with open(input_file, "r") as f:
        src = Template(f.read())
        with open(output_file, "w") as g:
            g.write(src.safe_substitute(variables))


create_config(TEMPLATE_MASTER, OUTPUT_MASTER, MASTER_FILES)
create_config(TEMPLATE_WORKER, OUTPUT_WORKER, WORKER_FILES)
