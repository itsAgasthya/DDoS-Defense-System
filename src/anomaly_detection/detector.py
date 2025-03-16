import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import layers, Model

from src.utils.logger import get_logger

logger = get_logger(__name__)

class AutoEncoder(Model):
    """Autoencoder model for anomaly detection."""
    
    def __init__(self, input_dim: int, encoding_dim: int = 32):
        super().__init__()
        self.encoder = tf.keras.Sequential([
            layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            layers.Dense(64, activation='relu'),
            layers.Dense(encoding_dim, activation='relu')
        ])
        
        self.decoder = tf.keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(encoding_dim,)),
            layers.Dense(128, activation='relu'),
            layers.Dense(input_dim, activation='sigmoid')
        ])
        
    def call(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class AnomalyDetector:
    """Main anomaly detection class implementing multiple detection algorithms."""
    
    def __init__(self, config: Dict):
        """
        Initialize the anomaly detector.
        
        Args:
            config: Configuration dictionary containing detection parameters
        """
        self.config = config
        self.window_size = config["window_size"]
        self.update_interval = config["update_interval"]
        
        # Initialize detection algorithms
        self.algorithms = {}
        self.thresholds = {}
        
        # Statistical detection
        if self._is_algorithm_enabled("statistical"):
            self.algorithms["statistical"] = {
                "scaler": StandardScaler(),
                "threshold": config["algorithms"][0]["z_score_threshold"]
            }
        
        # Isolation Forest
        if self._is_algorithm_enabled("isolation_forest"):
            self.algorithms["isolation_forest"] = IsolationForest(
                contamination=config["algorithms"][1]["contamination"],
                random_state=42,
                n_jobs=-1
            )
        
        # Autoencoder
        if self._is_algorithm_enabled("autoencoder"):
            self.algorithms["autoencoder"] = None  # Will be initialized during training
            self.thresholds["autoencoder"] = config["algorithms"][2]["threshold"]
    
    def _is_algorithm_enabled(self, name: str) -> bool:
        """Check if an algorithm is enabled in the configuration."""
        for algo in self.config["algorithms"]:
            if algo["name"] == name and algo["enabled"]:
                return True
        return False
    
    def train(self, X_train: np.ndarray, X_val: Optional[np.ndarray] = None) -> None:
        """
        Train the anomaly detection models.
        
        Args:
            X_train: Training data
            X_val: Optional validation data
        """
        logger.info("Training anomaly detection models...")
        
        # Train statistical model
        if "statistical" in self.algorithms:
            logger.info("Training statistical model...")
            self.algorithms["statistical"]["scaler"].fit(X_train)
        
        # Train Isolation Forest
        if "isolation_forest" in self.algorithms:
            logger.info("Training Isolation Forest...")
            self.algorithms["isolation_forest"].fit(X_train)
        
        # Train Autoencoder
        if "autoencoder" in self.algorithms:
            logger.info("Training Autoencoder...")
            input_dim = X_train.shape[1]
            
            # Initialize autoencoder if not already done
            if self.algorithms["autoencoder"] is None:
                self.algorithms["autoencoder"] = AutoEncoder(input_dim)
            
            # Compile and train
            self.algorithms["autoencoder"].compile(
                optimizer='adam',
                loss='mse'
            )
            
            # Split validation data if not provided
            if X_val is None:
                val_split = 0.2
                val_size = int(len(X_train) * val_split)
                X_val = X_train[-val_size:]
                X_train = X_train[:-val_size]
            
            # Train the model
            self.algorithms["autoencoder"].fit(
                X_train, X_train,
                epochs=100,
                batch_size=32,
                validation_data=(X_val, X_val),
                callbacks=[
                    tf.keras.callbacks.EarlyStopping(
                        patience=10,
                        restore_best_weights=True
                    )
                ],
                verbose=1
            )
            
            # Calculate reconstruction error threshold
            train_predictions = self.algorithms["autoencoder"].predict(X_train)
            reconstruction_errors = np.mean(np.square(X_train - train_predictions), axis=1)
            self.thresholds["autoencoder"] = np.percentile(
                reconstruction_errors,
                self.thresholds["autoencoder"] * 100
            )
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Predict anomalies using all enabled algorithms.
        
        Args:
            X: Input data to analyze
            
        Returns:
            Tuple of (combined predictions, individual algorithm predictions)
        """
        predictions = {}
        
        # Statistical detection
        if "statistical" in self.algorithms:
            X_scaled = self.algorithms["statistical"]["scaler"].transform(X)
            z_scores = np.max(np.abs(X_scaled), axis=1)
            predictions["statistical"] = z_scores > self.algorithms["statistical"]["threshold"]
        
        # Isolation Forest
        if "isolation_forest" in self.algorithms:
            # Convert to 1 for inliers and 0 for outliers
            predictions["isolation_forest"] = self.algorithms["isolation_forest"].predict(X) == -1
        
        # Autoencoder
        if "autoencoder" in self.algorithms:
            reconstructed = self.algorithms["autoencoder"].predict(X)
            reconstruction_errors = np.mean(np.square(X - reconstructed), axis=1)
            predictions["autoencoder"] = reconstruction_errors > self.thresholds["autoencoder"]
        
        # Combine predictions (majority voting)
        combined = np.zeros(len(X), dtype=bool)
        for pred in predictions.values():
            combined = combined | pred
        
        return combined, predictions
    
    def save_models(self, save_dir: Union[str, Path]) -> None:
        """
        Save trained models to disk.
        
        Args:
            save_dir: Directory to save models
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save statistical model
        if "statistical" in self.algorithms:
            np.save(
                save_dir / "statistical_scaler.npy",
                self.algorithms["statistical"]["scaler"].get_params()
            )
        
        # Save Isolation Forest
        if "isolation_forest" in self.algorithms:
            import joblib
            joblib.dump(
                self.algorithms["isolation_forest"],
                save_dir / "isolation_forest.joblib"
            )
        
        # Save Autoencoder
        if "autoencoder" in self.algorithms:
            self.algorithms["autoencoder"].save(save_dir / "autoencoder")
            np.save(
                save_dir / "autoencoder_threshold.npy",
                self.thresholds["autoencoder"]
            )
    
    def load_models(self, load_dir: Union[str, Path]) -> None:
        """
        Load trained models from disk.
        
        Args:
            load_dir: Directory containing saved models
        """
        load_dir = Path(load_dir)
        
        # Load statistical model
        if "statistical" in self.algorithms:
            params = np.load(load_dir / "statistical_scaler.npy", allow_pickle=True)
            self.algorithms["statistical"]["scaler"].set_params(**params.item())
        
        # Load Isolation Forest
        if "isolation_forest" in self.algorithms:
            import joblib
            self.algorithms["isolation_forest"] = joblib.load(
                load_dir / "isolation_forest.joblib"
            )
        
        # Load Autoencoder
        if "autoencoder" in self.algorithms:
            self.algorithms["autoencoder"] = tf.keras.models.load_model(
                load_dir / "autoencoder"
            )
            self.thresholds["autoencoder"] = np.load(
                load_dir / "autoencoder_threshold.npy"
            ) 