#!/usr/bin/env python3
"""
Run this ON the postgres VM (192.168.1.226) as root:

    sudo python3 setup_postgres.py

Installs PostgreSQL, opens it to the LAN, and sets the postgres
superuser's password (prompted interactively, never stored on disk).
"""

import getpass
import glob
import os
import re
import subprocess
import sys

ALLOWED_SUBNET = "192.168.1.0/24"


def run(cmd, **kwargs):
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def main():
    if os.geteuid() != 0:
        sys.exit("Run this as root: sudo python3 setup_postgres.py")

    run(["apt-get", "update"])
    run(["apt-get", "install", "-y", "postgresql", "postgresql-contrib"])

    conf_matches = glob.glob("/etc/postgresql/*/main/postgresql.conf")
    hba_matches = glob.glob("/etc/postgresql/*/main/pg_hba.conf")
    if not conf_matches or not hba_matches:
        sys.exit("Could not locate postgresql.conf / pg_hba.conf under /etc/postgresql")
    conf_path, hba_path = conf_matches[0], hba_matches[0]

    with open(conf_path) as f:
        conf = f.read()
    conf, n = re.subn(
        r"^#?\s*listen_addresses\s*=.*$",
        "listen_addresses = '*'",
        conf,
        flags=re.MULTILINE,
    )
    if n == 0:
        conf += "\nlisten_addresses = '*'\n"
    with open(conf_path, "w") as f:
        f.write(conf)

    hba_line = f"host all all {ALLOWED_SUBNET} scram-sha-256\n"
    with open(hba_path) as f:
        existing = f.read()
    if hba_line not in existing:
        with open(hba_path, "a") as f:
            f.write(hba_line)

    run(["systemctl", "enable", "--now", "postgresql"])
    run(["systemctl", "restart", "postgresql"])

    password = getpass.getpass("Set password for the postgres superuser: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        sys.exit("Passwords did not match, aborting.")

    subprocess.run(
        ["sudo", "-u", "postgres", "psql"],
        input=f"ALTER USER postgres PASSWORD '{password}';\n",
        text=True,
        check=True,
    )

    print(f"\nPostgreSQL installed and listening on all interfaces, open to {ALLOWED_SUBNET}.")


if __name__ == "__main__":
    main()
