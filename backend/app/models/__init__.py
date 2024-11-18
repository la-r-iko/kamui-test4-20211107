# Import all models for easy access throughout the application
from .user import User
from .lesson import Lesson
from .material import Material
from .payment import Payment
from .invitation import Invitation
from .lesson_booking import LessonBooking
from .material_access import MaterialAccess
from .payment_history import PaymentHistory

# Define all models that should be available when importing from models
__all__ = [
    'User',
    'Lesson',
    'Material',
    'Payment',
    'Invitation',
    'LessonBooking',
    'MaterialAccess',
    'PaymentHistory',
]