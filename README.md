# GDriveOps

`GDriveOps` is a Python package for handling Google Drive file uploads and downloads, with additional functionality for converting files to text.  This package provides tools for downloading and uploading PDF and text files from/to Google Drive.


## Installation

`pip install GDriveOps`


## Usage

```python
from GDriveOps.GDhandler import GoogleDriveHandler

# Initialize the Handler

Create an instance of GoogleDriveHandler by providing the paths to your token.json & credentials.json files.

handler = GoogleDriveHandler(credentials_path='path_to_credentials.json')


# Download all PDF files from a specified Google Drive folder to a local directory.

handler.download_all_pdfs('folder_id', save_dir='save_dir') #If you don't specify the save directory, it will automatically generate one in your present working directory and name it "PDF_docs". Folder ID is the specific Google Drive folder ID.


# Upload all .txt files from a local directory to a specified Google Drive folder.
handler.upload_txt(folder_id, directory_path='PDF_docs') #your directory


# Convert all PDF files in a local directory to text files.
handler.process_pdfs_in_dir(directory_path='local_dir')


# Convert all DOCX files in a local directory to text files.

handler.convert_docx_to_txt('local_dir')

#Download docs from drive to your computer

handler.download_docs(folder_id, save_dir="local_dir")

#handler.download_all_text_files(folder_id)
handler.download_txt(folder_id, save_dir='dir')

```


# Command Line Usage
First, ensure you have the package installed. You can install it directly from PyPI using pip (see the `Installation` above).


Once installed, you can use the following commands with `GDriveOps` to perform different actions:

```python
python -m GDriveOps <action> <folder_id> [--credentials <credentials_path>] [--directory <directory_path>]
```

## Actions

`download_pdfs`: Download all PDFs from a specified Google Drive folder.

`upload_txt`: Upload all .txt files from a specified directory to a Google Drive folder.

`convert_pdfs`: Convert all PDFs in a specified directory to text files.

`convert_docx`: Convert all DOCX files in a specified directory to text files.

`download_txts`: Download all text files from a specified Google Drive folder.

`download_docs`: Download all DOC and DOCX files from a specified Google Drive folder.

## Options

- `action`: The action to perform (e.g., download_pdfs, upload_txt, etc.).

- `folder_id`: The Google Drive folder ID where files will be uploaded or downloaded.

- `--credentials (credentials_path)`: Optional. Path to the credentials.json file. Default is credentials.json in your current working directory.

- `--directory (directory_path)`: Optional. Directory to process files in. Default is the current directory.


# Authentication
Before using the command line tools, ensure you have authenticated with Google Drive:

- First-time setup: Run the following code to authenticate and generate a token:

```python
from GDriveOps.GDhandler import GoogleDriveHandler
handler = GoogleDriveHandler(credentials_path='path/to/credentials.json')
```

This will open a browser window for authentication. Once completed, a token.json file will be created.

- Subsequent runs: You don't need to authenticate again unless the token expires or becomes invalid. You can just navigate to the same directory where youu have the credentials and perrom the tasks.


## Examples

```python

# Download all PDFs from a Google Drive folder:
python -m GDriveOps download_pdfs <folder_id> 

# Upload all .txt files from a local directory to a Google Drive folder:
python -m GDriveOps upload_txt <folder_id> --directory /path/to/local/directory


# Convert all PDFs in a local directory to text files:
python -m GDriveOps convert_pdfs --directory /path/to/local/directory


# Convert all DOCX files in a local directory to text files:
python -m GDriveOps convert_docx --directory /path/to/local/directory

# Download all text files from a Google Drive folder:
python -m GDriveOps download_txts <folder_id>


# Download all DOC and DOCX files from a Google Drive folder:
python -m GDriveOps download_docs <folder_id> 

```



# Setup Requirements
Ensure Python is installed on your system and obtain credentials.json from the Google API credentials. Also, you need to install the required Python packages.

## Detailed Setup Instructions

1. Obtain Google API Credentials:
- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project (or select an existing one).
- Navigate to the "Credentials" page (APIs & Services > Credentials) and create OAuth 2.0 Client IDs.
- Download the credentials.json file and place it in your working directory.


2. Install Dependencies:
   
   By default, GDriveOps should install the dependencies. If you're using Google Colab, I recommend installing the following versions for Google Authentication.
   ```python
   !pip install google-api-python-client==1.7.2 google-auth==2.14.1 google-auth-httplib2==0.0.3 google-auth-oauthlib==0.4.1 PyMuPDF python-docx
   ```

3. Running the Script:
   
**In a Terminal**:

Open a terminal and navigate to the directory containing your credentials.json. Use one of the provided commands to perform the desired action, replacing <folder_id> and <local_directory> with appropriate values.

**In a Jupyter Notebook or Python Script**:

You can run the package in a Jupyter notebook or any Python script as follows:

- Install the package via pip.
- Import the necessary classes and functions from the package.
- Use the same methods as described in the usage section.



# License
This project is licensed under the MIT License. See the LICENSE file for details.