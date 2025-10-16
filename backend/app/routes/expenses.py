# Open backend/app/routes/expenses.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
import uuid

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseListResponse
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new expense"""
    expense = ExpenseService.create_expense(db, expense_data, current_user.id)
    return expense

@router.get("/", response_model=ExpenseListResponse)
def get_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get list of expenses with optional filters"""
    expenses = ExpenseService.get_expenses(
        db, current_user.id, skip, limit, category, start_date, end_date
    )
    
    total_count = ExpenseService.get_expense_count(
        db, current_user.id, category, start_date, end_date
    )
    
    total_amount = ExpenseService.get_total_amount(
        db, current_user.id, category, start_date, end_date
    )
    
    return {
        "expenses": expenses,
        "total_count": total_count,
        "total_amount": total_amount
    }

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a single expense by ID"""
    expense = ExpenseService.get_expense_by_id(db, expense_id, current_user.id)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: uuid.UUID,
    expense_data: ExpenseUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an expense"""
    expense = ExpenseService.update_expense(db, expense_id, current_user.id, expense_data)
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an expense"""
    success = ExpenseService.delete_expense(db, expense_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    return None

@router.get("/summary/by-category", response_model=List[dict])
def get_category_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get expense summary by category"""
    summary = ExpenseService.get_category_summary(
        db, current_user.id, start_date, end_date
    )
    return summary

@router.get("/summary/by-month", response_model=List[dict])
def get_monthly_summary(
    year: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get monthly expense summary"""
    summary = ExpenseService.get_monthly_summary(db, current_user.id, year)
    return summary