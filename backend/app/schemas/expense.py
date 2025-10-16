# Open backend/app/schemas/expense.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import uuid

# Base schema
class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    category: str = Field(..., min_length=1, max_length=50)
    date: date
    payment_method: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)

# Schema for creating expense
class ExpenseCreate(ExpenseBase):
    pass

# Schema for updating expense
class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[date] = None # pyright: ignore[reportInvalidTypeForm]
    payment_method: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)

# Schema for expense response
class ExpenseResponse(ExpenseBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Schema for expense list with summary
class ExpenseListResponse(BaseModel):
    expenses: list[ExpenseResponse]
    total_count: int
    total_amount: Decimal