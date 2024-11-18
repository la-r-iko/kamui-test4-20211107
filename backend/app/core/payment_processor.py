from typing import Optional, Dict, Any
import stripe
from fastapi import HTTPException
from app.core.config import settings
from app.models.payment import PaymentIntent, PaymentConfirmation
from app.utils.logger import logger

class PaymentProcessor:
    def __init__(self):
        """Initialize the payment processor with Stripe configuration"""
        self.stripe = stripe
        self.stripe.api_key = settings.STRIPE_SECRET_KEY

    async def create_payment_intent(
        self, amount: int, currency: str = "usd", metadata: Optional[Dict[str, Any]] = None
    ) -> PaymentIntent:
        """
        Create a payment intent for processing payment
        
        Args:
            amount: Amount in cents
            currency: Currency code (default: usd)
            metadata: Additional metadata for the payment
            
        Returns:
            PaymentIntent object containing client secret and payment details
        """
        try:
            intent = self.stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={"enabled": True}
            )
            
            return PaymentIntent(
                client_secret=intent.client_secret,
                payment_intent_id=intent.id,
                amount=amount,
                currency=currency
            )
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error while creating payment intent: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Payment processing error: {str(e)}"
            )

    async def confirm_payment(self, payment_intent_id: str) -> PaymentConfirmation:
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: The ID of the payment intent to confirm
            
        Returns:
            PaymentConfirmation object with status and details
        """
        try:
            intent = self.stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return PaymentConfirmation(
                payment_intent_id=intent.id,
                status=intent.status,
                amount=intent.amount,
                currency=intent.currency
            )
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error while confirming payment: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Payment confirmation error: {str(e)}"
            )

    async def refund_payment(
        self, payment_intent_id: str, amount: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Refund a payment
        
        Args:
            payment_intent_id: The ID of the payment intent to refund
            amount: Optional amount to refund (if not specified, refunds entire amount)
            
        Returns:
            Dictionary containing refund details
        """
        try:
            refund_params = {"payment_intent": payment_intent_id}
            if amount:
                refund_params["amount"] = amount
                
            refund = self.stripe.Refund.create(**refund_params)
            
            return {
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount,
                "currency": refund.currency
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error while processing refund: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Refund processing error: {str(e)}"
            )

    async def get_payment_history(self, customer_id: str, limit: int = 10) -> Dict[str, Any]:
        """
        Retrieve payment history for a customer
        
        Args:
            customer_id: The Stripe customer ID
            limit: Maximum number of payments to retrieve
            
        Returns:
            Dictionary containing payment history details
        """
        try:
            payments = self.stripe.PaymentIntent.list(
                customer=customer_id,
                limit=limit
            )
            
            return {
                "payments": [
                    {
                        "payment_id": payment.id,
                        "amount": payment.amount,
                        "currency": payment.currency,
                        "status": payment.status,
                        "created": payment.created
                    }
                    for payment in payments.data
                ]
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error while retrieving payment history: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error retrieving payment history: {str(e)}"
            )

    async def handle_webhook_event(self, payload: Dict[str, Any], sig_header: str) -> Dict[str, Any]:
        """
        Handle Stripe webhook events
        
        Args:
            payload: The webhook event payload
            sig_header: The Stripe signature header
            
        Returns:
            Dictionary containing the processed event details
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
            
            # Handle different event types
            if event.type == "payment_intent.succeeded":
                await self._handle_payment_success(event.data.object)
            elif event.type == "payment_intent.payment_failed":
                await self._handle_payment_failure(event.data.object)
                
            return {"status": "success", "event_type": event.type}
            
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature in webhook: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid signature"
            )
        except Exception as e:
            logger.error(f"Error processing webhook: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Webhook processing error: {str(e)}"
            )

    async def _handle_payment_success(self, payment_intent: Dict[str, Any]) -> None:
        """Handle successful payment webhook event"""
        logger.info(f"Payment succeeded: {payment_intent.id}")
        # Implement success handling logic here

    async def _handle_payment_failure(self, payment_intent: Dict[str, Any]) -> None:
        """Handle failed payment webhook event"""
        logger.error(f"Payment failed: {payment_intent.id}")
        # Implement failure handling logic here