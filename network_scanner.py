import scapy.all as scapy
import socket
# Ensure you have installed this library: pip install mac-vendor-lookup
from mac_vendor_lookup import MacLookup 

# --- MAC Vendor Lookup Initialization ---
try:
    print("Updating OUI database (requires internet)...")
    # Attempt to update the OUI database for the freshest vendor names
    MacLookup().update_vendors() 
    print("OUI database update complete.")
    mac_lookup = MacLookup() 
except Exception as e:
    print(f"Warning: Failed to update or initialize MacLookup: {e}. Vendor names may be inaccurate.")
    # Fallback/Mock for MacLookup if it fails
    class MockMacLookup:
        def lookup(self, mac): return "UNKNOWN"
    mac_lookup = MockMacLookup()
# ----------------------------------------


# 🆕 ADDED: Function to get the Hostname from IP Address
def get_hostname_from_ip(ip_address):
    """Performs a reverse DNS lookup to get the device's hostname."""
    try:
        # socket.gethostbyaddr is the standard way to do reverse lookup
        hostname, aliases, addresses = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        # Common error when hostname is not registered (e.g., if DNS isn't configured for it)
        return "N/A (No Hostname)"
    except Exception:
        return "N/A (Lookup Failed)"


def get_local_ip_and_subnet():
    """Tries to get the local IP and calculates the subnet range (e.g., 192.168.1.0/24)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        ip_parts = local_ip.split('.')
        subnet_range = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.0/24'
        return subnet_range, local_ip
    except OSError:
        print("Could not get local IP. Check network connection.")
        return None, None

def scan_network(ip_range):
    """
    Scans the given IP range using ARP requests to find active hosts.
    Returns a list of dictionaries with 'ip', 'mac', and 'vendor'.
    """
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    devices_list = []
    for sent, received in answered_list:
        mac_address = received.hwsrc
        
        # Get Vendor Name
        try:
            vendor_name = mac_lookup.lookup(mac_address)
        except Exception:
            vendor_name = "UNKNOWN"
            
        device_info = {
            "ip": received.psrc,
            "mac": mac_address,
            "vendor": vendor_name 
        }
        devices_list.append(device_info)

    return devices_list

def dynamic_network_scanner_main():
    """Main function to run the network scan and display results."""
    print("🚀 Dynamic Network Scanner 🚀")
    
    ip_range, local_ip = get_local_ip_and_subnet()

    if ip_range is None:
        return

    print(f"Scanning local network at: {ip_range} (Local IP: {local_ip})\n")
    
    # Perform the scan
    devices = scan_network(ip_range)
    
    if not devices:
        print("No active devices found (other than possibly this host).")
        return

    # --------------------------------------------------------------------------
    # 💥 MODIFIED: Loop to add Hostname Lookup 💥
    # --------------------------------------------------------------------------
    
    # We create a final list to hold all enhanced data before printing
    final_devices_list = []
    print("Performing reverse DNS lookups for hostnames...")
    for device in devices:
        # Call the new hostname function
        hostname = get_hostname_from_ip(device['ip']) 
        device['hostname'] = hostname
        final_devices_list.append(device)
        
    print(f"\nTotal active devices found: {len(final_devices_list)}")
    print("-" * 105)
    # UPDATED: Added a column for Hostname
    print("{:<15} {:<18} {:<40} {:<30}".format("IP Address", "MAC Address", "Vendor/Company", "Device Hostname"))
    print("-" * 105)
    
    for device in final_devices_list:
        # UPDATED: Included the hostname in the final output
        print("{:<15} {:<18} {:<40} {:<30}".format(
            device['ip'], 
            device['mac'], 
            device['vendor'], 
            device['hostname']
        ))

# Execute the scanner
if __name__ == "__main__":
    dynamic_network_scanner_main()