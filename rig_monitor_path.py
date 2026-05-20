#!/usr/bin/env python3
"""
rig_monitor_path.py

Reads Open Hardware Monitor / LibreHardwareMonitor style JSON from data.json
and extracts sensors by full path so duplicate names like "GPU Core" do not collide.

Edit the SENSOR_PATHS section if your device names differ.
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

import requests


# Change this if your monitoring URL changes.
MONITOR_URL = "http://100.124.119.95:8085/data.json"


# Paths are matched by the "Text" fields inside the JSON tree.
# IMPORTANT:
# If your machine/GPU name differs, edit these labels to match data.json exactly.
SENSOR_PATHS = {
    "cpu_temp": [
        "DESKTOP-RCGEMTO",
        "Intel Core Ultra 7 265K",
        "Temperatures",
        "CPU Core",
    ],
    "cpu_package_power": [
        "DESKTOP-RCGEMTO",
        "Intel Core Ultra 7 265K",
        "Powers",
        "CPU Package",
    ],
    "gpu_temp": [
        "DESKTOP-RCGEMTO",
        "NVIDIA NVIDIA GeForce RTX 5070 Ti",
        "Temperatures",
        "GPU Core",
    ],
    "gpu_package_power": [
        "DESKTOP-RCGEMTO",
        "NVIDIA NVIDIA GeForce RTX 5070 Ti",
        "Powers",
        "GPU Package",
    ],
}


def find_child_by_text(node: dict[str, Any], text: str) -> Optional[dict[str, Any]]:
    """Return the first direct child whose Text exactly matches text."""
    for child in node.get("Children", []):
        if child.get("Text") == text:
            return child
    return None


def find_sensor_by_path(root: dict[str, Any], path: list[str]) -> Optional[str]:
    """
    Walk the JSON tree by exact Text labels and return the final node's Value.

    Example path:
    ["DESKTOP-RCGEMTO", "Intel Core Ultra 7 265K", "Temperatures", "CPU Core"]
    """
    current = root

    for label in path:
        current = find_child_by_text(current, label)
        if current is None:
            return None

    return current.get("Value")


def fetch_data() -> dict[str, Any]:
    response = requests.get(MONITOR_URL, timeout=10)
    response.raise_for_status()
    return response.json()


def main() -> None:
    data = fetch_data()

    metrics = {
        name: find_sensor_by_path(data, path)
        for name, path in SENSOR_PATHS.items()
    }

    print(f"Time: {datetime.now().isoformat(timespec='seconds')}")
    print(json.dumps(metrics, indent=2))

    # Human-readable version
    print()
    print("System Snapshot")
    print("----------------")
    print(f"CPU Temp:          {metrics['cpu_temp']}")
    print(f"CPU Package Power: {metrics['cpu_package_power']}")
    print(f"GPU Temp:          {metrics['gpu_temp']}")
    print(f"GPU Package Power: {metrics['gpu_package_power']}")


if __name__ == "__main__":
    main()
