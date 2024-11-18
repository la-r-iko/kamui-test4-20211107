from datetime import datetime, timedelta
from typing import List, Optional, Dict
from fastapi import HTTPException
import pytz
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.core.config import settings

class ScheduleManager:
    """スケジュール管理を行うクラス"""
    
    def __init__(self, db: Session):
        self.db = db
        self.timezone = pytz.timezone(settings.TIMEZONE)

    async def get_available_slots(
        self, 
        teacher_id: int, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict]:
        """利用可能な時間枠を取得する"""
        # 既存の予約を取得
        existing_lessons = self.db.query(Lesson).filter(
            Lesson.teacher_id == teacher_id,
            Lesson.start_time >= start_date,
            Lesson.end_time <= end_date
        ).all()

        # 利用可能な時間枠を生成
        available_slots = []
        current_time = start_date

        while current_time < end_date:
            # 営業時間内かチェック
            if self._is_business_hours(current_time):
                # 既存の予約と重複していないかチェック
                if not self._is_slot_booked(current_time, existing_lessons):
                    available_slots.append({
                        "start_time": current_time,
                        "end_time": current_time + timedelta(minutes=settings.LESSON_DURATION)
                    })
            current_time += timedelta(minutes=settings.SLOT_INTERVAL)

        return available_slots

    def create_schedule(self, schedule: ScheduleCreate) -> Lesson:
        """新しいスケジュールを作成する"""
        # 時間枠の重複チェック
        if self._check_schedule_conflict(schedule.start_time, schedule.end_time):
            raise HTTPException(
                status_code=400,
                detail="Schedule conflict detected"
            )

        # スケジュールの作成
        db_schedule = Lesson(
            teacher_id=schedule.teacher_id,
            student_id=schedule.student_id,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            status="scheduled"
        )
        
        self.db.add(db_schedule)
        self.db.commit()
        self.db.refresh(db_schedule)
        
        return db_schedule

    def update_schedule(self, schedule_id: int, schedule: ScheduleUpdate) -> Lesson:
        """スケジュールを更新する"""
        db_schedule = self.db.query(Lesson).filter(Lesson.id == schedule_id).first()
        if not db_schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        # 更新可能かチェック
        if not self._can_update_schedule(db_schedule):
            raise HTTPException(
                status_code=400,
                detail="Schedule cannot be updated"
            )

        # 時間枠の重複チェック（現在のスケジュールを除く）
        if self._check_schedule_conflict(
            schedule.start_time, 
            schedule.end_time,
            exclude_id=schedule_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Schedule conflict detected"
            )

        # スケジュールの更新
        for key, value in schedule.dict(exclude_unset=True).items():
            setattr(db_schedule, key, value)

        self.db.commit()
        self.db.refresh(db_schedule)
        
        return db_schedule

    def _is_business_hours(self, time: datetime) -> bool:
        """営業時間内かどうかをチェックする"""
        local_time = time.astimezone(self.timezone)
        hour = local_time.hour
        
        # 営業時間（9:00-21:00）内かチェック
        return settings.BUSINESS_HOURS_START <= hour < settings.BUSINESS_HOURS_END

    def _is_slot_booked(self, start_time: datetime, existing_lessons: List[Lesson]) -> bool:
        """指定された時間枠が既に予約されているかチェックする"""
        end_time = start_time + timedelta(minutes=settings.LESSON_DURATION)
        
        for lesson in existing_lessons:
            if (start_time < lesson.end_time and end_time > lesson.start_time):
                return True
        return False

    def _check_schedule_conflict(
        self, 
        start_time: datetime, 
        end_time: datetime,
        exclude_id: Optional[int] = None
    ) -> bool:
        """スケジュールの重複をチェックする"""
        query = self.db.query(Lesson).filter(
            Lesson.start_time < end_time,
            Lesson.end_time > start_time
        )
        
        if exclude_id:
            query = query.filter(Lesson.id != exclude_id)
            
        return query.first() is not None

    def _can_update_schedule(self, schedule: Lesson) -> bool:
        """スケジュールが更新可能かチェックする"""
        # キャンセル済みのスケジュールは更新不可
        if schedule.status == "cancelled":
            return False
            
        # 過去のスケジュールは更新不可
        if schedule.start_time < datetime.now(pytz.UTC):
            return False
            
        return True