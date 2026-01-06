#!/usr/bin/env python
# ========================
# PIPELINE VALIDATION TEST SCRIPT
# ========================

import sys
import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, List

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import test datasets
from tests.test_datasets import test_cases, test_config

class PipelineValidator:
    """Validates user data through all credibility checking pipelines"""
    
    def __init__(self, backend_url: str = "http://localhost:5000"):
        self.backend_url = backend_url
        self.api_endpoint = test_config['api_endpoint']
        self.timeout = test_config['timeout']
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self):
        """Run all test cases and generate report"""
        print("\n" + "="*80)
        print("INTERNSHIP CREDIBILITY VALIDATION PIPELINE TEST")
        print("="*80)
        print(f"Test Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Backend URL: {self.backend_url}")
        print("="*80 + "\n")
        
        self.start_time = datetime.now()
        
        for case_name, case_data in test_cases.items():
            print(f"\n{'='*80}")
            print(f"TEST CASE: {case_name.upper()}")
            print(f"{'='*80}")
            print(f"Description: {case_data['description']}")
            print(f"Company: {case_data['companyName']}")
            print(f"Email: {case_data['contactEmail']}")
            print(f"Position: {case_data['position']}")
            print(f"Salary: {case_data['salary']}")
            print(f"Duration: {case_data['duration']}")
            
            result = self.test_case(case_name, case_data)
            self.results.append(result)
            
            # Print results
            self._print_result(result)
        
        self.end_time = datetime.now()
        
        # Generate final report
        self._generate_report()
    
    def test_case(self, case_name: str, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Test a single case through the validation pipeline"""
        
        result = {
            'case_name': case_name,
            'description': case_data['description'],
            'status': 'UNKNOWN',
            'pipeline_stages': {},
            'final_score': None,
            'credibility_level': None,
            'errors': [],
            'validation_summary': {}
        }
        
        try:
            # Prepare request data
            request_data = {
                'companyName': case_data['companyName'],
                'contactEmail': case_data['contactEmail'],
                'position': case_data['position'],
                'salary': case_data['salary'],
                'duration': case_data['duration'],
                'jobDescription': case_data['jobDescription'],
                'website': case_data.get('website', '')
            }
            
            print("\n[PIPELINE] Sending request to backend API...")
            
            # Make API request
            url = f"{self.backend_url}{self.api_endpoint}"
            response = requests.post(url, json=request_data, timeout=self.timeout)
            
            if response.status_code == 200:
                api_response = response.json()
                result['status'] = 'SUCCESS'
                result['api_response'] = api_response
                
                # Extract pipeline information
                self._extract_pipeline_info(result, api_response, case_data)
                
            else:
                result['status'] = 'API_ERROR'
                result['errors'].append(f"HTTP {response.status_code}: {response.text}")
                print(f"[ERROR] API returned status {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            result['status'] = 'CONNECTION_ERROR'
            result['errors'].append("Could not connect to backend. Is Flask running?")
            print("[ERROR] Cannot connect to backend at", self.backend_url)
        
        except requests.exceptions.Timeout:
            result['status'] = 'TIMEOUT'
            result['errors'].append(f"Request timeout after {self.timeout} seconds")
            print("[ERROR] Request timeout")
        
        except Exception as e:
            result['status'] = 'ERROR'
            result['errors'].append(str(e))
            print(f"[ERROR] {str(e)}")
        
        return result
    
    def _extract_pipeline_info(self, result: Dict, api_response: Dict, case_data: Dict):
        """Extract information about which pipelines were executed"""
        
        print("\n[PIPELINE] Analyzing response from all validation pipelines...\n")
        
        # 1. Dataset Validation Pipeline
        if 'dataset_validation' in api_response:
            dataset_val = api_response['dataset_validation']
            result['pipeline_stages']['dataset_validation'] = {
                'executed': True,
                'checks_performed': dataset_val.get('checks_performed', []),
                'warnings': dataset_val.get('warnings', []),
                'matching_patterns': dataset_val.get('matching_patterns', []),
                'score_contribution': 0.25
            }
            print(f"✓ DATASET VALIDATION PIPELINE EXECUTED")
            print(f"  - Checks: {', '.join(dataset_val.get('checks_performed', []))}")
            print(f"  - Warnings: {len(dataset_val.get('warnings', []))}")
            print(f"  - Patterns Found: {len(dataset_val.get('matching_patterns', []))}")
        
        # 2. Company Verification Pipeline
        if 'company_verification' in api_response:
            company_ver = api_response['company_verification']
            result['pipeline_stages']['company_verification'] = {
                'executed': True,
                'warnings': company_ver.get('warnings', []),
                'positive_indicators': company_ver.get('positive_indicators', []),
                'score_contribution': 0.35
            }
            print(f"\n✓ COMPANY VERIFICATION PIPELINE EXECUTED")
            print(f"  - Warnings: {len(company_ver.get('warnings', []))}")
            print(f"  - Positive Indicators: {len(company_ver.get('positive_indicators', []))}")
        
        # 3. Breakdown/Scoring Pipeline (contains sentiment, offer quality, etc.)
        if 'breakdown' in api_response:
            breakdown = api_response['breakdown']
            result['pipeline_stages']['sentiment_analysis'] = {
                'executed': 'sentiment_score' in breakdown,
                'score': breakdown.get('sentiment_score', 0),
                'score_contribution': 0.15
            }
            if breakdown.get('sentiment_score') is not None:
                print(f"\n✓ SENTIMENT ANALYSIS PIPELINE EXECUTED")
                print(f"  - Sentiment Score: {breakdown.get('sentiment_score')}")
            
            result['pipeline_stages']['offer_quality'] = {
                'executed': 'offer_quality_score' in breakdown,
                'score': breakdown.get('offer_quality_score', 0),
                'score_contribution': 0.25
            }
            if breakdown.get('offer_quality_score') is not None:
                print(f"\n✓ OFFER QUALITY ASSESSMENT PIPELINE EXECUTED")
                print(f"  - Offer Quality Score: {breakdown.get('offer_quality_score')}")
        
        # 4. Red Flag Detection Pipeline
        if 'red_flags' in api_response:
            red_flags = api_response['red_flags']
            result['pipeline_stages']['red_flag_detection'] = {
                'executed': True,
                'flags_detected': len(red_flags),
                'flags': red_flags
            }
            print(f"\n✓ RED FLAG DETECTION PIPELINE EXECUTED")
            print(f"  - Red Flags Found: {len(red_flags)}")
            if red_flags:
                for key, value in red_flags.items():
                    print(f"    • {key}: {value}")
        
        # 5. Final Scoring Pipeline
        if 'credibility_score' in api_response:
            result['pipeline_stages']['final_scoring'] = {
                'executed': True,
                'final_score': api_response.get('credibility_score'),
                'credibility_level': api_response.get('credibility_level')
            }
            result['final_score'] = api_response.get('credibility_score')
            result['credibility_level'] = api_response.get('credibility_level')
            
            print(f"\n✓ FINAL SCORING PIPELINE EXECUTED")
            print(f"  - Final Credibility Score: {api_response.get('credibility_score'):.2%}")
            print(f"  - Credibility Level: {api_response.get('credibility_level')}")
        
        # Recommendations Pipeline
        if 'recommendations' in api_response:
            result['pipeline_stages']['recommendations'] = {
                'executed': True,
                'count': len(api_response.get('recommendations', []))
            }
            print(f"\n✓ RECOMMENDATIONS PIPELINE EXECUTED")
            print(f"  - Generated {len(api_response.get('recommendations', []))} recommendations")
        
        # Summary
        result['validation_summary'] = {
            'total_pipelines': len(result['pipeline_stages']),
            'executed_pipelines': sum(1 for p in result['pipeline_stages'].values() if p.get('executed')),
            'company_name': case_data['companyName'],
            'expected_result': self._determine_expected_result(case_data['description'])
        }
    
    def _determine_expected_result(self, description: str) -> str:
        """Determine expected result based on case description"""
        if 'scam' in description.lower():
            return 'LOW_CREDIBILITY'
        elif 'legitimate' in description.lower():
            return 'HIGH_CREDIBILITY'
        elif 'borderline' in description.lower():
            return 'MEDIUM_CREDIBILITY'
        else:
            return 'UNKNOWN'
    
    def _print_result(self, result: Dict):
        """Print test result"""
        print("\n" + "-"*80)
        print("PIPELINE EXECUTION SUMMARY:")
        print("-"*80)
        
        if result['status'] == 'SUCCESS':
            print(f"Status: ✓ SUCCESS")
            summary = result['validation_summary']
            print(f"Pipelines Executed: {summary['executed_pipelines']}/{summary['total_pipelines']}")
            print(f"Final Score: {result['final_score']:.2%}")
            print(f"Credibility Level: {result['credibility_level']}")
            print(f"Expected Result: {summary['expected_result']}")
            
            # Pipeline details
            print("\nDetailed Pipeline Results:")
            for pipeline_name, pipeline_info in result['pipeline_stages'].items():
                if pipeline_info.get('executed'):
                    print(f"  ✓ {pipeline_name.upper()}: Executed")
        else:
            print(f"Status: ✗ {result['status']}")
            for error in result['errors']:
                print(f"  Error: {error}")
    
    def _generate_report(self):
        """Generate comprehensive test report"""
        print("\n\n" + "="*80)
        print("TEST EXECUTION REPORT")
        print("="*80)
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Test Cases: {len(self.results)}")
        print(f"Successful Tests: {sum(1 for r in self.results if r['status'] == 'SUCCESS')}")
        print(f"Failed Tests: {sum(1 for r in self.results if r['status'] != 'SUCCESS')}")
        
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            print(f"Total Execution Time: {duration:.2f} seconds")
        
        print("\n" + "-"*80)
        print("DETAILED RESULTS:")
        print("-"*80)
        
        for i, result in enumerate(self.results, 1):
            print(f"\n{i}. {result['case_name'].upper()}")
            print(f"   Description: {result['description']}")
            print(f"   Status: {result['status']}")
            
            if result['status'] == 'SUCCESS':
                summary = result['validation_summary']
                print(f"   Score: {result['final_score']:.2%}")
                print(f"   Level: {result['credibility_level']}")
                print(f"   Pipelines: {summary['executed_pipelines']}/{summary['total_pipelines']} executed")
                
                # Pipeline breakdown
                for pipeline_name, info in result['pipeline_stages'].items():
                    if info.get('executed'):
                        print(f"     ✓ {pipeline_name}")
            else:
                print(f"   Errors: {'; '.join(result['errors'])}")
        
        # Save detailed report to JSON
        report_file = os.path.join(os.path.dirname(__file__), 'test_results.json')
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n\nDetailed JSON report saved to: {report_file}")
        
        print("\n" + "="*80)
        print("TEST EXECUTION COMPLETE")
        print("="*80 + "\n")

def main():
    """Main entry point"""
    validator = PipelineValidator()
    validator.run_all_tests()

if __name__ == '__main__':
    main()
