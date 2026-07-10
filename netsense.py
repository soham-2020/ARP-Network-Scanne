"""
netsense.py  –  NetSense Unified Entry Point
=============================================
Run all three modules from a single CLI.

Usage:
    python netsense.py scan        # ARP Network Scanner
    python netsense.py simulate    # Mock Network Simulator
    python netsense.py ml          # ML Packet Classifier
    python netsense.py all         # Run all three sequentially
    python netsense.py --help      # Show help
"""

import sys


def run_scan():
    from network_scanner import dynamic_network_scanner_main
    dynamic_network_scanner_main()


def run_simulate():
    from mock_simulator import run_simulator
    run_simulator()


def run_ml():
    from ml_classifier import main as ml_main
    ml_main()


COMMANDS = {
    "scan":     (run_scan,     "ARP Network Scanner"),
    "simulate": (run_simulate, "Mock Network Simulator"),
    "ml":       (run_ml,       "ML Packet Classifier"),
}


def print_help():
    print(__doc__)
    print("Available commands:")
    for cmd, (_, desc) in COMMANDS.items():
        print(f"  {cmd:<12} {desc}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "all":
        for name, (fn, desc) in COMMANDS.items():
            print(f"\n{'═' * 50}")
            print(f"  Running: {desc}")
            print(f"{'═' * 50}\n")
            fn()
        return

    if cmd not in COMMANDS:
        print(f"Unknown command: '{cmd}'")
        print_help()
        sys.exit(1)

    COMMANDS[cmd][0]()


if __name__ == "__main__":
    main()
