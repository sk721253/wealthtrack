# Open backend/app/models/investment.py

from sqlalchemy import Column, String, Numeric, Date, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import date
from decimal import Decimal
from app.database import Base

class Investment(Base):
    __tablename__ = "investments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Basic Information
    asset_type = Column(String(50), nullable=False, index=True)
    asset_name = Column(String(200), nullable=False)
    symbol = Column(String(20), nullable=True)  # Stock/Crypto ticker symbol
    
    # Quantity & Pricing
    quantity = Column(Numeric(20, 8), nullable=False)  # Support crypto decimals (e.g., 0.00123456 BTC)
    purchase_price = Column(Numeric(15, 2), nullable=False)  # Price per unit
    current_price = Column(Numeric(15, 2), nullable=False)   # Current price per unit
    
    # Dates
    purchase_date = Column(Date, nullable=False, index=True)
    maturity_date = Column(Date, nullable=True)  # For FDs, Bonds
    
    # Additional Information
    platform = Column(String(100), nullable=True)  # Broker/Platform name
    interest_rate = Column(Numeric(5, 2), nullable=True)  # For FDs, Bonds (%)
    notes = Column(String(500), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="investments")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('purchase_price > 0', name='check_purchase_price_positive'),
        CheckConstraint('current_price >= 0', name='check_current_price_non_negative'),
    )
    
    def __repr__(self):
        return f"<Investment {self.asset_name}: {self.quantity} units @ ₹{self.current_price}>"
    
    # Calculated Properties
    @property
    def invested_amount(self) -> Decimal:
        """Total amount invested (quantity × purchase_price)"""
        return Decimal(str(self.quantity)) * Decimal(str(self.purchase_price))
    
    @property
    def current_value(self) -> Decimal:
        """Current market value (quantity × current_price)"""
        return Decimal(str(self.quantity)) * Decimal(str(self.current_price))
    
    @property
    def absolute_gain(self) -> Decimal:
        """Absolute gain/loss (current_value - invested_amount)"""
        return self.current_value - self.invested_amount
    
    @property
    def percentage_gain(self) -> float:
        """Percentage gain/loss"""
        if self.invested_amount == 0:
            return 0.0
        return float((self.absolute_gain / self.invested_amount) * 100)
    
    @property
    def days_held(self) -> int:
        """Number of days investment is held"""
        return (date.today() - self.purchase_date).days
    
    @property
    def is_matured(self) -> bool:
        """Check if investment has matured (for FDs, Bonds)"""
        if self.maturity_date:
            return date.today() >= self.maturity_date
        return False