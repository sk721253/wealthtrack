# Create file: backend/app/routes/investments.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
import uuid

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.investment import (
    InvestmentCreate,
    InvestmentUpdate,
    InvestmentResponse,
    PriceUpdate,
    InvestmentListResponse,
    ASSET_TYPES
)
from app.services.investment_service import InvestmentService


class BulkPriceUpdate(BaseModel):
    updates: List[dict] 

router = APIRouter(prefix="/api/investments", tags=["Investments"])

@router.post("/", response_model=InvestmentResponse, status_code=status.HTTP_201_CREATED)
def create_investment(
    investment_data: InvestmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new investment"""
    investment = InvestmentService.create_investment(db, investment_data, current_user.id)
    return investment

@router.get("/", response_model=InvestmentListResponse)
def get_investments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    asset_type: Optional[str] = Query(None, description=f"Filter by asset type: {', '.join(ASSET_TYPES)}"),
    platform: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of investments with optional filters"""
    investments = InvestmentService.get_investments(
        db, current_user.id, skip, limit, asset_type, platform
    )
    
    total_count = InvestmentService.get_investment_count(
        db, current_user.id, asset_type, platform
    )
    
    portfolio_summary = InvestmentService.calculate_portfolio_summary(db, current_user.id)
    
    return {
        "investments": investments,
        "total_count": total_count,
        "portfolio_summary": portfolio_summary
    }

@router.get("/{investment_id}", response_model=InvestmentResponse)
def get_investment(
    investment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a single investment by ID"""
    investment = InvestmentService.get_investment_by_id(db, investment_id, current_user.id)
    
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    return investment

@router.put("/{investment_id}", response_model=InvestmentResponse)
def update_investment(
    investment_id: uuid.UUID,
    investment_data: InvestmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an investment"""
    investment = InvestmentService.update_investment(
        db, investment_id, current_user.id, investment_data
    )
    
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    return investment

@router.patch("/{investment_id}/price", response_model=InvestmentResponse)
def update_investment_price(
    investment_id: uuid.UUID,
    price_data: PriceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Quick update of investment price"""
    investment = InvestmentService.update_price(
        db, investment_id, current_user.id, price_data.current_price
    )
    
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    return investment

@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
    investment_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an investment"""
    success = InvestmentService.delete_investment(db, investment_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    
    return None

# Analytics endpoints

@router.get("/analytics/asset-allocation", response_model=List[dict])
def get_asset_allocation(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get asset allocation breakdown"""
    allocation = InvestmentService.get_asset_allocation(db, current_user.id)
    return allocation

@router.get("/analytics/top-performers", response_model=List[InvestmentResponse])
def get_top_performers(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get top performing investments"""
    performers = InvestmentService.get_top_performers(db, current_user.id, limit)
    return performers

@router.get("/analytics/worst-performers", response_model=List[InvestmentResponse])
def get_worst_performers(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get worst performing investments"""
    performers = InvestmentService.get_worst_performers(db, current_user.id, limit)
    return performers

@router.get("/analytics/maturing-soon", response_model=List[InvestmentResponse])
def get_maturing_soon(
    days: int = Query(30, ge=1, le=365, description="Number of days to look ahead"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get investments maturing within specified days"""
    investments = InvestmentService.get_maturing_soon(db, current_user.id, days)
    return investments

@router.get("/analytics/platform-summary", response_model=List[dict])
def get_platform_summary(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get investment summary grouped by platform"""
    summary = InvestmentService.get_platform_summary(db, current_user.id)
    return summary

# Bulk Update

@router.post("/bulk-update-prices")
def bulk_update_prices(
    price_updates: BulkPriceUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Bulk update prices for multiple investments"""
    result = InvestmentService.bulk_update_prices(db, current_user.id, price_updates.updates)
    return result

#statistics

@router.get("/analytics/trends")
def get_performance_trends(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get investment performance trends over time"""
    trends = InvestmentService.get_performance_trends(db, current_user.id, days)
    return trends

@router.get("/analytics/statistics")
def get_investment_statistics(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed investment statistics"""
    statistics = InvestmentService.get_investment_statistics(db, current_user.id)
    return statistics