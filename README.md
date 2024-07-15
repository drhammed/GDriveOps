# gdUpload

`gdUpload` is a Python package for handling Google Drive file uploads and downloads, with additional functionality for converting files to text.  This package provides tools for downloading and uploading PDF and text files from/to Google Drive.


## Installation


`pip install gdUpload`




## Usage

```python
from gdUpload.gdhandler import GoogleDriveHandler

# Initialize the Handler

Create an instance of GoogleDriveHandler by providing the paths to your token.json & credentials.json files.

handler = GoogleDriveHandler(token_path='path_to_token.json', credentials_path='path_to_credentials.json')

# Download all PDFs from a Google Drive folder
#Download all PDF files from a specified Google Drive folder to a local directory.

handler.download_all_pdfs('folder_id', save_dir='save_directory')

# Upload all text files from a local directory to a Google Drive folder
#Upload all .txt files from a local directory to a specified Google Drive folder.
handler.upload_all_txt_files('folder_id', directory_path='local_directory')

# Convert all PDFs in a local directory to text files
# Convert all PDF files in a local directory to text files.
handler.process_pdfs_in_directory('local_directory')

# Convert all DOCX files in a local directory to text files
# Convert all DOCX files in a local directory to text files.
handler.convert_all_docx_to_txt('local_directory')
```


## Command Line Usage
The package can also be used via command line. Use the following commands to perform different actions.

```python
# Download All PDFs
python gdhandler.py download_pdfs <folder_id>

# Upload All Text Files
python gdhandler.py upload_txt <folder_id> --directory <local_directory>

# Convert All PDFs to Text Files
python gdhandler.py convert_pdfs --directory <local_directory>

# Convert All DOCX Files to Text Files
python gdhandler.py convert_docx --directory <local_directory>
```


## Setup Requirements
Ensure Python is installed on your system and obtain credentials.json from the Google API credentials. Also, you need to install the required Python packages.

# Detailed Setup Instructions

1. Obtain Google API Credentials:
- Go to the Google Cloud Console.
- Create a new project (or select an existing one).
- Navigate to the "Credentials" page and create OAuth 2.0 Client IDs.
- Download the credentials.json file and place it in the directory where gdhandler.py is located.


2. Install Dependencies
   ```python
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-docx PyMuPDF
   ```

3. Running the Script
- In a Terminal
Open a terminal and navigate to the directory containing gdhandler.py.
Use one of the provided commands to perform the desired action, replacing <folder_id> and <local_directory> with appropriate values.
- In a Jupyter Notebook or Python Script
You can run the package in a Jupyter notebook or any Python script as follows:

Install the package via pip.
Import the necessary classes and functions from the package.
Use the same methods as described in the usage section.



# License
This project is licensed under the MIT License. See the LICENSE file for details.