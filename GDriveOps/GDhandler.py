#import libs
import os
import io
import fitz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from docx import Document

class GoogleDriveHandler:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self.create_service()

    def create_service(self):
        creds = None

        if not os.path.exists(self.credentials_path):
            raise FileNotFoundError(f"{self.credentials_path} not found. Please ensure it is in your current working directory.")

        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
            except Exception as e:
                print(f"Error loading {self.token_path}: {e}")
                creds = None

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Failed to refresh token: {e}. Re-authenticating...")
                    creds = None

            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                    if 'COLAB_GPU' in os.environ:
                        creds = flow.run_console()
                    else:
                        creds = flow.run_local_server(port=0)
                except Exception as e:
                    raise RuntimeError(f"Failed to obtain credentials: {e}")

            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            raise RuntimeError(f"Failed to create the Google Drive service: {e}")

        return service

    def ensure_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def get_files_in_folder(self, folder_id, mimeType, page_size=10):
        query = f"'{folder_id}' in parents and mimeType='{mimeType}' and trashed=false"
        files = []
        page_token = None
        while True:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
                pageSize=page_size
            ).execute()
            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def get_files_in_folder_with_query(self, query, page_size=10):
        query += " and trashed=false"
        files = []
        page_token = None
        while True:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
                pageSize=page_size
            ).execute()
            files.extend(results.get('files', []))
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
        return files

    def download_file(self, item, save_dir):
        file_name = item['name']
        if not os.path.exists(os.path.join(save_dir, file_name)):
            print(f"Downloading {file_name}...")
            request = self.service.files().get_media(fileId=item['id'])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            with open(os.path.join(save_dir, file_name), 'wb') as f:
                fh.seek(0)
                f.write(fh.read())
        else:
            print(f"{file_name} already exists. Skipping download.")

    def get_existing_files(self, folder_id):
        existing_files = self.service.files().list(q=f"'{folder_id}' in parents and trashed=false",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)').execute()
        return [file['name'] for file in existing_files.get('files', [])]

    def upload_file(self, file_name, folder_id, directory_path):
        file_path = os.path.join(directory_path, file_name)
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='text/plain')
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        print(f"{file_name} uploaded successfully with File ID: {file.get('id')}")

    def download_pdfs(self, folder_id, save_dir='PDF_docs'):
        self.ensure_directory(save_dir)
        page_token = None
        while True:
            items = self.get_files_in_folder(folder_id, "application/pdf", page_size=10)
            if not items:
                print('No more files found.')
                break
            for item in items:
                self.download_file(item, save_dir)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    def upload_txt(self, folder_id, directory_path='.'):
        self.ensure_directory(directory_path)
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith('.txt')]
        existing_files = self.get_existing_files(folder_id)

        for file_name in files:
            if file_name not in existing_files:
                self.upload_file(file_name, folder_id, directory_path)

    def convert_pdf_to_text(self, pdf_path):
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def process_pdfs_in_dir(self, directory_path):
        self.ensure_directory(directory_path)
        for filename in os.listdir(directory_path):
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(directory_path, filename)
                pdf_text = self.convert_pdf_to_text(full_path)
                output_filename = filename.rsplit('.', 1)[0] + '.txt'
                output_path = os.path.join(directory_path, output_filename)
                with open(output_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(pdf_text)
                print(f"Processed and saved: {filename} as {output_filename}")

    def docx_to_text(self, docx_file_path):
        doc = Document(docx_file_path)
        text = [paragraph.text for paragraph in doc.paragraphs]
        return '\n'.join(text)

    def convert_docx_to_txt(self, folder_path):
        self.ensure_directory(folder_path)
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.docx'):
                docx_file_path = os.path.join(folder_path, file_name)
                text_file_name = file_name.replace('.docx', '.txt')
                text_file_path = os.path.join(folder_path, text_file_name)
                text_content = self.docx_to_text(docx_file_path)
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_content)
                print(f"Converted {file_name} to {text_file_name}")

    def download_txt(self, folder_id, save_dir='Text_docs'):
        self.ensure_directory(save_dir)
        page_token = None
        while True:
            items = self.get_files_in_folder(folder_id, "text/plain", page_size=10)
            if not items:
                print('No more files found.')
                break
            for item in items:
                self.download_file(item, save_dir)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    def download_docs(self, folder_id, save_dir='Doc_docs'):
        self.ensure_directory(save_dir)
        query = f"'{folder_id}' in parents and (mimeType='application/msword' or mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document') and trashed=false"
        page_token = None
        while True:
            items = self.get_files_in_folder_with_query(query, page_size=10)
            if not items:
                print('No more files found.')
                break
            for item in items:
                self.download_file(item, save_dir)
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

# Entry point for command line usage
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Google Drive Handler')
    parser.add_argument('action', choices=['download_pdfs', 'upload_txt', 'convert_pdfs', 'convert_docx', 'download_txts', 'download_docs'], help='Action to perform')
    parser.add_argument('folder_id', help='Google Drive folder ID')
    parser.add_argument('--credentials', default='credentials.json', help='Path to credentials.json')
    parser.add_argument('--directory', default='.', help='Directory to process files in')

    args = parser.parse_args()

    handler = GoogleDriveHandler(credentials_path=args.credentials)

    if args.action == 'download_pdfs':
        handler.download_pdfs(args.folder_id)
    elif args.action == 'upload_txt':
        handler.upload_txt(args.folder_id, directory_path=args.directory)
    elif args.action == 'convert_pdfs':
        handler.process_pdfs_in_dir(args.directory)
    elif args.action == 'convert_docx':
        handler.convert_docx_to_txt(args.directory)
    elif args.action == 'download_txts':
        handler.download_txt(args.folder_id, save_dir=args.directory)
    elif args.action == 'download_docs':
        handler.download_docs(args.folder_id, save_dir=args.directory)

if __name__ == '__main__':
    main()
