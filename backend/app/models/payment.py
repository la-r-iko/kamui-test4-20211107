from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base

class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"

class Payment(Base):
    """
    決済情報を管理するモデル
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    
    stripe_payment_intent_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    
    description = Column(String(500), nullable=True)
    metadata = Column(String(1000), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # リレーションシップ
    user = relationship("User", back_populates="payments")
    lesson = relationship("Lesson", back_populates="payment")

    @property
    def is_completed(self):
        """支払いが完了しているかどうかを確認"""
        return self.status == PaymentStatus.COMPLETED

    @property
    def can_refund(self):
        """返金可能かどうかを確認"""
        return self.status == PaymentStatus.COMPLETED and not self.is_refunded

    @property
    def is_refunded(self):
        """返金済みかどうかを確認"""
        return self.status == PaymentStatus.REFUNDED

    def complete_payment(self):
        """支払い完了処理"""
        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def refund_payment(self):
        """返金処理"""
        if self.can_refund:
            self.status = PaymentStatus.REFUNDED
            self.updated_at = datetime.utcnow()

    def cancel_payment(self):
        """支払いキャンセル処理"""
        if self.status == PaymentStatus.PENDING:
            self.status = PaymentStatus.CANCELLED
            self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount}, status={self.status.value})>"