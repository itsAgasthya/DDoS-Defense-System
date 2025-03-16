#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path

import kagglehub
import pandas as pd
from tqdm import tqdm

from src.utils.logger import setup_logging
from src.utils.data_loader import CICDDoS2019Loader

def parse_args():
    parser = argparse.ArgumentParser(description="Download and prepare CICDDoS2019 dataset")
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data",
        help="Directory to store the dataset"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force download even if files exist"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(logging.INFO)
    logger = logging.getLogger(__name__)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Downloading CICDDoS2019 dataset...")
    try:
        data_path = kagglehub.dataset_download(
            "dhoogla/cicddos2019",
            force=args.force
        )
        logger.info(f"Dataset downloaded to: {data_path}")
        
        # Initialize the data loader
        loader = CICDDoS2019Loader(data_path)
        
        # Load and analyze both days
        for day in ["01-12", "03-11"]:
            logger.info(f"\nAnalyzing day {day}:")
            df = loader.load_data(day)
            
            # Print basic statistics
            logger.info(f"Total samples: {len(df):,}")
            
            # Get attack distribution
            distribution = loader.get_attack_distribution(df)
            logger.info("\nAttack distribution:")
            for attack_type, count in distribution.items():
                percentage = (count / len(df)) * 100
                logger.info(f"{attack_type}: {count:,} ({percentage:.2f}%)")
        
        # Save feature names for reference
        features = loader.get_feature_names()
        feature_file = output_dir / "features.txt"
        with open(feature_file, "w") as f:
            f.write("\n".join(features))
        logger.info(f"\nFeature names saved to: {feature_file}")
        
        logger.info("\nDataset preparation completed successfully!")
        
    except Exception as e:
        logger.error(f"Error preparing dataset: {str(e)}")
        raise

if __name__ == "__main__":
    main() 