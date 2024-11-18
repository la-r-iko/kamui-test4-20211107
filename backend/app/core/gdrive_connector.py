from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from typing import Optional, List, Dict
import os
import io
import logging
from datetime import datetime

class GoogleDriveConnector:
    """Google Driveとの連携を管理するクラス"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self):
        """初期化処理"""
        self.credentials = None
        self.service = None
        self.logger = logging.getLogger(__name__)
        
    def authenticate(self) -> bool:
        """
        Google Drive APIの認証を行う
        
        Returns:
            bool: 認証成功の場合True、失敗の場合False
        """
        try:
            client_config = {
                "installed": {
                    "client_id": os.getenv("GOOGLE_DRIVE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_DRIVE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"]
                }
            }
            
            flow = InstalledAppFlow.from_client_config(
                client_config,
                self.SCOPES
            )
            self.credentials = flow.run_local_server(port=0)
            self.service = build('drive', 'v3', credentials=self.credentials)
            return True
            
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            return False

    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> Optional[str]:
        """
        ファイルをGoogle Driveにアップロードする
        
        Args:
            file_path (str): アップロードするファイルのパス
            folder_id (Optional[str]): アップロード先のフォルダID
            
        Returns:
            Optional[str]: アップロードしたファイルのID、失敗時はNone
        """
        try:
            file_metadata = {
                'name': os.path.basename(file_path)
            }
            if folder_id:
                file_metadata['parents'] = [folder_id]
                
            media = MediaFileUpload(
                file_path,
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return file.get('id')
            
        except Exception as e:
            self.logger.error(f"Upload failed: {str(e)}")
            return None

    def download_file(self, file_id: str, output_path: str) -> bool:
        """
        Google Driveからファイルをダウンロードする
        
        Args:
            file_id (str): ダウンロードするファイルのID
            output_path (str): 保存先のパス
            
        Returns:
            bool: ダウンロード成功の場合True、失敗の場合False
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            fh.seek(0)
            with open(output_path, 'wb') as f:
                f.write(fh.read())
                f.close()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Download failed: {str(e)}")
            return False

    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Google Drive上にフォルダを作成する
        
        Args:
            folder_name (str): フォルダ名
            parent_id (Optional[str]): 親フォルダのID
            
        Returns:
            Optional[str]: 作成したフォルダのID、失敗時はNone
        """
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
                
            file = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return file.get('id')
            
        except Exception as e:
            self.logger.error(f"Folder creation failed: {str(e)}")
            return None

    def list_files(self, folder_id: Optional[str] = None) -> List[Dict]:
        """
        指定フォルダ内のファイル一覧を取得する
        
        Args:
            folder_id (Optional[str]): フォルダID
            
        Returns:
            List[Dict]: ファイル情報のリスト
        """
        try:
            query = f"'{folder_id}' in parents" if folder_id else None
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, mimeType, createdTime, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            self.logger.error(f"List files failed: {str(e)}")
            return []

# インスタンス化
gdrive = GoogleDriveConnector()

# 認証
if gdrive.authenticate():
    # ファイルのアップロード
    file_id = gdrive.upload_file("/path/to/file.pdf")
    
    # フォルダの作成
    folder_id = gdrive.create_folder("新しいフォルダ")
    
    # ファイル一覧の取得
    files = gdrive.list_files(folder_id)
    
    # ファイルのダウンロード
    gdrive.download_file(file_id, "/path/to/save/file.pdf")