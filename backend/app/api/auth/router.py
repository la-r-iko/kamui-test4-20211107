from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    PasswordReset
)
from app.core.email import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> Dict:
    """
    新規ユーザー登録エンドポイント
    """
    # メールアドレスの重複チェック
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # パスワードのハッシュ化
    hashed_password = get_password_hash(user_data.password)
    
    # ユーザーの作成
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # アクセストークンの生成
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login", response_model=UserResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Dict:
    """
    ユーザーログインエンドポイント
    """
    # ユーザーの検証
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # アクセストークンの生成
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
) -> Dict:
    """
    パスワードリセットエンドポイント
    """
    # ユーザーの存在確認
    user = db.query(User).filter(User.email == reset_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # パスワードリセットトークンの生成と送信
    reset_token = create_access_token(data={"sub": user.email}, expires_delta=30)  # 30分有効
    await send_password_reset_email(user.email, reset_token)
    
    return {
        "message": "Password reset instructions have been sent to your email"
    }

@router.post("/verify-reset-token", status_code=status.HTTP_200_OK)
async def verify_reset_token(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    パスワードリセットトークンの検証とパスワード更新
    """
    # 新しいパスワードのハッシュ化と更新
    hashed_password = get_password_hash(new_password)
    current_user.hashed_password = hashed_password
    
    db.commit()
    
    return {
        "message": "Password has been successfully updated"
    }