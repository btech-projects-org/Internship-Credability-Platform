# ========================
# TOKENIZER
# ========================

from typing import List

class Tokenizer:
    """
    Purpose: Token generation
    Allowed: Reusable token logic
    Forbidden: Vectorization, model-specific tokenization
    """
    
    def __init__(self, max_len=512):
        self.max_len = max_len
    
    def tokenize(self, text: str) -> List[str]:
        """
        Basic word tokenization
        
        Args:
            text: Input text
        
        Returns:
            List[str]: Tokens
        """
        if not text:
            return []
        
        # Simple whitespace tokenization
        tokens = text.lower().split()
        
        # Truncate to max length
        if len(tokens) > self.max_len:
            tokens = tokens[:self.max_len]
        
        return tokens
    
    def tokenize_chars(self, text: str) -> List[str]:
        """
        Character-level tokenization
        
        Args:
            text: Input text
        
        Returns:
            List[str]: Character tokens
        """
        return list(text[:self.max_len])
    
    def get_vocab(self, texts: List[str]) -> dict:
        """
        Build vocabulary from texts
        
        Args:
            texts: List of texts
        
        Returns:
            dict: Vocabulary {token: index}
        """
        vocab = {'<PAD>': 0, '<UNK>': 1}
        idx = 2
        
        for text in texts:
            tokens = self.tokenize(text)
            for token in tokens:
                if token not in vocab:
                    vocab[token] = idx
                    idx += 1
        
        return vocab
    
    def tokens_to_ids(self, tokens: List[str], vocab: dict) -> List[int]:
        """
        Convert tokens to IDs using vocabulary
        
        Args:
            tokens: List of tokens
            vocab: Vocabulary dict
        
        Returns:
            List[int]: Token IDs
        """
        return [vocab.get(token, vocab['<UNK>']) for token in tokens]
    
    def pad_sequence(self, sequence: List[int], max_len: int = None) -> List[int]:
        """
        Pad sequence to max length
        
        Args:
            sequence: Token ID sequence
            max_len: Maximum length (uses self.max_len if None)
        
        Returns:
            List[int]: Padded sequence
        """
        if max_len is None:
            max_len = self.max_len
        
        if len(sequence) < max_len:
            sequence = sequence + [0] * (max_len - len(sequence))
        else:
            sequence = sequence[:max_len]
        
        return sequence
