# gdUpload
 This package provides tools for downloading and uploading PDF and text files from/to Google Drive.

 # My Google Drive Package

This package provides tools for downloading and uploading PDF and text files from/to Google Drive.

## Installation

pip install my_google_drive_package



#Usage

from my_google_drive_package.google_drive_handler import GoogleDriveHandler

handler = GoogleDriveHandler()
handler.download_all_pdfs('your_folder_id')
handler.upload_all_txt_files('your_folder_id')
