#!/usr/bin/env python3
"""
Full pipeline, cross-platform (Windows/Mac/Linux):

    terraform apply  ->  VMs autostart  ->  wait for SSH  ->  configure both

Usage:
    python3 redeploy.py --key /path/to/key
    python3 redeploy.py --key /path/to/key --skip-terraform   # just reconfigure, don't touch infra
    python3 redeploy.py --key /path/to/key --target postgres  # only one host
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))
from deploy import HOSTS, deploy_host, resolve_key  # noqa: E402


def terraform_apply():
    print("=== terraform apply ===")
    subprocess.run(
        ["terraform", "apply", "-auto-approve"], cwd=PROJECT_ROOT, check=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="terraform apply, then configure the VMs it creates/updates"
    )
    parser.add_argument("--key", help="Path to SSH private key")
    parser.add_argument(
        "--target",
        choices=[*HOSTS.keys(), "all"],
        default="all",
        help="Which host(s) to configure (default: all)",
    )
    parser.add_argument(
        "--skip-terraform",
        action="store_true",
        help="Skip terraform apply, just (re)configure the VMs",
    )
    args = parser.parse_args()

    key = resolve_key(args.key)

    if not args.skip_terraform:
        terraform_apply()

    targets = HOSTS.keys() if args.target == "all" else [args.target]
    for name in targets:
        deploy_host(name, HOSTS[name], key)

    print("\nAll done.")


if __name__ == "__main__":
    main()
