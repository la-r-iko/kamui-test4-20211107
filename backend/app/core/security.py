from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT設定
SECRET_KEY = "your-secret-key-here"  # 本番環境では環境変数から取得すべき
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    プレーンパスワードとハッシュ化されたパスワードを比較検証する
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化する
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWTアクセストークンを生成する
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Security(oauth2_scheme)):
    """
    現在のユーザーを取得する
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # ここでユーザーをデータベースから取得する処理を追加
    # この例では省略していますが、実際の実装では必要です
    
    return user_id

def create_invitation_token(email: str) -> str:
    """
    招待用のトークンを生成する
    """
    expire = datetime.utcnow() + timedelta(days=7)  # 招待は7日間有効
    return create_access_token(
        data={"sub": email, "type": "invitation"},
        expires_delta=timedelta(days=7)
    )

def verify_invitation_token(token: str) -> Optional[str]:
    """
    招待トークンを検証する
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "invitation":
            return None
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None

class SecurityUtils:
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """
        パスワードの強度を検証する
        """
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        return True

    @staticmethod
    def sanitize_input(input_str: str) -> str:
        """
        入力文字列をサニタイズする
        """
        # 基本的なサニタイズ処理
        # 実際の実装ではより詳細な処理が必要
        return input_str.strip()
