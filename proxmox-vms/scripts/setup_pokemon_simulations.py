#!/usr/bin/env python3
"""
Run this ON the pokemon-simulations VM (192.168.1.227) as root:

    sudo python3 setup_pokemon_simulations.py

Installs Python3 + build tools and creates a venv at /opt/pokemon-sim/venv
with numpy, pandas, and psycopg2-binary.
"""

import os
import subprocess
import sys

VENV_PATH = "/opt/pokemon-sim/venv"
PIP_PACKAGES = ["numpy", "pandas", "psycopg2-binary"]
APP_USER = "ubuntu"


def run(cmd, **kwargs):
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kwargs)


def main():
    if os.geteuid() != 0:
        sys.exit("Run this as root: sudo python3 setup_pokemon_simulations.py")

    run(["apt-get", "update"])
    run(
        [
            "apt-get",
            "install",
            "-y",
            "python3",
            "python3-venv",
            "python3-pip",
            "build-essential",
            "libpq-dev",
            "git",
        ]
    )

    app_dir = os.path.dirname(VENV_PATH)
    run(["mkdir", "-p", app_dir])
    run(["chown", f"{APP_USER}:{APP_USER}", app_dir])

    if not os.path.exists(os.path.join(VENV_PATH, "bin", "activate")):
        run(["sudo", "-u", APP_USER, "python3", "-m", "venv", VENV_PATH])

    run(
        ["sudo", "-u", APP_USER, f"{VENV_PATH}/bin/pip", "install", "--upgrade", "pip"]
    )
    run(["sudo", "-u", APP_USER, f"{VENV_PATH}/bin/pip", "install", *PIP_PACKAGES])

    print(f"\nDone. Activate with: source {VENV_PATH}/bin/activate")


if __name__ == "__main__":
    main()
