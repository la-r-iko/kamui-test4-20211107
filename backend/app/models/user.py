from sqlalchemy import Boolean, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from .base import Base
from ..utils.security import get_password_hash

class User(Base):
    """
    User model for the application.
    Stores user information and authentication details.
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    lessons = relationship("Lesson", back_populates="user")
    materials = relationship("Material", back_populates="user")
    payments = relationship("Payment", back_populates="user")

    def __init__(self, email: str, password: str, first_name: str = None, last_name: str = None):
        """
        Initialize a new user instance.
        
        Args:
            email (str): User's email address
            password (str): Plain text password to be hashed
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
        """
        self.email = email.lower()
        self.hashed_password = get_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self) -> str:
        """
        Get user's full name.
        
        Returns:
            str: Full name of the user
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def update_password(self, new_password: str) -> None:
        """
        Update user's password with a new hashed password.
        
        Args:
            new_password (str): New plain text password to be hashed
        """
        self.hashed_password = get_password_hash(new_password)
        self.updated_at = datetime.utcnow()

    def update_login_timestamp(self) -> None:
        """
        Update the last login timestamp for the user.
        """
        self.last_login = datetime.utcnow()

    def to_dict(self) -> dict:
        """
        Convert user instance to dictionary representation.
        
        Returns:
            dict: Dictionary containing user information
        """
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self) -> str:
        """
        String representation of the User instance.
        
        Returns:
            str: String representation
        """
        return f"<User {self.email}>"