import logging
import threading
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scapy.all import sniff, IP
from scapy.layers.inet import TCP, UDP

from src.utils.logger import get_logger
from src.anomaly_detection.detector import AnomalyDetector

logger = get_logger(__name__)

class TrafficMonitor:
    """Real-time network traffic monitor."""
    
    def __init__(
        self,
        detector: AnomalyDetector,
        interface: str = "eth0",
        window_size: int = 10,  # seconds
        feature_names: Optional[List[str]] = None
    ):
        """
        Initialize the traffic monitor.
        
        Args:
            detector: Trained anomaly detector
            interface: Network interface to monitor
            window_size: Time window for traffic analysis in seconds
            feature_names: List of feature names to extract
        """
        self.detector = detector
        self.interface = interface
        self.window_size = window_size
        self.feature_names = feature_names
        
        # Initialize traffic windows
        self.current_window = []
        self.window_start_time = time.time()
        
        # Store recent predictions for trend analysis
        self.recent_predictions = deque(maxlen=100)
        
        # Threading control
        self.is_running = False
        self.capture_thread = None
        self.analysis_thread = None
        
        # Statistics
        self.stats = {
            "packets_processed": 0,
            "alerts_triggered": 0,
            "last_alert_time": None,
            "current_threat_level": "LOW"
        }
    
    def _extract_features(self, packet) -> Dict:
        """Extract relevant features from a packet."""
        features = {
            "packet_size": len(packet),
            "protocol": 0,  # Default for unknown
            "tcp_flags": 0,
            "udp_length": 0,
            "src_port": 0,
            "dst_port": 0
        }
        
        if IP in packet:
            features["protocol"] = packet[IP].proto
            
            if TCP in packet:
                features["tcp_flags"] = packet[TCP].flags
                features["src_port"] = packet[TCP].sport
                features["dst_port"] = packet[TCP].dport
            elif UDP in packet:
                features["udp_length"] = packet[UDP].len
                features["src_port"] = packet[UDP].sport
                features["dst_port"] = packet[UDP].dport
        
        return features
    
    def _process_packet(self, packet):
        """Process a captured packet."""
        if not packet:
            return
        
        # Extract features
        features = self._extract_features(packet)
        self.current_window.append(features)
        self.stats["packets_processed"] += 1
        
        # Check if window is complete
        current_time = time.time()
        if current_time - self.window_start_time >= self.window_size:
            self._analyze_window()
    
    def _analyze_window(self):
        """Analyze the current traffic window."""
        if not self.current_window:
            return
        
        # Convert window to DataFrame
        df = pd.DataFrame(self.current_window)
        
        # Calculate statistical features
        stats = {
            "packet_count": len(df),
            "avg_packet_size": df["packet_size"].mean(),
            "std_packet_size": df["packet_size"].std(),
            "tcp_ratio": (df["protocol"] == 6).mean(),
            "udp_ratio": (df["protocol"] == 17).mean(),
            "unique_src_ports": df["src_port"].nunique(),
            "unique_dst_ports": df["dst_port"].nunique(),
            "syn_ratio": (df["tcp_flags"] == 2).mean(),
        }
        
        # Prepare feature vector
        if self.feature_names:
            feature_vector = np.array([[
                stats[feature] if feature in stats else 0
                for feature in self.feature_names
            ]])
        else:
            feature_vector = np.array([list(stats.values())])
        
        # Detect anomalies
        is_anomaly, predictions = self.detector.predict(feature_vector)
        self.recent_predictions.append(is_anomaly[0])
        
        # Update threat level
        self._update_threat_level()
        
        # Reset window
        self.current_window = []
        self.window_start_time = time.time()
        
        # Log if anomaly detected
        if is_anomaly[0]:
            self.stats["alerts_triggered"] += 1
            self.stats["last_alert_time"] = time.time()
            logger.warning(
                f"Potential DDoS attack detected! "
                f"Threat Level: {self.stats['current_threat_level']}"
            )
    
    def _update_threat_level(self):
        """Update the current threat level based on recent predictions."""
        if len(self.recent_predictions) < 10:
            return
        
        # Calculate the ratio of positive predictions in recent windows
        alert_ratio = sum(self.recent_predictions) / len(self.recent_predictions)
        
        if alert_ratio > 0.8:
            self.stats["current_threat_level"] = "CRITICAL"
        elif alert_ratio > 0.5:
            self.stats["current_threat_level"] = "HIGH"
        elif alert_ratio > 0.2:
            self.stats["current_threat_level"] = "MEDIUM"
        else:
            self.stats["current_threat_level"] = "LOW"
    
    def _capture_traffic(self):
        """Capture network traffic in a separate thread."""
        try:
            sniff(
                iface=self.interface,
                prn=self._process_packet,
                store=0,
                stop_filter=lambda _: not self.is_running
            )
        except Exception as e:
            logger.error(f"Error capturing traffic: {str(e)}")
            self.stop()
    
    def _run_analysis(self):
        """Run continuous analysis in a separate thread."""
        while self.is_running:
            current_time = time.time()
            if current_time - self.window_start_time >= self.window_size:
                self._analyze_window()
            time.sleep(0.1)  # Prevent CPU overload
    
    def start(self):
        """Start monitoring traffic."""
        if self.is_running:
            logger.warning("Traffic monitor is already running")
            return
        
        logger.info(f"Starting traffic monitor on interface {self.interface}")
        self.is_running = True
        
        # Start capture thread
        self.capture_thread = threading.Thread(target=self._capture_traffic)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        
        # Start analysis thread
        self.analysis_thread = threading.Thread(target=self._run_analysis)
        self.analysis_thread.daemon = True
        self.analysis_thread.start()
    
    def stop(self):
        """Stop monitoring traffic."""
        logger.info("Stopping traffic monitor...")
        self.is_running = False
        
        if self.capture_thread:
            self.capture_thread.join(timeout=1.0)
        if self.analysis_thread:
            self.analysis_thread.join(timeout=1.0)
        
        logger.info("Traffic monitor stopped")
    
    def get_stats(self) -> Dict:
        """Get current monitoring statistics."""
        return {
            **self.stats,
            "uptime": time.time() - self.window_start_time,
            "packets_per_second": self.stats["packets_processed"] / max(1, time.time() - self.window_start_time)
        } 