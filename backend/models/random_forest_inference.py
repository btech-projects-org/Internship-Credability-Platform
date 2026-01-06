# ========================
# RANDOM FOREST INFERENCE
# ========================

import joblib
import numpy as np
import os

class RandomForestPredictor:
    """
    Purpose: RF prediction
    Allowed: Model loading, inference
    Forbidden: Training
    """
    
    def __init__(self, model_path='models/saved/random_forest.pkl'):
        self.model = None
        self.scaler = None
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model"""
        if os.path.exists(self.model_path):
            try:
                checkpoint = joblib.load(self.model_path)
                self.model = checkpoint['model']
                self.scaler = checkpoint['scaler']
                print(f"Model loaded from {self.model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
                self.scaler = None
        else:
            print(f"Model not found at {self.model_path}")
    
    def predict(self, features: np.ndarray) -> int:
        """
        Predict credibility class
        
        Args:
            features: Feature vector
        
        Returns:
            int: Prediction (0=fraud, 1=legit)
        """
        if self.model is None:
            return 1  # Default to legit if model not loaded
        
        try:
            # Ensure 2D array
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)[0]
            
            return int(prediction)
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return 1
    
    def predict_proba(self, features: np.ndarray) -> np.ndarray:
        """
        Predict probability distribution
        
        Args:
            features: Feature vector
        
        Returns:
            np.ndarray: Probability for each class
        """
        if self.model is None:
            return np.array([0.5, 0.5])
        
        try:
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            features_scaled = self.scaler.transform(features)
            probas = self.model.predict_proba(features_scaled)[0]
            
            return probas
            
        except Exception as e:
            print(f"Probability prediction error: {e}")
            return np.array([0.5, 0.5])
    
    def batch_predict(self, features_list: list) -> list:
        """
        Batch prediction
        
        Args:
            features_list: List of feature vectors
        
        Returns:
            list: Predictions
        """
        if self.model is None:
            return [1] * len(features_list)
        
        try:
            features_array = np.array(features_list)
            features_scaled = self.scaler.transform(features_array)
            predictions = self.model.predict(features_scaled)
            
            return predictions.tolist()
            
        except Exception as e:
            print(f"Batch prediction error: {e}")
            return [1] * len(features_list)
