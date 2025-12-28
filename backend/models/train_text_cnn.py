# ========================
# TEXT CNN TRAINING
# ========================

import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.preprocessing.text import Tokenizer as KerasTokenizer
from keras.preprocessing.sequence import pad_sequences
import os

from datasets.huggingface_loader import HuggingFaceLoader
from preprocessing.text_cleaner import TextCleaner

class TextCNNTrainer:
    """
    Purpose: Optional CNN training
    Allowed: Text-only CNN
    Forbidden: API exposure, runtime training
    """
    
    def __init__(self, max_len=200, vocab_size=10000, embedding_dim=100):
        self.max_len = max_len
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.model = None
        self.tokenizer = None
        self.text_cleaner = TextCleaner()
    
    def build_model(self):
        """Build Text CNN architecture"""
        model = Sequential([
            Embedding(self.vocab_size, self.embedding_dim, input_length=self.max_len),
            Conv1D(128, 5, activation='relu'),
            GlobalMaxPooling1D(),
            Dense(64, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def prepare_data(self):
        """Load and prepare text data"""
        print("Loading DiFraud dataset...")
        loader = HuggingFaceLoader()
        df = loader.load_twitter_rumours(max_samples=5000)
        
        # Clean texts
        texts = [self.text_cleaner.clean(str(t)) for t in df['text']]
        labels = df['label'].values
        
        # Tokenize
        self.tokenizer = KerasTokenizer(num_words=self.vocab_size)
        self.tokenizer.fit_on_texts(texts)
        
        sequences = self.tokenizer.texts_to_sequences(texts)
        X = pad_sequences(sequences, maxlen=self.max_len)
        
        return X, labels
    
    def train(self, X, y, epochs=10, batch_size=32):
        """Train Text CNN"""
        from sklearn.model_selection import train_test_split
        
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        if self.model is None:
            self.build_model()
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        return history
    
    def save_model(self, path='models/saved/text_cnn.h5'):
        """Save trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        
        # Save tokenizer
        import pickle
        with open(path.replace('.h5', '_tokenizer.pkl'), 'wb') as f:
            pickle.dump(self.tokenizer, f)
        
        print(f"Model saved to {path}")
    
    def run_training_pipeline(self):
        """Complete training pipeline"""
        X, y = self.prepare_data()
        self.build_model()
        self.train(X, y)
        self.save_model()
        print("Training complete!")


if __name__ == '__main__':
    trainer = TextCNNTrainer()
    trainer.run_training_pipeline()
