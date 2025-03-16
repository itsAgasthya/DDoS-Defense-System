#!/usr/bin/env python3

import argparse
import logging
from pathlib import Path

import numpy as np
import yaml
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.logger import setup_logging
from src.utils.config import load_config
from src.utils.data_loader import CICDDoS2019Loader
from src.anomaly_detection.detector import AnomalyDetector

def parse_args():
    parser = argparse.ArgumentParser(description="Train anomaly detection models")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="Path to CICDDoS2019 dataset directory"
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="models/anomaly_detection",
        help="Directory to save trained models"
    )
    parser.add_argument(
        "--plot-dir",
        type=str,
        default="plots",
        help="Directory to save evaluation plots"
    )
    return parser.parse_args()

def plot_confusion_matrix(y_true, y_pred, labels, save_path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        xticklabels=labels,
        yticklabels=labels
    )
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    args = parse_args()
    setup_logging(logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = load_config(args.config)
    
    # Create output directories
    model_dir = Path(args.model_dir)
    plot_dir = Path(args.plot_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize data loader
    logger.info("Loading dataset...")
    data_loader = CICDDoS2019Loader(args.data_dir)
    
    # Load and split data
    X_train, X_test, y_train, y_test = data_loader.load_and_split()
    
    # Convert one-hot encoded labels to binary (attack vs benign)
    y_train_binary = np.any(y_train[:, :-1], axis=1)  # All except last column (BENIGN)
    y_test_binary = np.any(y_test[:, :-1], axis=1)
    
    # Initialize and train anomaly detector
    logger.info("Initializing anomaly detector...")
    detector = AnomalyDetector(config["anomaly_detection"])
    
    logger.info("Training models...")
    detector.train(X_train)
    
    # Save trained models
    logger.info("Saving trained models...")
    detector.save_models(model_dir)
    
    # Evaluate on test set
    logger.info("Evaluating models...")
    y_pred_combined, y_pred_individual = detector.predict(X_test)
    
    # Calculate and print metrics
    logger.info("\nCombined Model Performance:")
    print(classification_report(y_test_binary, y_pred_combined))
    
    # Plot combined confusion matrix
    plot_confusion_matrix(
        y_test_binary,
        y_pred_combined,
        ['Benign', 'Attack'],
        plot_dir / 'confusion_matrix_combined.png'
    )
    
    # Evaluate individual algorithms
    for algo_name, predictions in y_pred_individual.items():
        logger.info(f"\n{algo_name.title()} Model Performance:")
        print(classification_report(y_test_binary, predictions))
        
        # Plot individual confusion matrices
        plot_confusion_matrix(
            y_test_binary,
            predictions,
            ['Benign', 'Attack'],
            plot_dir / f'confusion_matrix_{algo_name}.png'
        )
    
    logger.info(f"\nTraining completed. Models saved to: {model_dir}")
    logger.info(f"Evaluation plots saved to: {plot_dir}")

if __name__ == "__main__":
    main() 