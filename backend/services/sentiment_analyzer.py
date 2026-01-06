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
            # If AI model fails, use simple heuristic-based sentiment
            print(f"[WARNING] Sentiment AI model failed: {e}")
            print(f"[INFO] Using heuristic-based sentiment analysis instead")
            return self._heuristic_sentiment(text)
    
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
    
    def _heuristic_sentiment(self, text: str) -> Dict:
        """
        Simple heuristic-based sentiment when AI model unavailable
        Analyzes based on positive/negative keywords and structure
        """
        text_lower = text.lower()
        
        # Positive indicators for professional internship postings
        positive_words = [
            'opportunity', 'growth', 'learn', 'mentorship', 'hands-on',
            'experience', 'develop', 'gain', 'professional', 'team',
            'innovative', 'exciting', 'excellent', 'great', 'outstanding',
            'career', 'advancement', 'training', 'skills', 'collaborative',
            'dynamic', 'cutting-edge', 'industry', 'expert', 'comprehensive'
        ]
        
        # Negative indicators
        negative_words = [
            'scam', 'fraud', 'fake', 'payment required', 'pay upfront',
            'suspicious', 'unclear', 'vague', 'confusing', 'unprofessional',
            'urgent', 'act now', 'limited time', 'guarantee', 'no experience needed'
        ]
        
        # Count occurrences
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Length check (professional postings are detailed)
        word_count = len(text.split())
        has_good_length = 50 <= word_count <= 1000
        
        # Determine sentiment
        if negative_count > 2:
            return {'label': 'NEGATIVE', 'score': 0.7, 'sentiment_class': 0, 'method': 'heuristic'}
        elif positive_count >= 5 and has_good_length:
            # Professional, detailed posting with positive words
            confidence = min(0.9, 0.6 + (positive_count * 0.05))
            return {'label': 'POSITIVE', 'score': confidence, 'sentiment_class': 1, 'method': 'heuristic'}
        elif positive_count >= 2:
            # Some positive indicators
            return {'label': 'POSITIVE', 'score': 0.65, 'sentiment_class': 1, 'method': 'heuristic'}
        else:
            # Neutral/professional tone
            return {'label': 'NEUTRAL', 'score': 0.7, 'sentiment_class': 2, 'method': 'heuristic'}
