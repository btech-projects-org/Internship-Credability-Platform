# ========================
# TEXT CLEANING & NORMALIZATION
# ========================

import re
import string
from typing import List

class TextCleaner:
    """
    Purpose: Text normalization
    Allowed: O(n) operations
    Forbidden: Model usage, vectorization
    """
    
    def __init__(self):
        self.stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
            'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was'
        ])
    
    def clean(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
        
        Returns:
            str: Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """
        Remove stop words from text
        
        Args:
            text: Input text
        
        Returns:
            str: Text without stop words
        """
        words = text.split()
        filtered = [w for w in words if w not in self.stop_words]
        return ' '.join(filtered)
    
    def normalize_whitespace(self, text: str) -> str:
        """
        Normalize all whitespace to single spaces
        
        Args:
            text: Input text
        
        Returns:
            str: Normalized text
        """
        return ' '.join(text.split())
    
    def batch_clean(self, texts: List[str]) -> List[str]:
        """
        Clean multiple texts
        
        Args:
            texts: List of texts
        
        Returns:
            List[str]: Cleaned texts
        """
        return [self.clean(text) for text in texts]
