from .auth import (
    UserCreate,
    UserUpdate,
    UserInDB,
    UserResponse,
    TokenResponse,
    PasswordReset,
    InvitationVerify
)

from .lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    LessonBooking,
    LessonReschedule,
    LessonList
)

from .payment import (
    PaymentIntent,
    PaymentConfirm,
    PaymentHistory,
    PaymentResponse
)

from .material import (
    MaterialCreate,
    MaterialResponse,
    MaterialDownload,
    MaterialList
)

# APIで使用する全てのスキーマをここでエクスポート
__all__ = [
    # Auth関連スキーマ
    "UserCreate",
    "UserUpdate",
    "UserInDB",
    "UserResponse",
    "TokenResponse",
    "PasswordReset",
    "InvitationVerify",
    
    # レッスン関連スキーマ
    "LessonCreate",
    "LessonUpdate",
    "LessonResponse",
    "LessonBooking",
    "LessonReschedule",
    "LessonList",
    
    # 支払い関連スキーマ
    "PaymentIntent",
    "PaymentConfirm",
    "PaymentHistory",
    "PaymentResponse",
    
    # 教材関連スキーマ
    "MaterialCreate",
    "MaterialResponse",
    "MaterialDownload",
    "MaterialList"
]