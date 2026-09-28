import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.query_parser import parse_query_constraints

class TestQueryParser(unittest.TestCase):
    def test_extract_login(self):
        """Test extraction of 'login' category."""
        constraints = parse_query_constraints("How do I fix the login timeout?")
        self.assertEqual(constraints.get("category"), "login")
        
    def test_extract_hardware_case_insensitive(self):
        """Test extraction regardless of capitalization."""
        constraints = parse_query_constraints("My HARDWARE is broken.")
        self.assertEqual(constraints.get("category"), "hardware")
        
    def test_no_matching_category(self):
        """Test fallback when no strict category is mentioned."""
        constraints = parse_query_constraints("How do I reset my password?")
        self.assertIsNone(constraints.get("category"))

if __name__ == "__main__":
    unittest.main()