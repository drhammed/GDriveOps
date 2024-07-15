# tests/test_gdhandler.py

import unittest
from unittest.mock import patch, MagicMock
from gdUpload.gdhandler import GoogleDriveHandler

class TestGoogleDriveHandler(unittest.TestCase):

    @patch('gdUpload.gdhandler.build')
    @patch('gdUpload.gdhandler.Credentials')
    @patch('gdUpload.gdhandler.InstalledAppFlow')
    @patch('gdUpload.gdhandler.os.path.exists')
    def setUp(self, mock_exists, mock_flow, mock_credentials, mock_build):
        mock_exists.side_effect = lambda path: True  # Mock os.path.exists to always return True
        mock_credentials.from_authorized_user_file.return_value = MagicMock(valid=True)
        mock_flow.from_client_secrets_file.return_value.run_local_server.return_value = MagicMock()

        self.handler = GoogleDriveHandler()

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.io.BytesIO')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_download_pdfs(self, mock_create_service, mock_bytesio, mock_makedirs):
        mock_service = MagicMock()
        mock_service.files().list().execute.return_value = {
            'files': [{'id': 'file_id_1', 'name': 'file1.pdf'}],
            'nextPageToken': None
        }
        mock_service.files().get_media.return_value = MagicMock()
        mock_create_service.return_value = mock_service

        self.handler.download_pdfs('fake_folder_id')
        mock_service.files().list.assert_called()
        mock_service.files().get_media.assert_called_with(fileId='file_id_1')

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.os.path.exists')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_upload_txt(self, mock_create_service, mock_exists, mock_makedirs):
        mock_exists.side_effect = lambda path: True  # Mock os.path.exists to always return True
        mock_service = MagicMock()
        mock_service.files().list().execute.return_value = {'files': []}
        mock_create_service.return_value = mock_service

        with patch('gdUpload.gdhandler.os.listdir', return_value=['file1.txt']):
            with patch('gdUpload.gdhandler.MediaFileUpload', return_value=MagicMock()):
                self.handler.upload_txt('fake_folder_id', 'fake_directory')
                mock_service.files().create.assert_called()

    @patch('gdUpload.gdhandler.fitz.open')
    def test_convert_pdf_to_text(self, mock_fitz_open):
        mock_doc = MagicMock()
        mock_fitz_open.return_value.__enter__.return_value = mock_doc
        mock_doc.__iter__.return_value = [MagicMock(get_text=lambda: "Page 1 text"), MagicMock(get_text=lambda: "Page 2 text")]

        text = self.handler.convert_pdf_to_text('fake_pdf_path')
        self.assertEqual(text, "Page 1 textPage 2 text")

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.os.path.exists')
    @patch('gdUpload.gdhandler.os.listdir')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.convert_pdf_to_text')
    def test_process_pdfs_in_dir(self, mock_convert_pdf_to_text, mock_listdir, mock_exists, mock_makedirs):
        mock_exists.side_effect = lambda path: True
        mock_listdir.return_value = ['file1.pdf']
        mock_convert_pdf_to_text.return_value = 'Sample text from PDF'

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.handler.process_pdfs_in_dir('fake_directory')
            mock_convert_pdf_to_text.assert_called_with('fake_directory/file1.pdf')
            mock_file.assert_called_with('fake_directory/file1.txt', 'w', encoding='utf-8')

    @patch('gdUpload.gdhandler.Document')
    def test_docx_to_text(self, mock_document):
        mock_doc = MagicMock()
        mock_document.return_value = mock_doc
        mock_doc.paragraphs = [MagicMock(text='Paragraph 1'), MagicMock(text='Paragraph 2')]

        text = self.handler.docx_to_text('fake_docx_path')
        self.assertEqual(text, 'Paragraph 1\nParagraph 2')

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.os.path.exists')
    @patch('gdUpload.gdhandler.os.listdir')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.docx_to_text')
    def test_convert_docx_to_txt(self, mock_docx_to_text, mock_listdir, mock_exists, mock_makedirs):
        mock_exists.side_effect = lambda path: True
        mock_listdir.return_value = ['file1.docx']
        mock_docx_to_text.return_value = 'Sample text from DOCX'

        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.handler.convert_docx_to_txt('fake_directory')
            mock_docx_to_text.assert_called_with('fake_directory/file1.docx')
            mock_file.assert_called_with('fake_directory/file1.txt', 'w', encoding='utf-8')

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.io.BytesIO')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_download_txt(self, mock_create_service, mock_bytesio, mock_makedirs):
        mock_service = MagicMock()
        mock_service.files().list().execute.return_value = {
            'files': [{'id': 'file_id_1', 'name': 'file1.txt'}],
            'nextPageToken': None
        }
        mock_service.files().get_media.return_value = MagicMock()
        mock_create_service.return_value = mock_service

        self.handler.download_txt('fake_folder_id')
        mock_service.files().list.assert_called()
        mock_service.files().get_media.assert_called_with(fileId='file_id_1')

    @patch('gdUpload.gdhandler.os.makedirs')
    @patch('gdUpload.gdhandler.io.BytesIO')
    @patch('gdUpload.gdhandler.GoogleDriveHandler.create_service')
    def test_download_docs(self, mock_create_service, mock_bytesio, mock_makedirs):
        mock_service = MagicMock()
        mock_service.files().list().execute.return_value = {
            'files': [{'id': 'file_id_1', 'name': 'file1.docx'}],
            'nextPageToken': None
        }
        mock_service.files().get_media.return_value = MagicMock()
        mock_create_service.return_value = mock_service

        self.handler.download_docs('fake_folder_id')
        mock_service.files().list.assert_called()
        mock_service.files().get_media.assert_called_with(fileId='file_id_1')

if __name__ == '__main__':
    unittest.main()
