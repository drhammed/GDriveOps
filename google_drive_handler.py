# my_google_drive_package/google_drive_handler.py

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import os
import io
import fitz
from docx import Document

class GoogleDriveHandler:
    def __init__(self, token_path='token.json', credentials_path='credentials.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.token_path = token_path
        self.credentials_path = credentials_path
        self.service = self.create_service()

    def create_service(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        service = build('drive', 'v3', credentials=creds)
        return service

    def download_all_pdfs(self, folder_id, save_dir='PDF_docs'):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        page_token = None
        while True:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents and mimeType='application/pdf'",
                pageSize=10,
                fields="nextPageToken, files(id, name)",
                pageToken=page_token
            ).execute()

            items = results.get('files', [])
            if not items:
                print('No files found.')
                break

            for item in items:
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
            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break

    def upload_all_txt_files(self, folder_id, directory_path='.'):
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith('.txt')]
        existing_files = self.service.files().list(q=f"'{folder_id}' in parents",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)').execute()
        existing_file_names = [file['name'] for file in existing_files.get('files', [])]

        for file_name in files:
            if file_name not in existing_file_names:
                file_path = os.path.join(directory_path, file_name)
                file_metadata = {'name': file_name, 'parents': [folder_id]}
                media = MediaFileUpload(file_path, mimetype='text/plain')
                file = self.service.files().create(body=file_metadata,
                                                   media_body=media,
                                                   fields='id').execute()
                print(f"{file_name} uploaded successfully with File ID: {file.get('id')}")
            else:
                print(f"{file_name} already exists in the folder. Skipping upload.")

    def convert_pdf_to_text(self, pdf_path):
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def process_pdfs_in_directory(self, directory_path):
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

    def convert_all_docx_to_txt(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.docx'):
                docx_file_path = os.path.join(folder_path, file_name)
                text_file_name = file_name.replace('.docx', '.txt')
                text_file_path = os.path.join(folder_path, text_file_name)
                text_content = self.docx_to_text(docx_file_path)
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text_content)
                print(f"Converted {file_name} to {text_file_name}")
