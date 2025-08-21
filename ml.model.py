import time
import random

# Sample devices (mock pool)
sample_devices = [
    {"IP": "192.168.1.2", "MAC": "00:1A:2B:3C:4D:5E", "Vendor": "Apple"},
    {"IP": "192.168.1.3", "MAC": "00:1B:2C:3D:4E:5F", "Vendor": "Samsung"},
    {"IP": "192.168.1.4", "MAC": "00:1C:2D:3E:4F:5A", "Vendor": "Xiaomi"},
    {"IP": "192.168.1.5", "MAC": "00:1D:2E:3F:4A:5B", "Vendor": "Dell"},
    {"IP": "192.168.1.6", "MAC": "00:1E:2F:3A:4B:5C", "Vendor": "HP"},
    {"IP": "192.168.1.7", "MAC": "00:1F:2A:3B:4C:5D", "Vendor": "Lenovo"},
    {"IP": "192.168.1.8", "MAC": "00:1G:2B:3C:4D:5E", "Vendor": "Asus"},
]

# Devices currently connected
connected_devices = {}

while True:
    print("\n📡 Scanning network (mock)...")

    # Randomly disconnect some devices
    if connected_devices and random.random() < 0.3:  # 30% chance
        to_disconnect = random.choice(list(connected_devices.keys()))
        print(f"❌ Device disconnected: {to_disconnect}, MAC: {connected_devices[to_disconnect]['MAC']}")
        del connected_devices[to_disconnect]

    # Randomly pick 1–3 devices to try connecting
    new_attempts = random.sample(sample_devices, random.randint(1, 3))

    for device in new_attempts:
        ip, mac, vendor = device["IP"], device["MAC"], device["Vendor"]

        # 20% chance of wrong password attempt
        wrong_password = random.random() < 0.2  

        if ip not in connected_devices:
            if wrong_password:
                print(f"⚠️ Device {ip} ({vendor}) attempted WRONG Wi-Fi password!")
            else:
                connected_devices[ip] = device
                print(f"✅ New device connected: {ip}, MAC: {mac}, Vendor: {vendor}")
        else:
            print(f"Connected: {ip}, MAC: {mac}, Vendor: {vendor}")

    time.sleep(5)  # Scan every 5 seconds

