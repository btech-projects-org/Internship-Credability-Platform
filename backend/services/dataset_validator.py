# ========================
# DATASET VALIDATOR SERVICE
# ========================

import os
from typing import Dict, Any, List, Tuple
import json

class DatasetValidator:
    """
    Validates user data against HuggingFace and Kaggle datasets.
    Checks against known legitimate companies and scam patterns.
    """
    
    def __init__(self):
        self.hf_api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.kaggle_username = os.getenv("KAGGLE_USERNAME", "")
        self.kaggle_key = os.getenv("KAGGLE_KEY", "")
        
        # Cached datasets
        self.legitimate_companies = set()
        self.scam_companies = set()
        self.scam_patterns = []
        
        self._initialize_datasets()
    
    def _initialize_datasets(self):
        """Initialize datasets from HuggingFace and Kaggle"""
        print("[INFO] Initializing dataset validation...")
        
        # Try to load from HuggingFace
        if self.hf_api_key:
            self._load_huggingface_datasets()
        else:
            print("[WARNING] HUGGINGFACE_API_KEY not set. Skipping HF dataset validation.")
        
        # Try to load from Kaggle
        if self.kaggle_username and self.kaggle_key:
            self._load_kaggle_datasets()
        else:
            print("[WARNING] KAGGLE credentials not set. Skipping Kaggle dataset validation.")
        
        # Load local dataset if available
        self._load_local_datasets()
    
    def _load_huggingface_datasets(self):
        """Load datasets from HuggingFace Hub"""
        try:
            from datasets import load_dataset
            
            print("[DEBUG] Loading HuggingFace datasets...")
            
            # Load legitimate companies dataset
            try:
                # Dataset with verified/legitimate companies
                legitimate_ds = load_dataset(
                    "datasets/legitimate_companies",
                    split="train",
                    use_auth_token=self.hf_api_key
                )
                self.legitimate_companies = set(
                    [item['company_name'].lower() for item in legitimate_ds if 'company_name' in item]
                )
                print(f"[SUCCESS] Loaded {len(self.legitimate_companies)} legitimate companies from HuggingFace")
            except Exception as e:
                print(f"[WARNING] Could not load legitimate companies dataset: {e}")
            
            # Load scam patterns dataset
            try:
                scam_ds = load_dataset(
                    "datasets/internship_scams",
                    split="train",
                    use_auth_token=self.hf_api_key
                )
                self.scam_patterns = [
                    {
                        'pattern': item.get('scam_indicator'),
                        'severity': item.get('severity', 'medium'),
                        'description': item.get('description', '')
                    }
                    for item in scam_ds if 'scam_indicator' in item
                ]
                print(f"[SUCCESS] Loaded {len(self.scam_patterns)} scam patterns from HuggingFace")
            except Exception as e:
                print(f"[WARNING] Could not load scam patterns dataset: {e}")
        
        except ImportError:
            print("[WARNING] datasets library not installed. Install with: pip install datasets")
        except Exception as e:
            print(f"[ERROR] Failed to load HuggingFace datasets: {e}")
    
    def _load_kaggle_datasets(self):
        """Load datasets from Kaggle"""
        try:
            import kaggle
            from kaggle.api.kaggle_api_extended import KaggleApi
            
            print("[DEBUG] Authenticating with Kaggle...")
            
            api = KaggleApi()
            api.authenticate()
            
            # Download verified companies dataset
            try:
                print("[DEBUG] Downloading Kaggle internship datasets...")
                # Example: Download internship scams dataset
                api.dataset_download_files(
                    'mrisdal/internship-scams',
                    path='backend/data/kaggle',
                    unzip=True
                )
                print("[SUCCESS] Downloaded Kaggle internship datasets")
                
                # Parse downloaded data
                self._parse_kaggle_data()
            except Exception as e:
                print(f"[WARNING] Could not download Kaggle dataset: {e}")
        
        except ImportError:
            print("[WARNING] kaggle library not installed. Install with: pip install kaggle")
        except Exception as e:
            print(f"[ERROR] Failed to load Kaggle datasets: {e}")
    
    def _parse_kaggle_data(self):
        """Parse downloaded Kaggle data"""
        try:
            import csv
            import pandas as pd
            
            kaggle_path = 'backend/data/kaggle'
            
            # Try to read CSV files from Kaggle
            for filename in os.listdir(kaggle_path):
                if filename.endswith('.csv'):
                    filepath = os.path.join(kaggle_path, filename)
                    try:
                        df = pd.read_csv(filepath)
                        
                        # Look for company and scam information
                        if 'company_name' in df.columns:
                            self.scam_companies.update(
                                df[df['is_scam'] == True]['company_name'].str.lower().tolist()
                            )
                        
                        print(f"[SUCCESS] Parsed {filename}")
                    except Exception as e:
                        print(f"[WARNING] Could not parse {filename}: {e}")
        
        except Exception as e:
            print(f"[WARNING] Error parsing Kaggle data: {e}")
    
    def _load_local_datasets(self):
        """Load local JSON datasets if available"""
        try:
            local_paths = [
                'backend/data/legitimate_companies.json',
                'backend/data/scam_companies.json',
                'backend/data/scam_patterns.json'
            ]
            
            for path in local_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        data = json.load(f)
                        
                        if 'legitimate_companies' in path:
                            self.legitimate_companies = set(
                                [c.lower() for c in data.get('companies', [])]
                            )
                            print(f"[SUCCESS] Loaded {len(self.legitimate_companies)} local companies")
                        
                        elif 'scam_companies' in path:
                            self.scam_companies = set(
                                [c.lower() for c in data.get('companies', [])]
                            )
                            print(f"[SUCCESS] Loaded {len(self.scam_companies)} known scam companies")
                        
                        elif 'scam_patterns' in path:
                            self.scam_patterns = data.get('patterns', [])
                            print(f"[SUCCESS] Loaded {len(self.scam_patterns)} scam patterns")
        
        except Exception as e:
            print(f"[WARNING] Error loading local datasets: {e}")
    
    def validate_against_datasets(self, company_name: str, email: str = "", 
                                 job_desc: str = "") -> Dict[str, Any]:
        """
        Validate user data against datasets
        
        Args:
            company_name (str): Company name to validate
            email (str): Contact email
            job_desc (str): Job description
        
        Returns:
            dict: Validation results
        """
        results = {
            'company_validated': False,
            'in_legitimate_dataset': False,
            'in_scam_dataset': False,
            'matching_patterns': [],
            'dataset_confidence_score': 0.5,
            'checks_performed': [],
            'warnings': []
        }
        
        company_lower = company_name.lower().strip()
        
        try:
            # Check against legitimate companies
            if self.legitimate_companies:
                results['checks_performed'].append('legitimate_company_check')
                
                if company_lower in self.legitimate_companies:
                    results['in_legitimate_dataset'] = True
                    results['dataset_confidence_score'] += 0.3
                    results['warnings'].append(f"✓ {company_name} found in verified companies dataset")
                    print(f"[DEBUG] {company_name} verified in legitimate dataset")
            
            # Check against known scam companies
            if self.scam_companies:
                results['checks_performed'].append('scam_company_check')
                
                if company_lower in self.scam_companies:
                    results['in_scam_dataset'] = True
                    results['dataset_confidence_score'] -= 0.4
                    results['warnings'].append(f"⚠️ {company_name} found in known scam companies dataset")
                    print(f"[WARNING] {company_name} found in scam dataset!")
            
            # Check job description against scam patterns
            if self.scam_patterns and job_desc:
                results['checks_performed'].append('scam_pattern_check')
                
                job_desc_lower = job_desc.lower()
                
                for pattern_item in self.scam_patterns:
                    pattern = pattern_item.get('pattern', '').lower()
                    
                    if pattern and pattern in job_desc_lower:
                        results['matching_patterns'].append({
                            'pattern': pattern,
                            'severity': pattern_item.get('severity', 'medium'),
                            'description': pattern_item.get('description', '')
                        })
                        
                        severity_weight = {
                            'critical': 0.3,
                            'high': 0.2,
                            'medium': 0.1,
                            'low': 0.05
                        }
                        
                        weight = severity_weight.get(
                            pattern_item.get('severity', 'medium'), 0.1
                        )
                        results['dataset_confidence_score'] -= weight
            
            # Check email domain against dataset
            if email and '@' in email:
                results['checks_performed'].append('email_domain_check')
                
                domain = email.split('@')[1].lower()
                
                # Check if email domain matches known scam domains
                scam_domains = {
                    'tempmail.com', 'guerrillamail.com', 'mailinator.com',
                    '10minutemail.com', 'throwaway.email'
                }
                
                if domain in scam_domains:
                    results['dataset_confidence_score'] -= 0.2
                    results['warnings'].append(f"⚠️ Temporary email domain detected: {domain}")
                    print(f"[WARNING] Temporary email domain: {domain}")
            
            results['company_validated'] = (
                results['in_legitimate_dataset'] or 
                len(results['checks_performed']) > 0
            )
            
            # Clamp confidence score between 0 and 1
            results['dataset_confidence_score'] = max(
                0.0, 
                min(1.0, results['dataset_confidence_score'])
            )
        
        except Exception as e:
            print(f"[ERROR] Dataset validation failed: {e}")
            results['warnings'].append(f"Dataset validation error: {str(e)}")
        
        return results
    
    def refresh_datasets(self):
        """Refresh all datasets"""
        print("[INFO] Refreshing datasets...")
        self.legitimate_companies = set()
        self.scam_companies = set()
        self.scam_patterns = []
        self._initialize_datasets()
