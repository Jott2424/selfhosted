#!/usr/bin/env python3
"""
Cross-platform deploy orchestrator. Run from Windows, Mac, or Linux —
identical usage everywhere, no Ansible/control-node required.

Configures one or more VMs by copying the matching setup_*.py script over
and running it with sudo. Waits for SSH to come up first, so it's safe to
run right after starting a VM.

Usage:
    python3 deploy.py postgres
    python3 deploy.py pokemon-simulations
    python3 deploy.py all
    python3 deploy.py postgres --key /path/to/key

The SSH private key path is resolved from, in order:
    --key <path>
    PROXMOX_VMS_SSH_KEY environment variable
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

HOSTS = {
    "postgres": {
        "ip": "192.168.1.226",
        "user": "ubuntu",
        "script": "setup_postgres.py",
    },
    "pokemon-simulations": {
        "ip": "192.168.1.227",
        "user": "ubuntu",
        "script": "setup_pokemon_simulations.py",
    },
}


def resolve_key(cli_key):
    key = cli_key or os.environ.get("PROXMOX_VMS_SSH_KEY")
    if not key:
        sys.exit(
            "No SSH key given. Pass --key <path> or set the "
            "PROXMOX_VMS_SSH_KEY environment variable."
        )
    key = str(Path(key).expanduser())
    if not Path(key).is_file():
        sys.exit(f"SSH key not found: {key}")
    return key


def ssh_base(key, user, ip):
    return ["ssh", "-i", key, "-o", "StrictHostKeyChecking=accept-new", f"{user}@{ip}"]


def wait_for_ssh(key, user, ip, timeout=120):
    print(f"Waiting for SSH on {ip}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = subprocess.run(
            ssh_base(key, user, ip)
            + ["-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "echo ok"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"{ip} is reachable.")
            return
        time.sleep(5)
    sys.exit(f"Timed out waiting for SSH on {ip}")


def deploy_host(name, cfg, key):
    ip, user, script = cfg["ip"], cfg["user"], cfg["script"]
    local_script = SCRIPT_DIR / script
    if not local_script.is_file():
        sys.exit(f"Missing local script: {local_script}")

    print(f"\n=== {name} ({ip}) ===")
    wait_for_ssh(key, user, ip)

    print(f"Copying {script}...")
    subprocess.run(
        ["scp", "-i", key, str(local_script), f"{user}@{ip}:~/"], check=True
    )

    print(f"Running {script} (sudo)...")
    # -t forces a pty so sudo/getpass prompts work interactively over SSH.
    subprocess.run(
        ssh_base(key, user, ip) + ["-t", f"sudo python3 {script}"], check=True
    )


def main():
    parser = argparse.ArgumentParser(description="Deploy config to proxmox-vms hosts")
    parser.add_argument(
        "target", choices=[*HOSTS.keys(), "all"], help="Which host to configure"
    )
    parser.add_argument("--key", help="Path to SSH private key")
    args = parser.parse_args()

    key = resolve_key(args.key)
    targets = HOSTS.keys() if args.target == "all" else [args.target]

    for name in targets:
        deploy_host(name, HOSTS[name], key)

    print("\nDone.")


if __name__ == "__main__":
    main()
