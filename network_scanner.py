import scapy.all as scapy
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure you have installed this library: pip install mac-vendor-lookup
try:
    from mac_vendor_lookup import MacLookup
except ImportError:
    MacLookup = None

# ---------------------------------------------------------------------------
# MAC Vendor Lookup Initialization
# ---------------------------------------------------------------------------
def _init_mac_lookup():
    """Initialize and optionally update the OUI database. Returns a lookup object."""
    if MacLookup is None:
        print("Warning: mac-vendor-lookup not installed. Run: pip install mac-vendor-lookup")
        return None

    mac_lookup = MacLookup()
    try:
        print("Updating OUI database (requires internet)...")
        # Update the OUI database using the SAME instance to avoid double init
        mac_lookup.update_vendors()
        print("OUI database update complete.")
    except Exception as e:
        print(f"Warning: Could not update OUI database: {e}. Vendor names may be outdated.")
    return mac_lookup


mac_lookup = _init_mac_lookup()


# ---------------------------------------------------------------------------
# Helper: Reverse DNS Lookup (with timeout)
# ---------------------------------------------------------------------------
def get_hostname_from_ip(ip_address: str, timeout: float = 1.5) -> str:
    """
    Performs a reverse DNS lookup to retrieve the device's hostname.

    Args:
        ip_address: The IPv4 address to look up.
        timeout:    Maximum seconds to wait for a DNS response.

    Returns:
        The hostname string, or a descriptive fallback value.
    """
    # socket.setdefaulttimeout applies only to blocking socket operations
    original_timeout = socket.getdefaulttimeout()
    try:
        socket.setdefaulttimeout(timeout)
        hostname, _aliases, _addresses = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        # No PTR record exists for this IP
        return "N/A (No Hostname)"
    except socket.gaierror:
        return "N/A (DNS Error)"
    except socket.timeout:
        return "N/A (Timeout)"
    except Exception:
        return "N/A (Lookup Failed)"
    finally:
        socket.setdefaulttimeout(original_timeout)


# ---------------------------------------------------------------------------
# Helper: Detect Local IP + Subnet
# ---------------------------------------------------------------------------
def get_local_ip_and_subnet() -> tuple[str | None, str | None]:
    """
    Auto-detects the local IP address and calculates the /24 subnet range.

    Returns:
        (subnet_range, local_ip) e.g. ("192.168.1.0/24", "192.168.1.10"),
        or (None, None) on failure.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 80))
        local_ip: str = s.getsockname()[0]
        s.close()
    except OSError as exc:
        print(f"Could not detect local IP: {exc}. Check network connection.")
        return None, None

    parts = local_ip.split(".")
    # Build the network address for a /24 subnet
    subnet_range = f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    return subnet_range, local_ip


# ---------------------------------------------------------------------------
# Core: ARP Scan
# ---------------------------------------------------------------------------
def scan_network(ip_range: str) -> list[dict]:
    """
    Sends ARP broadcast requests over the given IP range and collects replies.

    Args:
        ip_range: CIDR notation, e.g. "192.168.1.0/24".

    Returns:
        List of dicts with keys: 'ip', 'mac', 'vendor'.
    """
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request

    # timeout=2 gives slower devices a fair chance to reply
    answered_list, _ = scapy.srp(packet, timeout=2, verbose=False)

    devices: list[dict] = []
    for _sent, received in answered_list:
        mac_address: str = received.hwsrc

        vendor_name = "UNKNOWN"
        if mac_lookup is not None:
            try:
                vendor_name = mac_lookup.lookup(mac_address)
            except Exception:
                vendor_name = "UNKNOWN"

        devices.append({
            "ip":     received.psrc,
            "mac":    mac_address,
            "vendor": vendor_name,
        })

    return devices


# ---------------------------------------------------------------------------
# Core: Hostname enrichment (parallel for speed)
# ---------------------------------------------------------------------------
def enrich_with_hostnames(devices: list[dict], max_workers: int = 30) -> list[dict]:
    """
    Adds a 'hostname' key to every device dict using parallel DNS lookups.

    Args:
        devices:     List of device dicts produced by scan_network().
        max_workers: Thread pool size (one thread per DNS query).

    Returns:
        The same list with 'hostname' populated on each entry.
    """
    print("Performing reverse DNS lookups for hostnames (parallel)...")

    def lookup(device: dict) -> dict:
        device["hostname"] = get_hostname_from_ip(device["ip"])
        return device

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(lookup, d): d for d in devices}
        for future in as_completed(futures):
            # Exceptions are suppressed inside lookup(); re-raise if they escape
            future.result()

    return devices


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
def print_results(devices: list[dict]) -> None:
    """Pretty-prints the scan results as a formatted table."""
    COL_IP     = 16
    COL_MAC    = 19
    COL_VENDOR = 40
    COL_HOST   = 35
    total_width = COL_IP + COL_MAC + COL_VENDOR + COL_HOST + 3  # spaces

    separator = "-" * total_width
    header = (
        f"{'IP Address':<{COL_IP}} "
        f"{'MAC Address':<{COL_MAC}} "
        f"{'Vendor/Company':<{COL_VENDOR}} "
        f"{'Device Hostname':<{COL_HOST}}"
    )

    print(f"\nTotal active devices found: {len(devices)}")
    print(separator)
    print(header)
    print(separator)

    for device in devices:
        print(
            f"{device['ip']:<{COL_IP}} "
            f"{device['mac']:<{COL_MAC}} "
            f"{device['vendor']:<{COL_VENDOR}} "
            f"{device['hostname']:<{COL_HOST}}"
        )

    print(separator)


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def dynamic_network_scanner_main() -> None:
    """Main function: detect subnet, scan, enrich with hostnames, display."""
    print("🌐 Dynamic ARP Network Scanner 🌐")
    print("=" * 40)

    ip_range, local_ip = get_local_ip_and_subnet()
    if ip_range is None:
        return

    print(f"Local IP  : {local_ip}")
    print(f"Scanning  : {ip_range}")
    print()

    devices = scan_network(ip_range)

    if not devices:
        print("No active devices found (other than possibly this host).")
        return

    devices = enrich_with_hostnames(devices)
    print_results(devices)


if __name__ == "__main__":
    dynamic_network_scanner_main()
