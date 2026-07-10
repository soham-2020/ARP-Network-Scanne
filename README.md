<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Scapy-Network%20Magic-1E90FF?style=for-the-badge&logo=wireshark&logoColor=white"/>
<img src="https://img.shields.io/badge/scikit--learn-ML%20Powered-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-8B5CF6?style=for-the-badge"/>

<br/><br/>

```
███╗   ██╗███████╗████████╗███████╗███████╗███╗   ██╗███████╗███████╗
████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝
██╔██╗ ██║█████╗     ██║   ███████╗█████╗  ██╔██╗ ██║███████╗█████╗  
██║╚██╗██║██╔══╝     ██║   ╚════██║██╔══╝  ██║╚██╗██║╚════██║██╔══╝  
██║ ╚████║███████╗   ██║   ███████║███████╗██║ ╚████║███████║███████╗
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝
```

### 🛡️ Real-Time Network Monitoring · Anomaly Detection · ML Packet Analysis

*Detect devices. Analyse traffic. Stay ahead of threats.*

</div>

---

## 📖 Overview

**NetSense** is a comprehensive Python-based **Network Monitoring and Security Toolkit** that combines:

- 🔍 **Real-time ARP device discovery** on your local subnet
- 🤖 **Machine learning-based packet classification** to flag suspicious traffic
- 🧪 **Mock network simulator** for safe testing of alert and monitoring systems

Built for **cybersecurity researchers, IoT testers, and network administrators** who need a lightweight yet powerful tool to study traffic patterns and detect anomalies — without expensive commercial software.

---

## ✨ Features

<table>
<tr>
<td width="33%" valign="top">

### 🌐 ARP Scanner
- Discovers all active devices on the subnet in real-time
- Shows **IP**, **MAC**, **Vendor**, and **Hostname**
- Auto-detects local IP and subnet range
- Parallel reverse DNS lookups (fast!)
- OUI vendor database with auto-update

</td>
<td width="33%" valign="top">

### 🧪 Mock Simulator
- Simulates device connect / disconnect events
- Randomly triggers wrong Wi-Fi password attempts
- Timestamped event logging
- Safe sandbox — no real traffic sent
- Fully configurable scan interval and probabilities

</td>
<td width="33%" valign="top">

### 🤖 ML Classifier
- Live packet capture via Scapy sniff()
- Extracts 6 features per packet
- Trains a **Random Forest** classifier
- Full precision / recall / F1 report
- Feature importance visualisation
- Handles class imbalance automatically

</td>
</tr>
</table>

---

## 🚀 How to Run

### ✅ Prerequisites

| Requirement | Version | Check |
|------------|---------|-------|
| Python | 3.10+ | `python --version` |
| pip | latest | `pip --version` |
| Administrator / root access | required | for raw socket operations |
| Internet connection | optional | for OUI vendor database update |

---

### 📦 Step 1 — Install Dependencies

```bash
pip install scapy mac-vendor-lookup pandas scikit-learn
```

> 💡 Use a virtual environment to keep dependencies isolated:
> ```bash
> python -m venv venv
> source venv/bin/activate      # Linux / macOS
> venv\Scripts\activate         # Windows
> pip install scapy mac-vendor-lookup pandas scikit-learn
> ```

---

### 🖥️ Step 2 — Clone the Repository

```bash
git clone https://github.com/soham-2020/ARP-Network-Scanne.git
cd ARP-Network-Scanne
```

---

### ▶️ Step 3 — Run the Tool

#### 🐧 Linux / macOS
```bash
# ARP Network Scanner (discovers all devices on your subnet)
sudo python netsense.py scan

# Mock Network Simulator (safe testing — no real packets)
sudo python netsense.py simulate

# ML Packet Classifier (captures live traffic + trains model)
sudo python netsense.py ml

# Run all three modules one after another
sudo python netsense.py all
```

#### 🪟 Windows (Run PowerShell as Administrator)
```powershell
# ARP Network Scanner
python netsense.py scan

# Mock Network Simulator
python netsense.py simulate

# ML Packet Classifier
python netsense.py ml

# Run all three
python netsense.py all
```

> ⚠️ **Why Administrator?**
> ARP scanning uses raw sockets (Layer 2) which require elevated privileges on all operating systems.

---

### 🔧 Run Individual Modules Directly

```bash
# Run only the scanner
sudo python network_scanner.py

# Run only the simulator
python mock_simulator.py

# Run only the ML classifier
sudo python ml_classifier.py
```

---

### 🐛 Common Issues & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Operation not permitted` | Not running as root/admin | Use `sudo` on Linux/macOS or run as Administrator on Windows |
| `ModuleNotFoundError: scapy` | Dependencies not installed | Run `pip install scapy` |
| `No active devices found` | ARP timeout too short | Increase `timeout` in `scan_network()` |
| `OUI update failed` | No internet | Vendor names show as `UNKNOWN` — harmless |
| `Live capture failed` | Firewall blocking | ML classifier falls back to synthetic dataset automatically |

---

## 📊 Sample Output

### ARP Network Scan
```
🌐 Dynamic ARP Network Scanner 🌐
========================================
Local IP  : 192.168.1.10
Scanning  : 192.168.1.0/24

Performing reverse DNS lookups for hostnames (parallel)...

Total active devices found: 5
──────────────────────────────────────────────────────────────────────────────────
IP Address       MAC Address         Vendor/Company                    Hostname
──────────────────────────────────────────────────────────────────────────────────
192.168.1.1      d4:6e:0e:aa:bb:cc   TP-LINK TECHNOLOGIES CO.,LTD      router.home
192.168.1.5      00:1a:2b:3c:4d:5e   Apple, Inc.                       macbook-pro.local
192.168.1.8      b8:27:eb:ff:ee:dd   Raspberry Pi Foundation            raspberrypi
192.168.1.12     00:1d:2e:3f:4a:5b   Dell Inc.                         DESKTOP-ABC123
192.168.1.19     00:1e:2f:3a:4b:5c   HP Inc.                           N/A (No Hostname)
──────────────────────────────────────────────────────────────────────────────────
```

### ML Classification Report
```
🤖 Training Random Forest classifier…

📊 Classification Report
==================================================
              precision    recall  f1-score   support

      normal       0.97      0.99      0.98        75
  suspicious       0.94      0.83      0.88        12

    accuracy                           0.97        87

🔑 Feature Importances
──────────────────────────────
  dport        0.3142  ████████████
  length       0.2876  ███████████
  sport        0.1934  ███████
  protocol     0.1205  ████
  ttl          0.0614  ██
  tcp_flags    0.0229  █
```

---

## 🗂️ Project Structure

```
NetSense/
├── netsense.py          # 🎯 Unified CLI entry point
├── network_scanner.py   # 🌐 ARP Scanner (real-time device discovery)
├── mock_simulator.py    # 🧪 Mock Network Simulator (safe testing)
├── ml_classifier.py     # 🤖 ML Packet Classifier (anomaly detection)
└── model/               # 💾 Saved model artefacts
```

---

## 🧩 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.10+ | Core runtime |
| **Packet I/O** | [Scapy](https://scapy.net/) | ARP scanning & live packet capture |
| **Vendor Lookup** | [mac-vendor-lookup](https://pypi.org/project/mac-vendor-lookup/) | OUI → Company name |
| **DNS** | `socket` (stdlib) | Reverse hostname lookups |
| **Data** | [pandas](https://pandas.pydata.org/) | Feature DataFrame |
| **ML** | [scikit-learn](https://scikit-learn.org/) | Random Forest classifier |
| **Concurrency** | `concurrent.futures` | Parallel DNS queries |

---

## ⚙️ Module Details

<details>
<summary><b>🌐 network_scanner.py — ARP Network Scanner</b></summary>

**How it works:**
1. Detects your local IP automatically via a UDP trick (no packets sent to the internet)
2. Constructs the `/24` subnet range
3. Sends ARP broadcast requests using Scapy `srp()`
4. For each responding host, looks up the vendor via OUI database
5. Runs **parallel** reverse-DNS lookups using a thread pool
6. Prints a formatted device table

```python
from network_scanner import dynamic_network_scanner_main
dynamic_network_scanner_main()
```

</details>

<details>
<summary><b>🧪 mock_simulator.py — Mock Network Simulator</b></summary>

Simulates realistic device behaviour with configurable parameters. Sends **zero** real network traffic.

```python
from mock_simulator import run_simulator

run_simulator(
    scan_interval=5.0,      # seconds between scan cycles
    disconnect_chance=0.30, # 30% chance a device drops each cycle
    wrong_pwd_chance=0.20,  # 20% chance of wrong-password attempt
    max_new_attempts=3,     # max new connection attempts per cycle
    max_iterations=None,    # None = run forever; or set a number
)
```

**Simulated events with timestamps:**
- `[2024-01-15 10:23:45] ✔  NEW DEVICE CONNECTED`
- `[2024-01-15 10:23:50] ✗  DISCONNECTED`
- `[2024-01-15 10:23:55] ⚠  WRONG Wi-Fi PASSWORD`

</details>

<details>
<summary><b>🤖 ml_classifier.py — ML Packet Classifier</b></summary>

**Features extracted per packet:**

| Feature | Description |
|---------|------------|
| `length` | Total packet size in bytes |
| `protocol` | IP protocol number (TCP=6, UDP=17, ICMP=1) |
| `ttl` | Time-to-live value |
| `tcp_flags` | TCP control flags (SYN, ACK, RST…) |
| `sport` | Source port |
| `dport` | Destination port |

> Falls back to a synthetic dataset automatically if live capture fails (e.g. in sandboxed environments).

```python
from ml_classifier import main as ml_main
ml_main()
```

</details>

---

## 🔒 Security & Ethics

> **Important:** This tool is designed for use on **networks you own or have explicit permission to scan.** Scanning networks without authorisation may be illegal in your jurisdiction. Use responsibly.

- Only ARP requests are sent (Layer 2 — no OS-level intrusion)
- Mock simulator sends **zero** real network traffic
- ML classifier captures packets **passively** — read-only sniffing only

---

## 🛣️ Roadmap

- [ ] Web dashboard (Flask/FastAPI) with live device map
- [ ] Email / Telegram alerts on new device detection
- [ ] Export scan results to CSV / JSON
- [ ] Docker container for easy deployment
- [ ] IPv6 neighbour discovery support
- [ ] PCAP file analysis mode (offline ML classification)

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**.

---

<div align="center">

Made with ❤️ by [soham-2020](https://github.com/soham-2020)

⭐ **Star this repo if you found it useful!** ⭐

</div>
