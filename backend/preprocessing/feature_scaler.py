# ========================
# FEATURE SCALER
# ========================

import numpy as np
from typing import List, Union

class FeatureScaler:
    """
    Purpose: Normalize numeric features
    Allowed: Min-max, standard scaling
    Forbidden: ML logic, model training
    """
    
    def __init__(self, method='minmax'):
        self.method = method  # 'minmax' or 'standard'
        self.min_vals = None
        self.max_vals = None
        self.mean_vals = None
        self.std_vals = None
    
    def fit(self, data: np.ndarray):
        """
        Fit scaler to data
        
        Args:
            data: numpy array of features
        """
        if self.method == 'minmax':
            self.min_vals = np.min(data, axis=0)
            self.max_vals = np.max(data, axis=0)
        elif self.method == 'standard':
            self.mean_vals = np.mean(data, axis=0)
            self.std_vals = np.std(data, axis=0)
    
    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Transform data using fitted scaler
        
        Args:
            data: numpy array of features
        
        Returns:
            np.ndarray: Scaled features
        """
        if self.method == 'minmax':
            if self.min_vals is None or self.max_vals is None:
                raise ValueError("Scaler not fitted. Call fit() first.")
            
            # Avoid division by zero
            range_vals = self.max_vals - self.min_vals
            range_vals[range_vals == 0] = 1
            
            return (data - self.min_vals) / range_vals
        
        elif self.method == 'standard':
            if self.mean_vals is None or self.std_vals is None:
                raise ValueError("Scaler not fitted. Call fit() first.")
            
            # Avoid division by zero
            std_vals = self.std_vals.copy()
            std_vals[std_vals == 0] = 1
            
            return (data - self.mean_vals) / std_vals
    
    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Fit and transform in one step
        
        Args:
            data: numpy array of features
        
        Returns:
            np.ndarray: Scaled features
        """
        self.fit(data)
        return self.transform(data)
    
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Reverse scaling transformation
        
        Args:
            data: Scaled features
        
        Returns:
            np.ndarray: Original scale features
        """
        if self.method == 'minmax':
            range_vals = self.max_vals - self.min_vals
            return data * range_vals + self.min_vals
        elif self.method == 'standard':
            return data * self.std_vals + self.mean_vals
