#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import re
import sys


def video_has_valid_stream(video_dev: str,
                           min_width=3000,
                           min_height=2000) -> bool:
    """
    Check whether a /dev/videoX supports a high-resolution video stream.
    Used to distinguish the real GelSight stream from control/empty nodes.
    """
    try:
        out = subprocess.check_output(
            ["v4l2-ctl", "--device", video_dev, "--list-formats-ext"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return False

    # Look for resolutions like: 3280x2464
    matches = re.findall(r"Size:\s+Discrete\s+(\d+)x(\d+)", out)
    for w, h in matches:
        if int(w) >= min_width and int(h) >= min_height:
            return True

    return False


def resolve_gelsight_device(target_name: str) -> str:
    """
    Resolve the correct /dev/videoX for a given GelSight device name.
    """
    video_root = "/sys/class/video4linux"
    candidates = []

    # Stage 1: match device name exactly
    for entry in os.listdir(video_root):
        if not entry.startswith("video"):
            continue

        name_path = os.path.join(video_root, entry, "name")
        try:
            with open(name_path, "r") as f:
                name = f.read().strip()
        except OSError:
            continue

        if name == target_name:
            candidates.append(f"/dev/{entry}")

    if not candidates:
        raise RuntimeError(
            f"[ERROR] No video devices found with name '{target_name}'. "
            f"Is the GelSight connected?"
        )

    # Stage 2: select the real streaming node
    for video_dev in candidates:
        if video_has_valid_stream(video_dev):
            return video_dev

    raise RuntimeError(
        f"[ERROR] Found devices {candidates} for '{target_name}', "
        f"but none expose a valid video stream."
    )


def main():
    """
    Simple test entrypoint.
    """

    # 👇 你现在系统里的两只 GelSight
    gelsight_names = [
        "GelSight Mini R0B 2DDZ-43PB: Ge",
        "GelSight Mini R0B 2DE9-0HLG: Ge",
    ]

    print("=== GelSight device resolution test ===\n")

    for name in gelsight_names:
        print(f"[INFO] Resolving device for: {name}")
        try:
            video_dev = resolve_gelsight_device(name)
            print(f"  ✅ Found stream device: {video_dev}\n")
        except RuntimeError as e:
            print(f"  ❌ {e}\n")

    print("=== Test finished ===")


if __name__ == "__main__":
    main()
