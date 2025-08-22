🖧 Network Monitoring & ML Toolkit

A comprehensive Python project for network monitoring, device simulation, and packet classification using machine learning. This toolkit combines real network scanning, mock network simulation, and ML-based packet analysis into a single, easy-to-use Python package.

📌 Features
1. Dynamic Network Scanner

Scans your local network using ARP requests to detect active devices.

Captures IP address, MAC address, and optionally vendor/manufacturer.

Continuously monitors devices for new connections or disconnections.

Perfect for network admins, cybersecurity enthusiasts, or anyone wanting to track devices.

2. Mock Network Simulation

Simulates a dynamic network environment with a predefined pool of devices.

Randomly connects/disconnects devices and simulates failed Wi-Fi login attempts.

Provides a safe testing environment for monitoring scripts or alert systems.

Prints network events in real-time with emojis:

✅ Connection

❌ Disconnection

⚠️ Wrong password attempts

3. ML-Based Packet Capture & Classification

Captures live network packets using Scapy.

Extracts packet features like Length and Protocol.

Labels packets as normal (0) or potential attack (1) based on heuristics.

Trains a Random Forest Classifier to detect suspicious packets.

Outputs a classification report with precision, recall, f1-score, and accuracy.

4. Automated Setup

Includes a helper script to install all required Python packages:
scapy, python-nmap, numpy, scikit-learn.

Works out-of-the-box on Windows, macOS, or Linux.
