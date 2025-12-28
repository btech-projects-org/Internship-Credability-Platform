# ========================
# HUGGING FACE DATASET LOADER (DiFraud)
# ========================

from datasets import load_dataset
import pandas as pd

class HuggingFaceLoader:
    """
    Purpose: Load DiFraud dataset via HuggingFace API
    Allowed: Subset filtering
    Forbidden: Dataset substitution, local storage
    """
    
    def __init__(self):
        self.dataset_name = 'difraud/difraud'
    
    def load_dataset(self, split='train', subset=None):
        """
        Load DiFraud dataset from HuggingFace
        
        Args:
            split: Dataset split ('train', 'test', 'validation')
            subset: Subset name (e.g., 'twitter-rumours')
        
        Returns:
            pandas.DataFrame: Loaded dataset
        """
        try:
            if subset:
                dataset = load_dataset(
                    self.dataset_name,
                    subset,
                    split=split,
                    streaming=False
                )
            else:
                dataset = load_dataset(
                    self.dataset_name,
                    split=split,
                    streaming=False
                )
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(dataset)
            
            return df
            
        except Exception as e:
            raise Exception(f"HuggingFace dataset load failed: {str(e)}")
    
    def load_twitter_rumours(self, max_samples=None):
        """
        Load Twitter Rumours subset specifically
        
        Args:
            max_samples: Maximum samples to load
        
        Returns:
            pandas.DataFrame: Twitter rumours data
        """
        try:
            df = self.load_dataset(split='train', subset='twitter-rumours')
            
            if max_samples and len(df) > max_samples:
                df = df.sample(n=max_samples)
            
            return df
            
        except Exception as e:
            raise Exception(f"Twitter Rumours load failed: {str(e)}")
    
    def stream_dataset(self, split='train'):
        """
        Stream dataset for large-scale processing
        
        Args:
            split: Dataset split
        
        Yields:
            dict: Dataset samples
        """
        dataset = load_dataset(
            self.dataset_name,
            split=split,
            streaming=True
        )
        
        for sample in dataset:
            yield sample
