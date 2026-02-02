"""
Test Runner Script
Runs all tests and saves results to test_results.txt
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


def run_tests():
    tests_dir = Path(__file__).parent
    
    exit_code = pytest.main([
        str(tests_dir),
        "-v",
        "--tb=short"
    ])
    
    return exit_code


if __name__ == "__main__":
    sys.exit(run_tests())
