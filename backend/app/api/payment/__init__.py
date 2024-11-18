"""
Payment API initialization module.
Handles payment configuration and processor initialization.
"""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
from core.payment_processor import PaymentProcessor
from core.security import SecurityConfig


class PaymentProvider(str, Enum):
    """Supported payment providers"""
    STRIPE = "stripe"
    PAYPAL = "paypal"


class PaymentConfig(BaseModel):
    """Payment configuration management class"""
    
    provider: PaymentProvider = Field(
        default=PaymentProvider.STRIPE,
        description="Payment provider to use"
    )
    api_key: str = Field(
        description="API key for the payment provider"
    )
    webhook_secret: Optional[str] = Field(
        default=None,
        description="Webhook secret for payment notifications"
    )
    test_mode: bool = Field(
        default=True,
        description="Whether to use test mode for payments"
    )
    currency: str = Field(
        default="USD",
        description="Default currency for payments"
    )

    class Config:
        use_enum_values = True

    def initialize_processor(self) -> PaymentProcessor:
        """
        Initialize and return a payment processor instance
        based on current configuration
        """
        security_config = SecurityConfig()
        return PaymentProcessor(
            provider=self.provider,
            api_key=security_config.encrypt_sensitive_data(self.api_key),
            webhook_secret=self.webhook_secret,
            test_mode=self.test_mode,
            currency=self.currency
        )

    @classmethod
    def get_default_config(cls) -> "PaymentConfig":
        """
        Returns a default payment configuration
        """
        return cls(
            provider=PaymentProvider.STRIPE,
            api_key="",
            test_mode=True,
            currency="USD"
        )


# Default payment configuration instance
default_payment_config = PaymentConfig.get_default_config()

__all__ = [
    "PaymentConfig",
    "PaymentProvider",
    "default_payment_config"
]