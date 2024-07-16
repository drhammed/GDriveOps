import pytest
import os
from unittest.mock import MagicMock, patch, mock_open
from GDriveOps.GDhandler import GoogleDriveHandler

@pytest.fixture
def handler():
    return GoogleDriveHandler()

def find_file_with_extension(directory, extension):
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            return os.path.join(directory, filename)
    return None

def test_ensure_directory(mocker, handler):
    mock_makedirs = mocker.patch('GDriveOps.GDhandler.os.makedirs')
    mocker.patch('GDriveOps.GDhandler.os.path.exists', return_value=False)
    handler.ensure_directory('new_dir')
    mock_makedirs.assert_called_with('new_dir')

def test_convert_pdf_to_text(mocker, handler):
    pdf_file = find_file_with_extension('tests/files', '.pdf')
    assert pdf_file is not None, "No .pdf file found in tests/files"
    text = handler.convert_pdf_to_text(pdf_file)
    assert "Diabetes is a disease" in text  # Match the actual content

def test_process_pdfs_in_dir(mocker, handler):
    pdf_file = find_file_with_extension('tests/files', '.pdf')
    pdf_name = os.path.basename(pdf_file)
    txt_file = os.path.splitext(pdf_name)[0] + '.txt'

    mocker.patch('GDriveOps.GDhandler.os.listdir', return_value=[pdf_name])
    mocker.patch.object(handler, 'convert_pdf_to_text', return_value='Sample text from PDF')

    with patch('builtins.open', mock_open()) as mock_file:
        handler.process_pdfs_in_dir('tests/files')
        handler.convert_pdf_to_text.assert_called_with(pdf_file)
        mock_file.assert_called_with(os.path.join('tests/files', txt_file), 'w', encoding='utf-8')

def test_docx_to_text(handler):
    docx_file = find_file_with_extension('tests/files', '.docx')
    assert docx_file is not None, "No .docx file found in tests/files"
    text = handler.docx_to_text(docx_file)
    assert "Diabetes is a disease" in text  # Match the actual content

def test_convert_docx_to_txt(mocker, handler):
    docx_file = find_file_with_extension('tests/files', '.docx')
    docx_name = os.path.basename(docx_file)
    txt_file = os.path.splitext(docx_name)[0] + '.txt'

    mocker.patch('GDriveOps.GDhandler.os.listdir', return_value=[docx_name])
    mocker.patch.object(handler, 'docx_to_text', return_value='Sample text from DOCX')

    with patch('builtins.open', mock_open()) as mock_file:
        handler.convert_docx_to_txt('tests/files')
        handler.docx_to_text.assert_called_with(docx_file)
        mock_file.assert_called_with(os.path.join('tests/files', txt_file), 'w', encoding='utf-8')

if __name__ == '__main__':
    pytest.main()
