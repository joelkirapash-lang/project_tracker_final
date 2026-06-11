"""
conftest.py
Pytest configuration: adds the project root to sys.path so imports work correctly.
"""
import sys
from pathlib import Path

# Ensure the project root is on the path for all test files
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
