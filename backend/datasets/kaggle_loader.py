# ========================
# KAGGLE DATASET LOADER (EMSCAD)
# ========================

import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

class KaggleLoader:
    """
    Purpose: Load EMSCAD dataset via Kaggle API
    Allowed: Streaming, parsing
    Forbidden: Local file persistence, dataset substitution
    """
    
    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()
        self.dataset_name = 'shivamb/real-or-fake-fake-jobposting-prediction'
    
    def load_dataset(self, max_rows=None):
        """
        Load EMSCAD dataset from Kaggle
        
        Args:
            max_rows: Maximum rows to load (None = all)
        
        Returns:
            pandas.DataFrame: Loaded dataset
        """
        try:
            # Download dataset files to temp location
            self.api.dataset_download_files(
                self.dataset_name,
                path='temp_kaggle',
                unzip=True
            )
            
            # Load CSV
            df = pd.read_csv('temp_kaggle/fake_job_postings.csv', nrows=max_rows)
            
            # Clean up temp files
            import shutil
            shutil.rmtree('temp_kaggle', ignore_errors=True)
            
            return df
            
        except Exception as e:
            raise Exception(f"Kaggle dataset load failed: {str(e)}")
    
    def get_sample(self, n=1000):
        """
        Get sample of dataset
        
        Args:
            n: Number of samples
        
        Returns:
            pandas.DataFrame: Sample dataset
        """
        df = self.load_dataset(max_rows=n)
        return df.sample(n=min(n, len(df)))
