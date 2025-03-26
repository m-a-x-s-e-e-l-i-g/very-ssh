import os
import re

def parse_ssh_config():
    ssh_config_path = os.path.expanduser("~/.ssh/config")
    hosts = []
    if os.path.exists(ssh_config_path):
        with open(ssh_config_path, "r") as f:
            content = f.read()
            hosts = re.findall(r"^\s*Host\s+([^\s*?]+)", content, re.MULTILINE)
    return hosts
