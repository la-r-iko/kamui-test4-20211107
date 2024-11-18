from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class PaymentBase(BaseModel):
    """支払い基本情報のベーススキーマ"""
    amount: Decimal = Field(..., description="支払い金額", ge=0)
    currency: str = Field(default="JPY", description="通貨コード")
    description: Optional[str] = Field(None, description="支払いの説明")

class PaymentCreate(PaymentBase):
    """支払い作成時のスキーマ"""
    user_id: int = Field(..., description="支払いを行うユーザーID")
    lesson_id: Optional[int] = Field(None, description="関連するレッスンID")
    payment_method_id: str = Field(..., description="Stripeの支払い方法ID")

class PaymentResponse(PaymentBase):
    """支払い情報レスポンススキーマ"""
    id: int = Field(..., description="支払いID")
    status: str = Field(..., description="支払いステータス")
    created_at: datetime = Field(..., description="作成日時")
    updated_at: datetime = Field(..., description="更新日時")
    payment_intent_id: Optional[str] = Field(None, description="StripeのPaymentIntentID")
    
    class Config:
        orm_mode = True

class PaymentIntent(BaseModel):
    """Stripe Payment Intent作成用スキーマ"""
    client_secret: str = Field(..., description="クライアントシークレット")
    payment_intent_id: str = Field(..., description="PaymentIntentID")

class PaymentConfirmation(BaseModel):
    """支払い確認用スキーマ"""
    payment_intent_id: str = Field(..., description="確認するPaymentIntentのID")
    payment_method_id: Optional[str] = Field(None, description="支払い方法ID")

class PaymentHistoryResponse(BaseModel):
    """支払い履歴レスポンススキーマ"""
    payments: List[PaymentResponse]
    total_count: int = Field(..., description="総支払い数")
    total_amount: Decimal = Field(..., description="総支払い金額")

class PaymentMethod(BaseModel):
    """支払い方法スキーマ"""
    id: str = Field(..., description="支払い方法ID")
    type: str = Field(..., description="支払い方法タイプ")
    card_brand: Optional[str] = Field(None, description="カードブランド")
    last4: Optional[str] = Field(None, description="カード番号下4桁")
    exp_month: Optional[int] = Field(None, description="有効期限(月)")
    exp_year: Optional[int] = Field(None, description="有効期限(年)")

    @validator('type')
    def validate_payment_type(cls, v):
        allowed_types = ['card', 'bank_transfer']
        if v not in allowed_types:
            raise ValueError(f"支払い方法は{allowed_types}のいずれかである必要があります")
        return v

class RefundCreate(BaseModel):
    """返金作成用スキーマ"""
    payment_id: int = Field(..., description="返金対象の支払いID")
    amount: Optional[Decimal] = Field(None, description="返金額（指定しない場合は全額返金）")
    reason: str = Field(..., description="返金理由")

class RefundResponse(BaseModel):
    """返金情報レスポンススキーマ"""
    id: int = Field(..., description="返金ID")
    payment_id: int = Field(..., description="返金された支払いID")
    amount: Decimal = Field(..., description="返金額")
    status: str = Field(..., description="返金ステータス")
    created_at: datetime = Field(..., description="返金日時")
    reason: str = Field(..., description="返金理由")

    class Config:
        orm_mode = True