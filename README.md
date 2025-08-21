Network Monitoring & ML Toolkit

A comprehensive Python project for network monitoring, device simulation, and packet classification using machine learning. This toolkit combines real network scanning, mock network simulation, and ML-based packet analysis into a single, easy-to-use Python package.

Features
1. Dynamic Network Scanner

Scans your local network using ARP requests to detect active devices.

Captures IP address, MAC address, and optionally vendor/manufacturer.

Continuously monitors devices to detect new connections or disconnections.

Ideal for network admins, cybersecurity enthusiasts, or anyone wanting to track devices on their network.

2. Mock Network Simulation

Simulates a dynamic network environment with a predefined pool of devices.

Randomly connects or disconnects devices and simulates failed Wi-Fi login attempts.

Provides a safe testing environment for monitoring scripts or alert systems.

Prints network events in real-time with emojis for clarity (✅ for connection, ❌ for disconnection, ⚠️ for wrong password attempts).

3. ML-Based Packet Capture & Classification

Captures live network packets using Scapy.

Extracts packet features such as Length and Protocol.

Labels packets as normal (0) or potential attack (1) based on heuristics.

Trains a Random Forest Classifier to detect suspicious packets.

Outputs a classification report with precision, recall, f1-score, and accuracy.

4. Automated Setup

Includes a helper script to install all required Python packages (scapy, python-nmap, numpy, scikit-learn).

Ensures the project works out-of-the-box on Windows, macOS, or Linux.

Installation

Clone the repository:

git clone https://github.com/your-username/network-monitor-ml-toolkit.git
cd network-monitor-ml-toolkit


Install required packages:

python install_packages.py

Usage
1. Run Dynamic Network Scanner
python arp_scanner.py


Scans the subnet for connected devices.

Prints IP, MAC, and vendor info.

2. Run Mock Network Simulation
python mock_network.py


Simulates device connections/disconnections and failed login attempts.

Updates network status every 5 seconds.

3. Run ML Packet Classifier
python ml_packet_classifier.py


Captures packets from the network.

Labels packets as normal or suspicious.

Trains a Random Forest model and prints the classification report.
