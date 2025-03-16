import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class CICDDoS2019Loader:
    """Data loader for the CICDDoS2019 dataset."""
    
    def __init__(self, data_path: Union[str, Path]):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the CICDDoS2019 dataset directory
        """
        self.data_path = Path(data_path)
        self.scaler = StandardScaler()
        
        # Define attack types in the dataset
        self.attack_types = [
            'DrDoS_DNS',
            'DrDoS_LDAP',
            'DrDoS_MSSQL',
            'DrDoS_NetBIOS',
            'DrDoS_NTP',
            'DrDoS_SNMP',
            'DrDoS_SSDP',
            'DrDoS_UDP',
            'Syn',
            'TFTP',
            'UDP-lag',
            'WebDDoS',
            'BENIGN'
        ]
        
    def load_data(self, day: str = "01-12") -> pd.DataFrame:
        """
        Load data for a specific day.
        
        Args:
            day: Day of the dataset ("01-12" or "03-11")
            
        Returns:
            DataFrame containing the day's data
        """
        data_file = self.data_path / f"CSE-CIC-IDS2018_{day}.csv"
        
        if not data_file.exists():
            raise FileNotFoundError(f"Dataset file not found: {data_file}")
        
        # Read CSV with optimized settings
        df = pd.read_csv(
            data_file,
            low_memory=False,
            dtype={
                'Flow ID': 'category',
                'Source IP': 'category',
                'Destination IP': 'category',
                'Timestamp': 'category',
                'Label': 'category'
            }
        )
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess the data for model training.
        
        Args:
            df: Raw DataFrame from the dataset
            
        Returns:
            Tuple of (features, labels)
        """
        # Drop non-numeric columns
        non_numeric_cols = [
            'Flow ID', 'Source IP', 'Source Port',
            'Destination IP', 'Destination Port',
            'Timestamp', 'Protocol', 'Label'
        ]
        X = df.drop(columns=non_numeric_cols)
        
        # Handle missing values
        X = X.fillna(0)
        
        # Scale the features
        X = self.scaler.fit_transform(X)
        
        # Convert labels to numeric
        y = pd.get_dummies(df['Label'])
        
        return X, y.values
    
    def load_and_split(
        self,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Load, preprocess and split the data into train and test sets.
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Load both days of data
        df_day1 = self.load_data("01-12")
        df_day2 = self.load_data("03-11")
        
        # Combine the data
        df = pd.concat([df_day1, df_day2], ignore_index=True)
        
        # Preprocess
        X, y = self.preprocess_data(df)
        
        # Split the data
        return train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )
    
    def get_feature_names(self) -> List[str]:
        """Get the names of the features used in the model."""
        df = self.load_data("01-12")
        non_numeric_cols = [
            'Flow ID', 'Source IP', 'Source Port',
            'Destination IP', 'Destination Port',
            'Timestamp', 'Protocol', 'Label'
        ]
        return [col for col in df.columns if col not in non_numeric_cols]
    
    def get_attack_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Get the distribution of attack types in the dataset.
        
        Args:
            df: DataFrame containing the data
            
        Returns:
            Dictionary mapping attack types to their counts
        """
        return df['Label'].value_counts().to_dict()

# Example usage:
if __name__ == "__main__":
    import kagglehub
    
    # Download the dataset
    data_path = kagglehub.dataset_download("dhoogla/cicddos2019")
    
    # Initialize the loader
    loader = CICDDoS2019Loader(data_path)
    
    # Load and split the data
    X_train, X_test, y_train, y_test = loader.load_and_split()
    
    print("Training set shape:", X_train.shape)
    print("Test set shape:", X_test.shape)
    
    # Get feature names
    features = loader.get_feature_names()
    print("\nFeatures used:", len(features))
    
    # Load a single day's data and get attack distribution
    df = loader.load_data("01-12")
    distribution = loader.get_attack_distribution(df)
    print("\nAttack distribution:")
    for attack_type, count in distribution.items():
        print(f"{attack_type}: {count}") 