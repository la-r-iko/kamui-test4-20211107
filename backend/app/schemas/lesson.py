from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class LessonStatus(str, Enum):
    """レッスンのステータスを定義する列挙型"""
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"

class LessonType(str, Enum):
    """レッスンタイプを定義する列挙型"""
    ONE_ON_ONE = "one_on_one"
    GROUP = "group"
    WORKSHOP = "workshop"

class LessonLevel(str, Enum):
    """レッスンレベルを定義する列挙型"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LessonBase(BaseModel):
    """レッスンの基本情報を定義するベースモデル"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    duration: int = Field(..., ge=30, le=180)  # 分単位
    lesson_type: LessonType
    level: LessonLevel
    max_participants: Optional[int] = Field(default=1, ge=1)
    price: float = Field(..., ge=0)

class LessonCreate(LessonBase):
    """レッスン作成時に使用するモデル"""
    instructor_id: int
    scheduled_at: datetime
    
class LessonUpdate(BaseModel):
    """レッスン更新時に使用するモデル"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    duration: Optional[int] = Field(None, ge=30, le=180)
    lesson_type: Optional[LessonType] = None
    level: Optional[LessonLevel] = None
    max_participants: Optional[int] = Field(None, ge=1)
    price: Optional[float] = Field(None, ge=0)
    status: Optional[LessonStatus] = None
    scheduled_at: Optional[datetime] = None

class LessonInDB(LessonBase):
    """データベースに保存されているレッスン情報を表すモデル"""
    id: int
    instructor_id: int
    scheduled_at: datetime
    created_at: datetime
    updated_at: datetime
    status: LessonStatus = LessonStatus.SCHEDULED
    current_participants: int = 0

    class Config:
        orm_mode = True

class LessonResponse(LessonInDB):
    """APIレスポンスとして返すレッスン情報モデル"""
    instructor_name: str
    is_bookable: bool
    remaining_slots: int

class LessonBooking(BaseModel):
    """レッスン予約時に使用するモデル"""
    lesson_id: int
    student_id: int
    notes: Optional[str] = Field(None, max_length=500)

class LessonCancellation(BaseModel):
    """レッスンキャンセル時に使用するモデル"""
    lesson_id: int
    cancellation_reason: Optional[str] = Field(None, max_length=500)

class LessonSearch(BaseModel):
    """レッスン検索時に使用するモデル"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    lesson_type: Optional[LessonType] = None
    level: Optional[LessonLevel] = None
    instructor_id: Optional[int] = None
    price_min: Optional[float] = Field(None, ge=0)
    price_max: Optional[float] = Field(None, ge=0)