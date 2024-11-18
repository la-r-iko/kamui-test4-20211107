from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.services.payment import PaymentService
from app.schemas.payment import PaymentCreate, PaymentStatus
from app.core.config import Settings

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)

# 依存関係の注入
settings = Settings()
payment_service = PaymentService()

class PaymentProcessRequest(BaseModel):
    amount: float
    currency: str = "usd"
    payment_method: str
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str

@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    payment_data: PaymentProcessRequest,
    current_user = Depends(get_current_user)
):
    """
    決済処理を実行するエンドポイント
    
    Args:
        payment_data: 決済に必要な情報
        current_user: 認証されたユーザー情報
    
    Returns:
        PaymentResponse: 決済処理の結果
    """
    try:
        payment_result = await payment_service.process_payment(
            user_id=current_user.id,
            amount=payment_data.amount,
            currency=payment_data.currency,
            payment_method=payment_data.payment_method,
            description=payment_data.description
        )
        
        return PaymentResponse(
            payment_id=payment_result.id,
            status=payment_result.status,
            amount=payment_result.amount,
            currency=payment_result.currency
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/status/{payment_id}", response_model=PaymentStatus)
async def get_payment_status(
    payment_id: str,
    current_user = Depends(get_current_user)
):
    """
    決済状態を取得するエンドポイント
    
    Args:
        payment_id: 決済ID
        current_user: 認証されたユーザー情報
    
    Returns:
        PaymentStatus: 決済の現在の状態
    """
    try:
        payment_status = await payment_service.get_payment_status(
            payment_id=payment_id,
            user_id=current_user.id
        )
        
        if not payment_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
            
        return payment_status
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/webhook", include_in_schema=False)
async def payment_webhook(payload: Dict):
    """
    決済サービスからのWebhookを処理するエンドポイント
    
    Args:
        payload: Webhookペイロード
    """
    try:
        await payment_service.handle_webhook(payload)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )