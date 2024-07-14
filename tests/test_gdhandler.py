# tests/test_gdhandler.py

import unittest
from unittest.mock import patch, MagicMock, mock_open
from gdUpload.gdhandler import GoogleDriveHandler
import os
import io

class TestGoogleDriveHandler(unittest.TestCase):

    @patch('gdUpload.gdhandler.Credentials.from_authorized_user_file')
    @patch('gdUpload.gdhandler.build')
    @patch('gdUpload.gdhandler.InstalledAppFlow.from_client_secrets_file')
    def setUp(self, mock_flow, mock_build, mock_creds):
        print("Setting up mocks")
        # Mock the credentials and service
        self.mock_creds = MagicMock()
        mock_creds.return_value = self.mock_creds
        self.mock_service = MagicMock()
        mock_build.return_value = self.mock_service
        mock_flow.return_value.run_local_server.return_value = self.mock_creds

        # Initialize the handler with mocks
        self.handler = GoogleDriveHandler(token_path='test_token.json', credentials_path='test_credentials.json')
        print("Setup complete")

    @patch('gdUpload.gdhandler.build')
    @patch('gdUpload.gdhandler.Credentials.from_authorized_user_file')
    def test_create_service(self, mock_credentials, mock_build):
        print("Running test_create_service")
        mock_credentials.return_value = self.mock_creds
        mock_build.return_value = self.mock_service
        service = self.handler.create_service()
        self.assertIsNotNone(service)
        mock_credentials.assert_called_once_with('test_token.json', self.handler.SCOPES)
        mock_build.assert_called_once_with('drive', 'v3', credentials=mock_credentials.return_value)
        print("test_create_service complete")

    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    @patch('gdUpload.gdhandler.MediaIoBaseDownload')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_download_all_pdfs(self, mock_path_exists, mock_open, mock_makedirs, mock_media_download, mock_create_service):
        print("Running test_download_all_pdfs")
        mock_service = MagicMock()
        mock_create_service.return_value = mock_service
        mock_service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': 'file_id', 'name': 'test.pdf'}]
        }

        mock_request = MagicMock()
        mock_service.files.return_value.get_media.return_value = mock_request

        mock_media_download_instance = MagicMock()
        mock_media_download.return_value = mock_media_download_instance
        mock_media_download_instance.next_chunk.side_effect = [(MagicMock(progress=0.5), False), (MagicMock(progress=1.0), True)]

        self.handler.download_all_pdfs('test_folder_id')

        mock_service.files.return_value.list.assert_called_once_with(
            q="'test_folder_id' in parents and mimeType='application/pdf'",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            pageToken=None
        )

        mock_service.files.return_value.get_media.assert_called_once_with(fileId='file_id')
        mock_media_download.assert_called_once_with(mock_request, mock.ANY)
        self.assertTrue(mock_media_download_instance.next_chunk.called)
        mock_makedirs.assert_called_once_with('PDF_docs')
        mock_open.assert_called_once_with('PDF_docs/test.pdf', 'wb')
        print("test_download_all_pdfs complete")

    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_upload_all_txt_files(self, mock_create_service):
        print("Running test_upload_all_txt_files")
        mock_service = MagicMock()
        mock_create_service.return_value = mock_service
        with patch('os.listdir', return_value=['test.txt']):
            with patch('os.path.isfile', return_value=True):
                self.handler.upload_all_txt_files('test_folder_id')
                mock_service.files.return_value.create.assert_called_once()
        print("test_upload_all_txt_files complete")

if __name__ == '__main__':
    unittest.main()
