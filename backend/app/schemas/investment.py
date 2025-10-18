# Open backend/app/schemas/investment.py

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
import uuid

# Asset type enum (for documentation)
ASSET_TYPES = ["Stock", "MutualFund", "FD", "Gold", "Crypto", "Bond", "Other"]

# Base schema
class InvestmentBase(BaseModel):
    asset_type: str = Field(..., description="Type of investment")
    asset_name: str = Field(..., min_length=1, max_length=200, description="Name of the asset")
    symbol: Optional[str] = Field(None, max_length=20, description="Stock/Crypto symbol")
    quantity: Decimal = Field(..., gt=0, description="Quantity/Units of the asset")
    purchase_price: Decimal = Field(..., gt=0, description="Purchase price per unit")
    current_price: Decimal = Field(..., ge=0, description="Current price per unit")
    purchase_date: date = Field(..., description="Date of purchase")
    maturity_date: Optional[date] = Field(None, description="Maturity date (for FDs, Bonds)")
    platform: Optional[str] = Field(None, max_length=100, description="Platform/Broker name")
    interest_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Interest rate (%)")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")
    
    @field_validator('asset_type')
    @classmethod
    def validate_asset_type(cls, v):
        if v not in ASSET_TYPES:
            raise ValueError(f'Asset type must be one of: {", ".join(ASSET_TYPES)}')
        return v
    
    @field_validator('maturity_date')
    @classmethod
    def validate_maturity_date(cls, v, info):
        if v and 'purchase_date' in info.data:
            if v <= info.data['purchase_date']:
                raise ValueError('Maturity date must be after purchase date')
        return v

# Schema for creating investment
class InvestmentCreate(InvestmentBase):
    pass

# Schema for updating investment
class InvestmentUpdate(BaseModel):
    asset_type: Optional[str] = Field(None, description="Type of investment")
    asset_name: Optional[str] = Field(None, min_length=1, max_length=200)
    symbol: Optional[str] = Field(None, max_length=20)
    quantity: Optional[Decimal] = Field(None, gt=0)
    purchase_price: Optional[Decimal] = Field(None, gt=0)
    current_price: Optional[Decimal] = Field(None, ge=0)
    purchase_date: Optional[date] = None
    maturity_date: Optional[date] = None
    platform: Optional[str] = Field(None, max_length=100)
    interest_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=500)

# Schema for investment response
class InvestmentResponse(InvestmentBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Calculated fields
    invested_amount: Decimal
    current_value: Decimal
    absolute_gain: Decimal
    percentage_gain: float
    days_held: int
    is_matured: bool
    
    class Config:
        from_attributes = True

# Schema for updating only current price (quick update)
class PriceUpdate(BaseModel):
    current_price: Decimal = Field(..., gt=0, description="Updated current price")

# Schema for portfolio summary
class PortfolioSummary(BaseModel):
    total_invested: float
    total_current_value: float
    total_gain_loss: float
    total_gain_loss_percentage: float
    total_investments: int
    asset_type_breakdown: list[dict]

# Schema for investment list response
class InvestmentListResponse(BaseModel):
    investments: list[InvestmentResponse]
    total_count: int
    portfolio_summary: PortfolioSummary