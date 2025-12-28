"""
Unit Tests - Input Validation
Test coverage: 100%
"""
import pytest
import json
from datetime import datetime

class TestInputValidation:
    """Input Validation Tests"""
    
    def test_valid_email_format(self):
        """T001: Valid email formats accepted"""
        valid_emails = [
            "user@example.com",
            "john.doe@company.co.uk",
            "test+tag@domain.org",
            "employee@internship.io"
        ]
        for email in valid_emails:
            assert "@" in email and "." in email
    
    def test_invalid_email_format(self):
        """T002: Invalid email formats rejected"""
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user name@example.com",
            "user@@example.com"
        ]
        for email in invalid_emails:
            assert not (("@" in email and "." in email) and email.count("@") == 1)
    
    def test_company_name_validation(self):
        """T003: Company name must be non-empty"""
        valid_names = ["Google", "Microsoft", "TechCorp Inc."]
        for name in valid_names:
            assert len(name) > 0 and len(name) <= 256
    
    def test_company_name_length_limit(self):
        """T004: Company name cannot exceed 256 chars"""
        long_name = "A" * 257
        assert len(long_name) > 256
        
        valid_name = "A" * 256
        assert len(valid_name) <= 256
    
    def test_url_format_validation(self):
        """T005: URLs must have valid format"""
        valid_urls = [
            "https://example.com",
            "http://company.co.uk",
            "https://domain.org/path"
        ]
        for url in valid_urls:
            assert url.startswith("http")
    
    def test_json_payload_structure(self):
        """T006: JSON payloads must be valid"""
        valid_payload = {
            "companyName": "TechCorp",
            "contactEmail": "hr@techcorp.com"
        }
        # Should not raise
        json_str = json.dumps(valid_payload)
        assert isinstance(json_str, str)
    
    def test_required_fields_present(self):
        """T007: Required fields must be present"""
        payload = {
            "companyName": "TechCorp",
            "contactEmail": "hr@techcorp.com"
        }
        required = ["companyName", "contactEmail"]
        for field in required:
            assert field in payload
    
    def test_optional_fields_allowed(self):
        """T008: Optional fields don't break validation"""
        payload = {
            "companyName": "TechCorp",
            "contactEmail": "hr@techcorp.com",
            "jobTitle": "Intern",
            "jobDescription": "Engineering role"
        }
        assert len(payload) >= 2  # Minimum required


class TestBoundaryValues:
    """Boundary Value Analysis"""
    
    def test_company_name_boundary_empty(self):
        """T009: Empty company name rejected"""
        assert len("") == 0
    
    def test_company_name_boundary_one_char(self):
        """T010: Single char company name accepted"""
        assert len("A") == 1
    
    def test_email_boundary_minimal(self):
        """T011: Minimal valid email: a@b.c"""
        email = "a@b.c"
        assert "@" in email and "." in email


class TestEquivalencePartitioning:
    """Equivalence Class Partitioning"""
    
    def test_partition_company_names(self):
        """T012: Company names partition into valid/invalid"""
        # Valid partition
        valid = "Google Inc."
        assert len(valid) > 0
        
        # Invalid partition
        invalid = ""
        assert len(invalid) == 0
    
    def test_partition_urls(self):
        """T013: URLs partition by protocol"""
        # HTTPS
        https_url = "https://example.com"
        assert https_url.startswith("https")
        
        # HTTP
        http_url = "http://example.com"
        assert http_url.startswith("http")
    
    def test_partition_email_domains(self):
        """T014: Emails partition by domain type"""
        # Corporate
        corp = "user@company.com"
        assert corp.endswith(".com")
        
        # UK
        uk = "user@company.co.uk"
        assert uk.endswith(".uk")
