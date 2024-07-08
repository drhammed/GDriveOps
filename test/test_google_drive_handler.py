# tests/test_google_drive_handler.py

import unittest
from my_google_drive_package.google_drive_handler import GoogleDriveHandler

class TestGoogleDriveHandler(unittest.TestCase):

    def setUp(self):
        self.handler = GoogleDriveHandler()

    def test_create_service(self):
        self.assertIsNotNone(self.handler.service)

    # Add more tests for other methods

if __name__ == '__main__':
    unittest.main()
    
