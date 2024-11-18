from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from .base import Base

class LessonStatus(PyEnum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"

class LessonType(PyEnum):
    INDIVIDUAL = "individual"
    GROUP = "group"
    WORKSHOP = "workshop"

class Lesson(Base):
    """
    レッスンモデルの定義
    レッスンの基本情報、スケジュール、状態などを管理する
    """
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    
    # スケジュール関連
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # 分単位
    
    # レッスン情報
    lesson_type = Column(Enum(LessonType), nullable=False, default=LessonType.INDIVIDUAL)
    status = Column(Enum(LessonStatus), nullable=False, default=LessonStatus.PENDING)
    max_participants = Column(Integer, default=1)
    current_participants = Column(Integer, default=0)
    
    # 料金情報
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    # 関連情報
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True)
    
    # Zoom/Meet等のミーティング情報
    meeting_url = Column(String(255))
    meeting_id = Column(String(100))
    meeting_password = Column(String(100))
    
    # システム管理用
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # リレーションシップ
    teacher = relationship("User", back_populates="lessons")
    material = relationship("Material", back_populates="lessons")
    bookings = relationship("Booking", back_populates="lesson")

    def __init__(self, **kwargs):
        super(Lesson, self).__init__(**kwargs)
        if self.start_time and self.end_time:
            self.duration = int((self.end_time - self.start_time).total_seconds() / 60)

    def is_available(self) -> bool:
        """レッスンが予約可能かどうかを確認する"""
        return (
            self.is_active and
            self.status == LessonStatus.SCHEDULED and
            self.current_participants < self.max_participants
        )

    def add_participant(self) -> bool:
        """参加者を追加する"""
        if not self.is_available():
            return False
        self.current_participants += 1
        return True

    def remove_participant(self) -> bool:
        """参加者を削除する"""
        if self.current_participants > 0:
            self.current_participants -= 1
            return True
        return False

    def cancel(self) -> bool:
        """レッスンをキャンセルする"""
        if self.status == LessonStatus.SCHEDULED:
            self.status = LessonStatus.CANCELLED
            return True
        return False

    def complete(self) -> bool:
        """レッスンを完了状態にする"""
        if self.status == LessonStatus.SCHEDULED:
            self.status = LessonStatus.COMPLETED
            return True
        return False