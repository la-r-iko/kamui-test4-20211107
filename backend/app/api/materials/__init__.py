from fastapi import APIRouter
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Core dependencies
from app.core.gdrive_connector import GDriveConnector
from app.core.access_control import require_auth, check_permissions

# Initialize router
router = APIRouter()

class MaterialConfig(BaseModel):
    """
    教材設定を管理するための設定クラス
    """
    id: str
    title: str
    description: Optional[str] = None
    file_id: str  # Google Drive file ID
    category: str
    access_level: str = "student"  # student, teacher, admin
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}
    
    class Config:
        schema_extra = {
            "example": {
                "id": "mat_123",
                "title": "Basic Grammar Guide",
                "description": "Complete guide for basic English grammar",
                "file_id": "1ABC...xyz",
                "category": "grammar",
                "access_level": "student",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
                "metadata": {
                    "language_level": "beginner",
                    "file_type": "pdf",
                    "size_bytes": 1024000
                }
            }
        }

# Initialize Google Drive connector for materials
gdrive = GDriveConnector()

# Import routes
from .routes import *

# Export necessary components
__all__ = [
    'router',
    'MaterialConfig',
    'gdrive'
]