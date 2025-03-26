from .config import parse_ssh_config
from .theme import is_light_mode
from .ui import launch_gui

def main():
    hosts = parse_ssh_config()
    mode = is_light_mode()
    launch_gui(hosts, mode)

if __name__ == "__main__":
    main()
