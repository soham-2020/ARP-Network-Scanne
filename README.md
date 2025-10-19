NetSense: Comprehensive Network Monitoring & ML Toolkit
NetSense is a robust Python toolkit developed for comprehensive network monitoring, device behavior simulation, and advanced packet classification using machine learning. This project integrates real-world network scanning with a safe, simulated testing environment and an ML model for security analysis, making it a valuable resource for network administrators, security researchers, and enthusiasts.

Features
I. Real-World Network Scanning
This module actively discovers and identifies devices connected to the local network by leveraging low-level networking protocols.

Dynamic Network Scanner: Uses ARP requests via Scapy to efficiently detect all active hosts on the local subnet. It automatically determines the local IP address and the correct subnet range to scan.

Advanced Device Identification: Captures the IP Address, MAC Address, and performs Reverse DNS Lookup using the socket library to retrieve the device's Hostname (e.g., "My-Laptop-PC").

Vendor Lookup: Translates the first part of the MAC address to identify the device Manufacturer/Vendor (e.g., Apple, Cisco, HP) using the OUI database provided by the mac-vendor-lookup library.

II. Network Simulation and Testing
This module provides a controlled environment for testing monitoring scripts and alert systems without affecting a live network.

Mock Network Simulation: Simulates a dynamic network environment using a predefined pool of devices. The simulation generates random events such as:

Connections: New devices joining the network.

Disconnections: A 30% chance of a connected device randomly dropping off.

Failed Attempts: A 20% chance that a device attempting to connect fails due to a simulated "wrong Wi-Fi password."

Real-time Event Logging: Prints simulated network events to the console, clearly marking successful connections, disconnections, and authentication failures.

III. Machine Learning-Based Packet Analysis
This module introduces a foundational machine learning approach to network security monitoring.

Packet Capture and Feature Extraction: Captures live network packets using Scapy and extracts relevant features, such as packet Length and Protocol.

Suspicious Packet Detection: Labels packets as normal (0) or potentially suspicious (1) based on simple, predefined heuristics.

Random Forest Classifier: Trains a Random Forest Classifier from the scikit-learn library to learn patterns associated with normal versus suspicious traffic.

Performance Metrics: Outputs a comprehensive classification report to evaluate the model, including Precision, Recall, F1-score, and Accuracy.

Requirements and Setup
To run this toolkit, you need the following Python libraries. A requirements.txt file is included in the project for easy installation:

Bash

pip install -r requirements.txt
Key Libraries:
scapy: For network scanning (ARP) and raw packet capture.

mac-vendor-lookup: For device manufacturer identification.

scikit-learn: For the machine learning classification module.

numpy: For data processing within the ML module.

Note on Permissions: The real-world scanning and packet capture features require elevated privileges (root/administrator) to interact with the raw network interfaces. Please run the corresponding scripts with sudo on Linux/macOS or as an Administrator on Windows.
