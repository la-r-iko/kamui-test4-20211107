from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

class MaterialBase(BaseModel):
    """教材の基本スキーマ"""
    title: str = Field(..., description="教材のタイトル", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="教材の説明")
    category: str = Field(..., description="教材のカテゴリ (例: 文法, リスニング等)")
    level: str = Field(..., description="教材のレベル (例: 初級, 中級, 上級)")
    file_type: str = Field(..., description="ファイルタイプ (例: PDF, VIDEO, AUDIO)")

class MaterialCreate(MaterialBase):
    """教材作成用スキーマ"""
    file_url: HttpUrl = Field(..., description="教材ファイルのURL")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="サムネイル画像のURL")
    tags: Optional[List[str]] = Field(default=[], description="教材に関連するタグ")

class MaterialUpdate(BaseModel):
    """教材更新用スキーマ"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    file_url: Optional[HttpUrl] = None
    thumbnail_url: Optional[HttpUrl] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Material(MaterialBase):
    """教材の完全なスキーマ"""
    id: int = Field(..., description="教材のID")
    file_url: HttpUrl = Field(..., description="教材ファイルのURL")
    thumbnail_url: Optional[HttpUrl] = Field(None, description="サムネイル画像のURL")
    tags: List[str] = Field(default=[], description="教材に関連するタグ")
    download_count: int = Field(default=0, description="ダウンロード数")
    is_active: bool = Field(default=True, description="教材が有効かどうか")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")

    class Config:
        orm_mode = True

class MaterialDownload(BaseModel):
    """教材ダウンロード記録用スキーマ"""
    material_id: int = Field(..., description="教材のID")
    user_id: int = Field(..., description="ダウンロードしたユーザーのID")
    downloaded_at: datetime = Field(default_factory=datetime.utcnow, description="ダウンロード日時")

    class Config:
        orm_mode = True