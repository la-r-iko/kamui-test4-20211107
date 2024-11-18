from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime

from app.services import lesson_service
from app.schemas import lesson as lesson_schemas
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()

class LessonController:
    """レッスン予約に関する制御を行うコントローラークラス"""
    
    @router.post("/lessons/book", response_model=lesson_schemas.LessonBooking)
    async def book_lesson(
        lesson_request: lesson_schemas.LessonBookingCreate,
        current_user: User = Depends(get_current_user)
    ):
        """新規レッスンを予約するエンドポイント"""
        try:
            booking = await lesson_service.create_booking(
                user_id=current_user.id,
                lesson_data=lesson_request
            )
            return booking
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @router.get("/lessons/schedule", response_model=List[lesson_schemas.LessonSchedule])
    async def get_schedule(
        start_date: datetime = None,
        end_date: datetime = None,
        current_user: User = Depends(get_current_user)
    ):
        """ユーザーのレッスンスケジュールを取得するエンドポイント"""
        try:
            schedule = await lesson_service.get_user_schedule(
                user_id=current_user.id,
                start_date=start_date,
                end_date=end_date
            )
            return schedule
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @router.put("/lessons/{booking_id}", response_model=lesson_schemas.LessonBooking)
    async def update_booking(
        booking_id: int,
        update_data: lesson_schemas.LessonBookingUpdate,
        current_user: User = Depends(get_current_user)
    ):
        """既存のレッスン予約を更新するエンドポイント"""
        try:
            updated_booking = await lesson_service.update_booking(
                booking_id=booking_id,
                user_id=current_user.id,
                update_data=update_data
            )
            return updated_booking
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    @router.delete("/lessons/{booking_id}", response_model=lesson_schemas.LessonBookingDelete)
    async def cancel_booking(
        booking_id: int,
        current_user: User = Depends(get_current_user)
    ):
        """レッスン予約をキャンセルするエンドポイント"""
        try:
            result = await lesson_service.cancel_booking(
                booking_id=booking_id,
                user_id=current_user.id
            )
            return result
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

# レッスンコントローラーのインスタンスを作成
lesson_controller = LessonController()

# ルーターにエンドポイントを追加
router.include_router(router, prefix="/api", tags=["lessons"])