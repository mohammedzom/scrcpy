#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path


def require_binary(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"ERROR: required command not found: {name}")
    return path


def command_supports(binary: str, option: str) -> bool:
    try:
        proc = subprocess.run(
            [binary, "--help"],
            capture_output=True,
            text=True,
            timeout=3.0,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return option in (proc.stdout + proc.stderr)


def adb_devices(adb: str, timeout: float = 3.0):
    try:
        proc = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return []

    devices = []
    for line in proc.stdout.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            devices.append((parts[0], parts[1]))
    return devices


def terminate_process(proc):
    if not proc or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=2)
    except subprocess.TimeoutExpired:
        proc.kill()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Assist legitimate recovery of an Android device with a broken/black "
            "screen by starting scrcpy OTG control and switching to normal scrcpy "
            "when ADB becomes authorized."
        )
    )
    parser.add_argument("--serial", help="USB/ADB serial to target when known")
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=1.0,
        help="Seconds between ADB checks (default: 1.0)",
    )
    parser.add_argument(
        "--no-otg",
        action="store_true",
        help="Only watch ADB; do not start scrcpy OTG",
    )
    parser.add_argument(
        "--no-accessibility-shortcut",
        action="store_true",
        help="Do not attempt the Volume Up + Volume Down accessibility shortcut",
    )
    parser.add_argument(
        "--otg-scrcpy",
        help=(
            "scrcpy binary to use for OTG. By default, use "
            "build-auto/app/scrcpy from this checkout when available, "
            "otherwise use scrcpy from PATH."
        ),
    )
    parser.add_argument(
        "scrcpy_args",
        nargs=argparse.REMAINDER,
        help="Extra arguments passed to normal scrcpy after ADB is ready",
    )
    args = parser.parse_args()

    scrcpy = require_binary("scrcpy")
    adb = require_binary("adb")

    repo_root = Path(__file__).resolve().parents[1]
    local_otg = repo_root / "build-auto" / "app" / "scrcpy"

    if args.otg_scrcpy:
        otg_scrcpy = args.otg_scrcpy
    elif local_otg.is_file():
        otg_scrcpy = str(local_otg)
    else:
        otg_scrcpy = scrcpy

    print("BlackScreen Rescue MVP")
    print("Use only on a device you own or are authorized to service.")
    print("This tool does not bypass PIN, pattern, password, FRP, or encryption.")
    print()

    otg = None
    if not args.no_otg:
        cmd = [otg_scrcpy, "--otg"]
        if args.serial:
            cmd += ["-s", args.serial]

        accessibility_option = "--accessibility-shortcut"
        if not args.no_accessibility_shortcut:
            if command_supports(otg_scrcpy, accessibility_option):
                cmd.append(accessibility_option)
                print(
                    "[1/3] Starting OTG control and attempting the "
                    "accessibility volume-key shortcut..."
                )
            else:
                print(
                    "[1/3] Starting OTG keyboard/mouse control. "
                    "This scrcpy build does not include automatic "
                    "accessibility-shortcut support."
                )
        else:
            print("[1/3] Starting OTG keyboard/mouse control...")

        otg = subprocess.Popen(cmd)
    else:
        print("[1/3] OTG start skipped.")

    print("[2/3] Waiting for ADB authorization...")
    last_state = None

    try:
        while True:
            devices = adb_devices(adb)

            if args.serial:
                devices = [d for d in devices if d[0] == args.serial]

            ready = next((d for d in devices if d[1] == "device"), None)
            unauthorized = next((d for d in devices if d[1] == "unauthorized"), None)

            if ready:
                serial = ready[0]
                print(f"[3/3] ADB ready: {serial}")
                terminate_process(otg)

                cmd = [scrcpy, "-s", serial]
                extra = args.scrcpy_args
                if extra and extra[0] == "--":
                    extra = extra[1:]
                cmd += extra

                print("Starting normal scrcpy mirroring...")
                return subprocess.call(cmd)

            state = "unauthorized" if unauthorized else "waiting"
            if state != last_state:
                if state == "unauthorized":
                    print(
                        "ADB detected but not authorized. Approve the RSA prompt "
                        "on the device using OTG input."
                    )
                else:
                    print(
                        "ADB is not available yet. Keep using OTG/TalkBack to "
                        "navigate your own device and enable USB debugging."
                    )
                last_state = state

            if otg and otg.poll() is not None:
                otg = None
                print(
                    "OTG window closed; continuing to watch ADB. "
                    "Restart this tool if you need OTG control again."
                )

            time.sleep(max(args.poll_interval, 0.2))

    except KeyboardInterrupt:
        print("\nCancelled.")
        terminate_process(otg)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
