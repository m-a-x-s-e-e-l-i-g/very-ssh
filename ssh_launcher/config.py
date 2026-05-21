import os

def parse_ssh_config():
    ssh_config_path = os.path.expanduser("~/.ssh/config")
    hosts = []

    if not os.path.exists(ssh_config_path):
        return hosts

    with open(ssh_config_path, "r") as config_file:
        for line in config_file:
            parts = line.lstrip().split()
            if len(parts) < 2 or parts[0] != "Host":
                continue

            host = parts[1]
            if "*" in host or "?" in host:
                continue

            hosts.append(host)

    return hosts
