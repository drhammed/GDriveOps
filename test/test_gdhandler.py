# tests/test_gdhandler.py

import unittest
import os
from unittest.mock import patch, MagicMock
from gdUpload.gdhandler import GoogleDriveHandler

class TestGoogleDriveHandler(unittest.TestCase):

    def setUp(self):
        # Use mock credentials for testing
        self.handler = GoogleDriveHandler(token_path='test_token.json', credentials_path='test_credentials.json')

    @patch('gdUpload.gdhandler.build')
    @patch('gdUpload.gdhandler.Credentials.from_authorized_user_file')
    def test_create_service(self, mock_credentials, mock_build):
        mock_credentials.return_value = MagicMock()
        mock_build.return_value = MagicMock()
        service = self.handler.create_service()
        self.assertIsNotNone(service)
        mock_credentials.assert_called_once_with('test_token.json', self.handler.SCOPES)
        mock_build.assert_called_once_with('drive', 'v3', credentials=mock_credentials.return_value)

    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_download_all_pdfs(self, mock_create_service):
        mock_service = MagicMock()
        mock_create_service.return_value = mock_service
        mock_service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': 'file_id', 'name': 'test.pdf'}]
        }
        self.handler.download_all_pdfs('test_folder_id')
        mock_service.files.return_value.get_media.assert_called_once_with(fileId='file_id')

    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_upload_all_txt_files(self, mock_create_service):
        mock_service = MagicMock()
        mock_create_service.return_value = mock_service
        with patch('os.listdir', return_value=['test.txt']):
            with patch('os.path.isfile', return_value=True):
                self.handler.upload_all_txt_files('test_folder_id')
                mock_service.files.return_value.create.assert_called_once()

    # Add more tests for other methods

if __name__ == '__main__':
    unittest.main()
