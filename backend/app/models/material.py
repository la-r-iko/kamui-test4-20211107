from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Material(Base):
    """教材モデル
    
    教材情報を管理するためのSQLAlchemyモデル
    """
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(255))
    file_type = Column(String(50))  # pdf, doc, video等
    content_url = Column(String(255))  # Google Drive or S3 URL
    download_count = Column(Integer, default=0)
    is_public = Column(Boolean, default=True)
    
    # メタデータ
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 作成者情報
    created_by = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="materials")
    
    # カテゴリー情報
    category_id = Column(Integer, ForeignKey("material_categories.id"))
    category = relationship("MaterialCategory", back_populates="materials")
    
    # レッスンとの関連付け
    lesson_materials = relationship("LessonMaterial", back_populates="material")

    def __init__(self, title: str, description: str = None, file_path: str = None,
                 file_type: str = None, content_url: str = None, is_public: bool = True,
                 created_by: int = None, category_id: int = None):
        self.title = title
        self.description = description
        self.file_path = file_path
        self.file_type = file_type
        self.content_url = content_url
        self.is_public = is_public
        self.created_by = created_by
        self.category_id = category_id

    def to_dict(self):
        """モデルを辞書形式に変換"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'content_url': self.content_url,
            'download_count': self.download_count,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'category_id': self.category_id
        }

    def increment_download_count(self):
        """ダウンロード数をインクリメント"""
        self.download_count += 1

    def __repr__(self):
        return f"<Material(id={self.id}, title='{self.title}')>"


class MaterialCategory(Base):
    """教材カテゴリーモデル"""
    __tablename__ = "material_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # 関連付け
    materials = relationship("Material", back_populates="category")

    def __repr__(self):
        return f"<MaterialCategory(id={self.id}, name='{self.name}')>"


class LessonMaterial(Base):
    """レッスンと教材の中間テーブル"""
    __tablename__ = "lesson_materials"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    
    # 関連付け
    lesson = relationship("Lesson", back_populates="lesson_materials")
    material = relationship("Material", back_populates="lesson_materials")

    def __repr__(self):
        return f"<LessonMaterial(lesson_id={self.lesson_id}, material_id={self.material_id})>"