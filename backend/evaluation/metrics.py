# ========================
# EVALUATION METRICS
# ========================

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns

class MetricsCalculator:
    """
    Purpose: Performance metrics
    Allowed: Accuracy, precision, recall
    Forbidden: Visualization unless asked
    """
    
    def __init__(self):
        pass
    
    def calculate_all_metrics(self, y_true, y_pred, y_prob=None):
        """
        Calculate all classification metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities (optional)
        
        Returns:
            dict: All metrics
        """
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        metrics['precision'] = precision_score(y_true, y_pred, average='binary')
        metrics['recall'] = recall_score(y_true, y_pred, average='binary')
        metrics['f1_score'] = f1_score(y_true, y_pred, average='binary')
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        metrics['true_negatives'] = int(cm[0, 0])
        metrics['false_positives'] = int(cm[0, 1])
        metrics['false_negatives'] = int(cm[1, 0])
        metrics['true_positives'] = int(cm[1, 1])
        
        # ROC-AUC if probabilities provided
        if y_prob is not None:
            try:
                metrics['roc_auc'] = roc_auc_score(y_true, y_prob)
            except:
                metrics['roc_auc'] = None
        
        return metrics
    
    def print_metrics_report(self, y_true, y_pred):
        """Print formatted metrics report"""
        print("\n" + "="*50)
        print("CLASSIFICATION METRICS REPORT")
        print("="*50)
        
        metrics = self.calculate_all_metrics(y_true, y_pred)
        
        print(f"\nAccuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1_score']:.4f}")
        
        print("\nConfusion Matrix:")
        print(f"TN: {metrics['true_negatives']:5d}  FP: {metrics['false_positives']:5d}")
        print(f"FN: {metrics['false_negatives']:5d}  TP: {metrics['true_positives']:5d}")
        
        print("\n" + "="*50)
        
        return metrics
    
    def calculate_class_wise_metrics(self, y_true, y_pred):
        """Calculate metrics for each class"""
        report = classification_report(y_true, y_pred, output_dict=True)
        return report
    
    def plot_confusion_matrix(self, y_true, y_pred, save_path=None):
        """
        Plot confusion matrix
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            save_path: Path to save plot (optional)
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Fraud', 'Legit'],
                   yticklabels=['Fraud', 'Legit'])
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.title('Confusion Matrix')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_roc_curve(self, y_true, y_prob, save_path=None):
        """
        Plot ROC curve
        
        Args:
            y_true: True labels
            y_prob: Predicted probabilities
            save_path: Path to save plot (optional)
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_prob)
        auc = roc_auc_score(y_true, y_prob)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.3f})', linewidth=2)
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        plt.grid(alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def compare_models(self, results_dict):
        """
        Compare multiple models
        
        Args:
            results_dict: {model_name: {y_true, y_pred}}
        
        Returns:
            DataFrame: Comparison table
        """
        import pandas as pd
        
        comparison = []
        
        for model_name, data in results_dict.items():
            metrics = self.calculate_all_metrics(data['y_true'], data['y_pred'])
            comparison.append({
                'Model': model_name,
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1 Score': metrics['f1_score']
            })
        
        df = pd.DataFrame(comparison)
        return df
