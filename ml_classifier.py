"""
ml_classifier.py  –  NetSense ML-Based Packet Classifier
==========================================================
Captures live packets using Scapy, extracts features, labels them,
trains a Random Forest classifier, and reports precision/recall/F1.

Run (requires root / Administrator):
    sudo python ml_classifier.py        # Linux / macOS
    python ml_classifier.py             # Windows (run as Administrator)

Dependencies:
    pip install scapy pandas scikit-learn
"""

import time
import random
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Scapy may print a warning on import — suppress it cleanly
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: scapy not installed. Live capture will be skipped.")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CAPTURE_COUNT  = 100   # Number of packets to sniff (increase for real use)
CAPTURE_IFACE  = None  # None = default interface; set e.g. "eth0" on Linux
RANDOM_STATE   = 42


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------
def extract_features(packet: Any) -> dict | None:
    """
    Extract numeric features from a single Scapy packet.

    Returns a dict with extracted fields, or None if the packet
    cannot be processed (e.g. non-IP packet).
    """
    if not packet.haslayer(scapy.IP):
        return None

    ip_layer = packet[scapy.IP]

    # Protocol number (TCP=6, UDP=17, ICMP=1, etc.)
    proto = ip_layer.proto

    # Packet length in bytes
    length = len(packet)

    # TTL value (useful for OS fingerprinting / anomaly detection)
    ttl = ip_layer.ttl

    # TCP flags (0 if not TCP)
    tcp_flags = 0
    if packet.haslayer(scapy.TCP):
        tcp_flags = int(packet[scapy.TCP].flags)

    # Source / destination port (0 if not TCP/UDP)
    sport = dport = 0
    if packet.haslayer(scapy.TCP):
        sport = packet[scapy.TCP].sport
        dport = packet[scapy.TCP].dport
    elif packet.haslayer(scapy.UDP):
        sport = packet[scapy.UDP].sport
        dport = packet[scapy.UDP].dport

    return {
        "length":    length,
        "protocol":  proto,
        "ttl":       ttl,
        "tcp_flags": tcp_flags,
        "sport":     sport,
        "dport":     dport,
    }


def label_packet(features: dict) -> str:
    """
    Heuristic labelling for demonstration purposes.

    In production replace this with ground-truth labels from a PCAP or IDS.
    Rules:
      - ICMP flood signature (large ICMP packets) → suspicious
      - Uncommon high ports on TCP → suspicious
      - Known-good protocols & ports          → normal
    """
    proto  = features["protocol"]
    length = features["length"]
    dport  = features["dport"]

    # ICMP (1) with large payload = potential flood
    if proto == 1 and length > 500:
        return "suspicious"

    # Very large packets with unusual ports
    if length > 1400 and dport not in (80, 443, 53, 22, 8080):
        return "suspicious"

    # TCP SYN with no data and unusual port
    if proto == 6 and features["tcp_flags"] == 2 and dport > 49152:
        return "suspicious"

    return "normal"


# ---------------------------------------------------------------------------
# Live packet capture
# ---------------------------------------------------------------------------
def capture_packets(count: int = CAPTURE_COUNT, iface: str | None = CAPTURE_IFACE) -> list[dict]:
    """
    Capture `count` packets and return their feature dicts.

    Falls back to a synthetic dataset if Scapy is unavailable or
    if no packets are captured (e.g. in a sandboxed environment).
    """
    records: list[dict] = []

    if SCAPY_AVAILABLE:
        print(f"📡 Capturing {count} packets (this may take a few seconds)…")
        try:
            packets = scapy.sniff(count=count, iface=iface, timeout=30, store=True)
            for pkt in packets:
                features = extract_features(pkt)
                if features is not None:
                    features["label"] = label_packet(features)
                    records.append(features)
            print(f"   Captured {len(records)} usable IP packets.")
        except Exception as exc:
            print(f"   Live capture failed: {exc}")

    if not records:
        print("⚠  Falling back to synthetic dataset for demonstration…")
        records = _generate_synthetic_data(n_normal=180, n_suspicious=20)

    return records


def _generate_synthetic_data(n_normal: int, n_suspicious: int) -> list[dict]:
    """
    Generate a small synthetic dataset that mimics captured packets.
    Only used when live capture is unavailable.
    """
    rng = random.Random(RANDOM_STATE)
    data: list[dict] = []

    for _ in range(n_normal):
        proto = rng.choice([6, 17, 6, 6])  # mostly TCP
        dport = rng.choice([80, 443, 53, 22, 8080])
        data.append({
            "length":    rng.randint(60, 800),
            "protocol":  proto,
            "ttl":       rng.choice([64, 128, 255]),
            "tcp_flags": 16,  # ACK
            "sport":     rng.randint(1024, 49151),
            "dport":     dport,
            "label":     "normal",
        })

    for _ in range(n_suspicious):
        data.append({
            "length":    rng.randint(1200, 1500),
            "protocol":  rng.choice([1, 6]),
            "ttl":       rng.randint(1, 60),
            "tcp_flags": rng.choice([2, 4, 0]),  # SYN / RST / null
            "sport":     rng.randint(49152, 65535),
            "dport":     rng.randint(49152, 65535),
            "label":     "suspicious",
        })

    rng.shuffle(data)
    return data


# ---------------------------------------------------------------------------
# Model training & evaluation
# ---------------------------------------------------------------------------
FEATURE_COLS = ["length", "protocol", "ttl", "tcp_flags", "sport", "dport"]


def train_and_evaluate(records: list[dict]) -> None:
    """
    Train a Random Forest classifier on the captured / synthetic data
    and print a full classification report.
    """
    df = pd.DataFrame(records)

    if df["label"].nunique() < 2:
        print("⚠  Only one class present in data — cannot train a meaningful classifier.")
        print("   Capture more packets or adjust heuristics.")
        return

    X = df[FEATURE_COLS]
    y = df["label"]

    # Encode labels to integers (RandomForest works fine with strings too,
    # but encoding makes the report cleaner)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.25, random_state=RANDOM_STATE, stratify=y_encoded
    )

    print("\n🤖 Training Random Forest classifier…")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=RANDOM_STATE,
        class_weight="balanced",   # handles class imbalance automatically
    )
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    print("\n📊 Classification Report")
    print("=" * 50)
    print(
        classification_report(
            y_test, y_pred,
            target_names=le.classes_,
            zero_division=0,
        )
    )

    # Feature importance
    importances = sorted(
        zip(FEATURE_COLS, clf.feature_importances_),
        key=lambda x: x[1], reverse=True
    )
    print("🔑 Feature Importances")
    print("-" * 30)
    for feat, imp in importances:
        bar = "█" * int(imp * 40)
        print(f"  {feat:<12} {imp:.4f}  {bar}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    start = time.time()

    print("🛡️  NetSense ML Packet Classifier")
    print("=" * 45)

    records = capture_packets()
    train_and_evaluate(records)

    print(f"\n⏱  Done in {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
