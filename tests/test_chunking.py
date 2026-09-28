import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from embeddings.chunk import create_whole_ticket_chunk

class TestChunking(unittest.TestCase):
    def test_full_ticket(self):
        """Test standard ticket with both description and resolution."""
        chunk = create_whole_ticket_chunk("App crashes on startup.", "Cleared app cache.")
        self.assertEqual(chunk, "Description: App crashes on startup. Resolution: Cleared app cache.")
        
    def test_missing_resolution(self):
        """Test open tickets that don't have a resolution yet."""
        chunk = create_whole_ticket_chunk("User cannot log in.", "")
        self.assertEqual(chunk, "Description: User cannot log in.")
        
    def test_missing_description(self):
        """Test malformed tickets with no description."""
        chunk = create_whole_ticket_chunk("", "Restarted the server.")
        self.assertEqual(chunk, "")

if __name__ == "__main__":
    unittest.main()