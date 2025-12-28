# ========================
# TEXT CNN INFERENCE
# ========================

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

class TextCNNPredictor:
    """
    Purpose: CNN inference
    Allowed: Feature embedding, prediction
    Forbidden: Training
    """
    
    def __init__(self, model_path='models/saved/text_cnn.h5'):
        self.model = None
        self.tokenizer = None
        self.max_len = 200
        self.model_path = model_path
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained CNN model"""
        if os.path.exists(self.model_path):
            try:
                self.model = load_model(self.model_path)
                
                # Load tokenizer
                tokenizer_path = self.model_path.replace('.h5', '_tokenizer.pkl')
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                
                print(f"CNN model loaded from {self.model_path}")
            except Exception as e:
                print(f"Error loading CNN model: {e}")
                self.model = None
        else:
            print(f"CNN model not found at {self.model_path}")
    
    def predict(self, text: str) -> float:
        """
        Predict credibility score for text
        
        Args:
            text: Input text
        
        Returns:
            float: Credibility score (0-1)
        """
        if self.model is None or self.tokenizer is None:
            return 0.5
        
        try:
            # Tokenize and pad
            sequence = self.tokenizer.texts_to_sequences([text])
            padded = pad_sequences(sequence, maxlen=self.max_len)
            
            # Predict
            prediction = self.model.predict(padded, verbose=0)[0][0]
            
            return float(prediction)
            
        except Exception as e:
            print(f"CNN prediction error: {e}")
            return 0.5
    
    def batch_predict(self, texts: list) -> list:
        """
        Batch prediction
        
        Args:
            texts: List of texts
        
        Returns:
            list: Predictions
        """
        if self.model is None or self.tokenizer is None:
            return [0.5] * len(texts)
        
        try:
            sequences = self.tokenizer.texts_to_sequences(texts)
            padded = pad_sequences(sequences, maxlen=self.max_len)
            
            predictions = self.model.predict(padded, verbose=0)
            
            return [float(p[0]) for p in predictions]
            
        except Exception as e:
            print(f"Batch CNN prediction error: {e}")
            return [0.5] * len(texts)
    
    def get_embeddings(self, text: str) -> np.ndarray:
        """
        Get text embeddings from CNN
        
        Args:
            text: Input text
        
        Returns:
            np.ndarray: Embedding vector
        """
        if self.model is None or self.tokenizer is None:
            return np.zeros(64)
        
        try:
            # Create embedding model (up to pooling layer)
            embedding_model = tf.keras.Model(
                inputs=self.model.input,
                outputs=self.model.layers[-3].output  # Before dense layers
            )
            
            sequence = self.tokenizer.texts_to_sequences([text])
            padded = pad_sequences(sequence, maxlen=self.max_len)
            
            embedding = embedding_model.predict(padded, verbose=0)[0]
            
            return embedding
            
        except Exception as e:
            print(f"Embedding extraction error: {e}")
            return np.zeros(64)
