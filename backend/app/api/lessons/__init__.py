from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.core.schedule_manager import ScheduleManager
from app.core.payment_processor import PaymentProcessor
from app.core.security import get_current_user

# APIルーターの初期化
router = APIRouter()

class LessonConfig:
    """レッスン設定を管理するクラス"""
    
    def __init__(self):
        self.schedule_manager = ScheduleManager()
        self.payment_processor = PaymentProcessor()
        self.min_booking_notice = 24  # 予約に必要な最小時間（時間単位）
        self.max_advance_booking = 30  # 予約可能な最大先日数
        
    def get_available_slots(self, start_date: datetime, end_date: datetime) -> list:
        """利用可能なレッスン枠を取得"""
        return self.schedule_manager.get_available_slots(start_date, end_date)
    
    def update_settings(self, 
                       min_notice: Optional[int] = None,
                       max_advance: Optional[int] = None):
        """レッスン設定の更新"""
        if min_notice is not None:
            self.min_booking_notice = min_notice
        if max_advance is not None:
            self.max_advance_booking = max_advance

def setup_schedule():
    """
    スケジュール設定の初期化と設定
    """
    schedule_manager = ScheduleManager()
    try:
        schedule_manager.initialize()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to setup schedule: {str(e)}"
        )

def validate_booking(
    lesson_id: int,
    user_id: int,
    booking_time: datetime,
    lesson_config: LessonConfig = Depends(LessonConfig)
) -> bool:
    """
    予約のバリデーション
    
    Args:
        lesson_id: レッスンID
        user_id: ユーザーID
        booking_time: 予約時間
        lesson_config: レッスン設定
        
    Returns:
        bool: バリデーション結果
    """
    now = datetime.now()
    
    # 最小予約通知時間のチェック
    hours_until_lesson = (booking_time - now).total_seconds() / 3600
    if hours_until_lesson < lesson_config.min_booking_notice:
        raise HTTPException(
            status_code=400,
            detail=f"Booking must be made at least {lesson_config.min_booking_notice} hours in advance"
        )
    
    # 最大予約可能日数のチェック
    days_in_advance = (booking_time - now).days
    if days_in_advance > lesson_config.max_advance_booking:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot book more than {lesson_config.max_advance_booking} days in advance"
        )
    
    # スケジュールの利用可能性チェック
    if not lesson_config.schedule_manager.is_slot_available(booking_time):
        raise HTTPException(
            status_code=400,
            detail="Selected time slot is not available"
        )
    
    return True

# 必要なエンドポイントをルーターに登録
@router.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化処理"""
    setup_schedule()