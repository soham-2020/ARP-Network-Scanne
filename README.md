Overview

NetSense is a comprehensive Python-based Network Monitoring and Security Toolkit that integrates real-time device scanning, network simulation, and machine learning-based packet analysis.
It’s designed for cybersecurity researchers, IoT testers, and network administrators to study traffic patterns, detect anomalies, and simulate device behavior in a safe environment.

⚙️ Core Features
1️⃣ Dynamic ARP Network Scanner

Uses Scapy to perform real-time device discovery within the local subnet.

Displays IP, MAC, Vendor, and Hostname using the OUI database and reverse DNS lookup.

Auto-detects local IP and subnet range dynamically.

2️⃣ Mock Network Simulator

Simulates real-world device behavior with random connections, disconnections, and failed Wi-Fi attempts.

Logs every network event with timestamps for behavioral analysis.

Ideal for testing alert and monitoring systems safely.

3️⃣ Machine Learning-Based Packet Classifier

Captures live network packets using Scapy’s sniff() function.

Extracts packet features (Length, Protocol) and labels them for anomaly detection.

Trains a Random Forest classifier to distinguish between normal and suspicious packets.

Outputs a classification report (precision, recall, F1-score).

🧩 Tech Stack

Languages: Python 3.10+

Libraries: scapy, socket, mac-vendor-lookup, pandas, scikit-learn

Concepts: Network Scanning, DNS Lookup, OUI Vendor Mapping, ML Classification

🚀 How to Run
# 1️⃣ Install dependencies
pip install scapy mac-vendor-lookup pandas scikit-learn

# 2️⃣ Run as Administrator or root for network access
sudo python netsense.py

📊 Key Outputs

Real-time device table (IP, MAC, Vendor, Hostname)

Mock connection/disconnection events

ML classification metrics for network anomaly detection
