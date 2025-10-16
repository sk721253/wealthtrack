# Open backend/app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

# Schema for user registration
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for user response (what API returns)
class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Enable ORM mode

# Schema for user update
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None