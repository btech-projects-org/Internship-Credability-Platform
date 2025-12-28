# ========================
# SENTIMENT ANALYZER
# ========================

from typing import List, Dict

class SentimentAnalyzer:
    """
    Purpose: Sentiment scoring
    Allowed: Batch sentiment inference
    Forbidden: Final decision logic, training
    """
    
    def __init__(self):
        # Lazy load model on first use to speed up app startup
        self.model = None
    
    def _ensure_model_loaded(self):
        """Load model if not already loaded"""
        if self.model is None:
            from transformers import pipeline
            self.model = pipeline('sentiment-analysis', 
                                 model='distilbert-base-uncased-finetuned-sst-2-english')
    
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of single text
        
        Args:
            text: Input text
        
        Returns:
            dict: Sentiment result with label and score
        """
        if not text or not isinstance(text, str):
            return {'label': 'NEUTRAL', 'score': 0.5}
        
        try:
            self._ensure_model_loaded()
            # Truncate to model's max length
            text = text[:512]
            
            result = self.model(text)[0]
            
            return {
                'label': result['label'],
                'score': float(result['score']),
                'sentiment_class': self._map_to_class(result['label'])
            }
        except Exception as e:
            return {'error': str(e), 'label': 'NEUTRAL', 'score': 0.5}
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts: List of texts
        
        Returns:
            List[dict]: Sentiment results
        """
        if not texts:
            return []
        
        try:
            self._ensure_model_loaded()
            # Truncate all texts
            texts = [t[:512] if t else "" for t in texts]
            
            results = self.model(texts)
            
            return [
                {
                    'label': r['label'],
                    'score': float(r['score']),
                    'sentiment_class': self._map_to_class(r['label'])
                }
                for r in results
            ]
        except Exception as e:
            return [{'error': str(e)} for _ in texts]
    
    def _map_to_class(self, label: str) -> int:
        """Map sentiment label to numeric class"""
        mapping = {
            'POSITIVE': 1,
            'NEGATIVE': 0,
            'NEUTRAL': 2
        }
        return mapping.get(label.upper(), 2)
    
    def get_polarity_score(self, text: str) -> float:
        """
        Get polarity score (-1 to 1)
        
        Args:
            text: Input text
        
        Returns:
            float: Polarity score
        """
        result = self.analyze(text)
        
        if result['label'] == 'POSITIVE':
            return result['score']
        elif result['label'] == 'NEGATIVE':
            return -result['score']
        else:
            return 0.0
