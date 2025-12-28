# ========================
# RANDOM FOREST TRAINING
# ========================

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

from datasets.kaggle_loader import KaggleLoader
from preprocessing.text_cleaner import TextCleaner
from preprocessing.feature_scaler import FeatureScaler

class RandomForestTrainer:
    """
    Purpose: Train RF model
    Allowed: Offline training
    Forbidden: Runtime imports, API exposure
    """
    
    def __init__(self):
        self.model = None
        self.scaler = FeatureScaler(method='standard')
        self.text_cleaner = TextCleaner()
    
    def load_and_prepare_data(self):
        """Load dataset and prepare features"""
        print("Loading EMSCAD dataset from Kaggle...")
        loader = KaggleLoader()
        df = loader.load_dataset(max_rows=10000)  # Limit for training speed
        
        print(f"Loaded {len(df)} samples")
        
        # Feature engineering
        features = self._engineer_features(df)
        labels = df['fraudulent'].values if 'fraudulent' in df.columns else df['target'].values
        
        return features, labels
    
    def _engineer_features(self, df: pd.DataFrame) -> np.ndarray:
        """Engineer features from dataset"""
        features_list = []
        
        for _, row in df.iterrows():
            feat = []
            
            # Text length features
            feat.append(len(str(row.get('title', ''))))
            feat.append(len(str(row.get('description', ''))))
            feat.append(len(str(row.get('requirements', ''))))
            feat.append(len(str(row.get('benefits', ''))))
            
            # Has features
            feat.append(1 if row.get('company_logo') else 0)
            feat.append(1 if row.get('has_company_logo') else 0)
            feat.append(1 if row.get('has_questions') else 0)
            
            # Salary features
            feat.append(float(row.get('salary_range', 0) or 0))
            feat.append(1 if row.get('telecommuting') else 0)
            
            # Experience level (ordinal encoding)
            exp_level = row.get('required_experience', 'Unknown')
            exp_map = {'Entry level': 0, 'Mid-Senior level': 1, 'Executive': 2, 'Unknown': -1}
            feat.append(exp_map.get(exp_level, -1))
            
            features_list.append(feat)
        
        return np.array(features_list)
    
    def train(self, X, y):
        """Train Random Forest model"""
        print("Splitting data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Training Random Forest...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Training accuracy: {train_score:.4f}")
        print(f"Test accuracy: {test_score:.4f}")
        
        return train_score, test_score
    
    def save_model(self, path='models/saved/random_forest.pkl'):
        """Save trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, path)
        print(f"Model saved to {path}")
    
    def run_training_pipeline(self):
        """Complete training pipeline"""
        X, y = self.load_and_prepare_data()
        self.train(X, y)
        self.save_model()
        print("Training complete!")


if __name__ == '__main__':
    trainer = RandomForestTrainer()
    trainer.run_training_pipeline()
