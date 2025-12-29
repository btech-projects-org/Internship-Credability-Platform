#!/usr/bin/env python3
# ========================
# GENERATE STUB MODELS
# Creates placeholder trained models for demo
# ========================

import sys
import joblib
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle

def create_random_forest_stub():
    """Create a minimal trained Random Forest for demo"""
    print("Creating Random Forest stub model...")
    
    # Create a simple dummy model (not actually trained on real data)
    X_dummy = np.random.rand(100, 20)  # 20 features
    y_dummy = np.random.randint(0, 2, 100)
    
    rf = RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=1)
    rf.fit(X_dummy, y_dummy)
    
    scaler = StandardScaler()
    scaler.fit(X_dummy)
    
    checkpoint = {
        'model': rf,
        'scaler': scaler
    }
    
    model_dir = Path(__file__).parent / 'saved'
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / 'random_forest.pkl'
    
    joblib.dump(checkpoint, str(model_path))
    print(f"  ✓ Random Forest saved to {model_path}")

def create_text_cnn_stub():
    """Create a stub Text CNN tokenizer for demo"""
    print("Creating Text CNN stub tokenizer...")
    
    # Create a minimal tokenizer
    try:
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense
        
        # Create tokenizer
        tokenizer = Tokenizer(num_words=1000, oov_token='<OOV>')
        dummy_texts = ['this is a sample text'] * 50
        tokenizer.fit_on_texts(dummy_texts)
        
        model_dir = Path(__file__).parent / 'saved'
        model_dir.mkdir(parents=True, exist_ok=True)
        tokenizer_path = model_dir / 'text_cnn_tokenizer.pkl'
        
        with open(str(tokenizer_path), 'wb') as f:
            pickle.dump(tokenizer, f)
        
        print(f"  ✓ Text CNN tokenizer saved to {tokenizer_path}")
        
        # Create a simple CNN model
        model = Sequential([
            Embedding(1000, 32, input_length=200),
            Conv1D(64, 5, activation='relu'),
            GlobalMaxPooling1D(),
            Dense(1, activation='sigmoid')
        ])
        model.compile(loss='binary_crossentropy', optimizer='adam')
        
        model_path = model_dir / 'text_cnn.h5'
        model.save(str(model_path))
        print(f"  ✓ Text CNN model saved to {model_path}")
        
    except ImportError:
        print("  ⚠ TensorFlow not available; Text CNN model skipped")
        print("    (Random Forest inference will be used as fallback)")

if __name__ == '__main__':
    print()
    print("=" * 60)
    print("  STUB MODEL GENERATION")
    print("=" * 60)
    print()
    
    try:
        create_random_forest_stub()
        create_text_cnn_stub()
        
        print()
        print("=" * 60)
        print("  SUCCESS")
        print("=" * 60)
        print()
        print("Stub models created. Ready for demo/testing.")
        print()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
