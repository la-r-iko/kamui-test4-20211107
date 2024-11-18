from fastapi import APIRouter
from typing import Optional
from pydantic import BaseSettings
from core.security import get_password_hash, verify_password, create_access_token
from core.email_service import EmailService

# 認証関連の設定クラス
class AuthConfig(BaseSettings):
    """認証に関する設定を管理するクラス"""
    SECRET_KEY: str = "your-secret-key"  # 本番環境では環境変数から取得すべき
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24
    INVITATION_TOKEN_EXPIRE_DAYS: int = 7
    MIN_PASSWORD_LENGTH: int = 8
    
    # メール関連の設定
    VERIFICATION_EMAIL_SUBJECT: str = "メールアドレス認証"
    PASSWORD_RESET_EMAIL_SUBJECT: str = "パスワードリセット"
    INVITATION_EMAIL_SUBJECT: str = "招待"
    
    class Config:
        case_sensitive = True
        env_prefix = "AUTH_"

# ルーターの初期化
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

# グローバル設定インスタンス
auth_config = AuthConfig()

# メールサービスインスタンス
email_service = EmailService()

# 認証関連の依存関係をエクスポート
__all__ = [
    "router",
    "auth_config",
    "email_service",
    "get_password_hash",
    "verify_password",
    "create_access_token"
]

# 以下のファイルからルートをインポート
from .routes import login, signup, password_reset, invitation

# ルートの登録
router.include_router(login.router)
router.include_router(signup.router)
router.include_router(password_reset.router)
router.include_router(invitation.router)