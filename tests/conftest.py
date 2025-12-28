"""
Pytest Configuration & Fixtures
"""
import sys
import os
from pathlib import Path

# Add backend to path
BACKEND_ROOT = Path(__file__).resolve().parents[2] / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import pytest
from flask import Flask
from dotenv import load_dotenv

@pytest.fixture(scope="session")
def setup_env():
    """Load environment variables once per session"""
    load_dotenv(BACKEND_ROOT / "config" / "secrets.env")
    yield

@pytest.fixture
def app():
    """Create Flask app for testing"""
    os.chdir(str(BACKEND_ROOT))
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()
