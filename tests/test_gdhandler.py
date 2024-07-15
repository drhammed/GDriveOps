# tests/test_gdhandler.py

import pytest
from unittest.mock import patch, MagicMock, mock_open
from gdUpload.gdhandler import GoogleDriveHandler
import os
import io
#import sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


print(f"Current working directory: {os.getcwd()}") 

class TestGoogleDriveHandler:

    @patch('gdUpload.gdhandler.Credentials.from_authorized_user_file')
    @patch('gdUpload.gdhandler.build')
    @patch('gdUpload.gdhandler.InstalledAppFlow.from_client_secrets_file')
    def setup_method(self, method, mock_flow, mock_build, mock_creds):
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
        assert service is not None
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
        mock_service.files.return_value.list.side_effect = [
            MagicMock(execute=MagicMock(return_value={'files': [{'id': 'file_id', 'name': 'test.pdf'}], 'nextPageToken': 'token'})),
            MagicMock(execute=MagicMock(return_value={'files': [], 'nextPageToken': None}))
        ]

        mock_request = MagicMock()
        mock_service.files.return_value.get_media.return_value = mock_request

        mock_media_download_instance = MagicMock()
        mock_media_download.return_value = mock_media_download_instance
        mock_media_download_instance.next_chunk.side_effect = [(MagicMock(progress=0.5), False), (MagicMock(progress=1.0), True)]

        self.handler.download_all_pdfs('test_folder_id')

        mock_service.files.return_value.list.assert_any_call(
            q="'test_folder_id' in parents and mimeType='application/pdf'",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            pageToken=None
        )
        mock_service.files.return_value.list.assert_any_call(
            q="'test_folder_id' in parents and mimeType='application/pdf'",
            pageSize=10,
            fields="nextPageToken, files(id, name)",
            pageToken='token'
        )
        mock_service.files.return_value.get_media.assert_called_once_with(fileId='file_id')
        mock_media_download.assert_called_once_with(mock_request, mock.ANY)
        assert mock_media_download_instance.next_chunk.called
        mock_makedirs.assert_called_once_with('PDF_docs')
        mock_open.assert_called_once_with('PDF_docs/test.pdf', 'wb')
        print("test_download_all_pdfs complete")

    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    @patch('os.listdir', return_value=['test.txt'])
    @patch('os.path.isfile', return_value=True)
    def test_upload_all_txt_files(self, mock_isfile, mock_listdir, mock_create_service):
        print("Running test_upload_all_txt_files")
        mock_service = MagicMock()
        mock_create_service.return_value = mock_service

        existing_files = {'files': []}
        mock_service.files.return_value.list.return_value.execute.return_value = existing_files

        self.handler.upload_all_txt_files('test_folder_id')

        mock_service.files.return_value.create.assert_called_once()
        print("test_upload_all_txt_files complete")

    @patch('os.listdir')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    @patch('fitz.open')
    def test_process_pdfs_in_directory(self, mock_fitz_open, mock_open, mock_path_join, mock_listdir):
        print("Running test_process_pdfs_in_directory")
        mock_listdir.return_value = ['test.pdf']
        mock_path_join.side_effect = lambda *args: os.path.join(*args)
        
        mock_pdf_doc = MagicMock()
        mock_fitz_open.return_value = mock_pdf_doc
        mock_pdf_page = MagicMock()
        mock_pdf_doc.__enter__.return_value = mock_pdf_doc
        mock_pdf_doc.__iter__.return_value = iter([mock_pdf_page])
        mock_pdf_page.get_text.return_value = "This is a test."

        self.handler.process_pdfs_in_directory('test_directory')

        mock_fitz_open.assert_called_once_with('test_directory/test.pdf')
        mock_open.assert_called_once_with('test_directory/test.txt', 'w', encoding='utf-8')
        print("test_process_pdfs_in_directory complete")

    @patch('os.listdir')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open)
    @patch('gdUpload.gdhandler.Document')
    def test_convert_all_docx_to_txt(self, mock_document, mock_open, mock_path_join, mock_listdir):
        print("Running test_convert_all_docx_to_txt")
        mock_listdir.return_value = ['test.docx']
        mock_path_join.side_effect = lambda *args: os.path.join(*args)

        mock_doc = MagicMock()
        mock_document.return_value = mock_doc
        mock_doc.paragraphs = [MagicMock(text='This is a test.')]

        self.handler.convert_all_docx_to_txt('test_directory')

        mock_document.assert_called_once_with('test_directory/test.docx')
        mock_open.assert_called_once_with('test_directory/test.txt', 'w', encoding='utf-8')
        print("test_convert_all_docx_to_txt complete")

    @patch('fitz.open')
    def test_convert_pdf_to_text(self, mock_fitz_open):
        print("Running test_convert_pdf_to_text")
        mock_pdf_doc = MagicMock()
        mock_fitz_open.return_value = mock_pdf_doc
        mock_pdf_page = MagicMock()
        mock_pdf_doc.__enter__.return_value = mock_pdf_doc
        mock_pdf_doc.__iter__.return_value = iter([mock_pdf_page])
        mock_pdf_page.get_text.return_value = "This is a test."

        text = self.handler.convert_pdf_to_text('test.pdf')

        mock_fitz_open.assert_called_once_with('test.pdf')
        assert text == "This is a test."
        print("test_convert_pdf_to_text complete")

    @patch('gdUpload.gdhandler.Document')
    def test_docx_to_text(self, mock_document):
        print("Running test_docx_to_text")
        mock_doc = MagicMock()
        mock_document.return_value = mock_doc
        mock_doc.paragraphs = [MagicMock(text='This is a test.')]

        text = self.handler.docx_to_text('test.docx')

        mock_document.assert_called_once_with('test.docx')
        assert text == "This is a test."
        print("test_docx_to_text complete")

if __name__ == '__main__':
    pytest.main()
