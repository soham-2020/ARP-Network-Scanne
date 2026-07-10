"""
mock_simulator.py  –  NetSense Mock Network Simulator
======================================================
Simulates real-world device behaviour (connections, disconnections, wrong
Wi-Fi passwords) with timestamped event logging.

Previously this file was named "ml.model.py", which was misleading.
The ML/packet-classification component lives in the separate ml_classifier.py.

Run:
    python mock_simulator.py
"""

import time
import random
from datetime import datetime


# ---------------------------------------------------------------------------
# Mock device pool
# ---------------------------------------------------------------------------
# NOTE: All MAC addresses must use only valid hex digits (0-9, A-F).
#       The original had "00:1G:2B:3C:4D:5E" for Asus – 'G' is invalid hex.
SAMPLE_DEVICES = [
    {"IP": "192.168.1.2",  "MAC": "00:1A:2B:3C:4D:5E", "Vendor": "Apple"},
    {"IP": "192.168.1.3",  "MAC": "00:1B:2C:3D:4E:5F", "Vendor": "Samsung"},
    {"IP": "192.168.1.4",  "MAC": "00:1C:2D:3E:4F:5A", "Vendor": "Xiaomi"},
    {"IP": "192.168.1.5",  "MAC": "00:1D:2E:3F:4A:5B", "Vendor": "Dell"},
    {"IP": "192.168.1.6",  "MAC": "00:1E:2F:3A:4B:5C", "Vendor": "HP"},
    {"IP": "192.168.1.7",  "MAC": "00:1F:2A:3B:4C:5D", "Vendor": "Lenovo"},
    {"IP": "192.168.1.8",  "MAC": "00:1A:2B:4C:4D:5E", "Vendor": "Asus"},   # ← fixed: was 1G
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _ts() -> str:
    """Return a human-readable timestamp string for log lines."""
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def _log_event(event: str, ip: str, mac: str = "", vendor: str = "") -> None:
    """Print a timestamped event line."""
    extras = ""
    if mac:
        extras += f"  MAC: {mac}"
    if vendor:
        extras += f"  Vendor: {vendor}"
    print(f"{_ts()} {event}  IP: {ip}{extras}")


# ---------------------------------------------------------------------------
# Simulator
# ---------------------------------------------------------------------------
def run_simulator(
    scan_interval: float = 5.0,
    disconnect_chance: float = 0.30,
    wrong_pwd_chance: float = 0.20,
    max_new_attempts: int = 3,
    max_iterations: int | None = None,
) -> None:
    """
    Runs the mock network simulator.

    Args:
        scan_interval:     Seconds between each scan cycle.
        disconnect_chance: Probability (0-1) that a connected device drops each cycle.
        wrong_pwd_chance:  Probability (0-1) that a connecting device uses wrong password.
        max_new_attempts:  Maximum number of new connection attempts per cycle.
        max_iterations:    Stop after this many cycles (None = run forever; press Ctrl+C).
    """
    connected_devices: dict[str, dict] = {}
    iteration = 0

    print("📡 NetSense Mock Network Simulator")
    print("=" * 45)
    print(f"  Scan interval : {scan_interval}s")
    print(f"  Disconnect P  : {disconnect_chance:.0%}")
    print(f"  Wrong-pwd P   : {wrong_pwd_chance:.0%}")
    if max_iterations:
        print(f"  Max iterations: {max_iterations}")
    print("  Press Ctrl+C to stop.\n")

    try:
        while max_iterations is None or iteration < max_iterations:
            iteration += 1
            print(f"\n{'─' * 45}")
            print(f"📡 Scan cycle #{iteration}  {_ts()}")
            print(f"{'─' * 45}")

            # ── 1. Random disconnections ────────────────────────────────────
            if connected_devices and random.random() < disconnect_chance:
                ip_to_drop = random.choice(list(connected_devices.keys()))
                dropped = connected_devices.pop(ip_to_drop)
                _log_event("✗  DISCONNECTED", ip_to_drop, dropped["MAC"], dropped["Vendor"])

            # ── 2. Random new connection attempts ──────────────────────────
            attempt_count = random.randint(1, max(1, max_new_attempts))
            new_attempts = random.sample(SAMPLE_DEVICES, min(attempt_count, len(SAMPLE_DEVICES)))

            for device in new_attempts:
                ip, mac, vendor = device["IP"], device["MAC"], device["Vendor"]

                if ip in connected_devices:
                    _log_event("✓  ALREADY CONNECTED", ip, mac, vendor)
                    continue

                # Simulate wrong-password failure
                if random.random() < wrong_pwd_chance:
                    _log_event("⚠  WRONG Wi-Fi PASSWORD", ip, mac, vendor)
                else:
                    connected_devices[ip] = device
                    _log_event("✔  NEW DEVICE CONNECTED", ip, mac, vendor)

            # ── 3. Summary ─────────────────────────────────────────────────
            print(f"\n  Currently connected: {len(connected_devices)} device(s)")
            for dev_ip, dev in connected_devices.items():
                print(f"    • {dev_ip}  ({dev['MAC']})  [{dev['Vendor']}]")

            time.sleep(scan_interval)

    except KeyboardInterrupt:
        print("\n\n[Simulator stopped by user]")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_simulator()
