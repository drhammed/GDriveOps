# gdUpload

`gdUpload` is a Python package for handling Google Drive file uploads and downloads, with additional functionality for converting files to text.  This package provides tools for downloading and uploading PDF and text files from/to Google Drive.


## Installation


`pip install gdUpload`




## Usage

```python
from gdUpload.gdhandler import GoogleDriveHandler

handler = GoogleDriveHandler(token_path='path_to_token.json', credentials_path='path_to_credentials.json')

# Download all PDFs from a Google Drive folder
handler.download_all_pdfs('folder_id', save_dir='save_directory')

# Upload all text files from a local directory to a Google Drive folder
handler.upload_all_txt_files('folder_id', directory_path='local_directory')

# Convert all PDFs in a local directory to text files
handler.process_pdfs_in_directory('local_directory')

# Convert all DOCX files in a local directory to text files
handler.convert_all_docx_to_txt('local_directory')

```