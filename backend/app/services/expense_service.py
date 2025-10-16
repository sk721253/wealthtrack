# Create new file: backend/app/services/expense_service.py

from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from typing import Optional, List
from datetime import date
import uuid
from decimal import Decimal

class ExpenseService:
    
    @staticmethod
    def create_expense(db: Session, expense_data: ExpenseCreate, user_id: uuid.UUID) -> Expense:
        """Create a new expense"""
        db_expense = Expense(
            **expense_data.model_dump(),
            user_id=user_id
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense
    
    @staticmethod
    def get_expense_by_id(db: Session, expense_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Expense]:
        """Get a single expense by ID"""
        return db.query(Expense).filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        ).first()
    
    @staticmethod
    def get_expenses(
        db: Session,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Expense]:
        """Get list of expenses with filters"""
        query = db.query(Expense).filter(Expense.user_id == user_id)
        
        # Apply filters
        if category:
            query = query.filter(Expense.category == category)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        # Order by date descending and apply pagination
        expenses = query.order_by(Expense.date.desc()).offset(skip).limit(limit).all()
        return expenses
    
    @staticmethod
    def get_total_amount(
        db: Session,
        user_id: uuid.UUID,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Decimal:
        """Get total amount of expenses"""
        query = db.query(func.sum(Expense.amount)).filter(Expense.user_id == user_id)
        
        if category:
            query = query.filter(Expense.category == category)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        total = query.scalar()
        return total if total else Decimal('0.00')
    
    @staticmethod
    def get_expense_count(
        db: Session,
        user_id: uuid.UUID,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> int:
        """Get count of expenses"""
        query = db.query(func.count(Expense.id)).filter(Expense.user_id == user_id)
        
        if category:
            query = query.filter(Expense.category == category)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        return query.scalar()
    
    @staticmethod
    def update_expense(
        db: Session,
        expense_id: uuid.UUID,
        user_id: uuid.UUID,
        expense_data: ExpenseUpdate
    ) -> Optional[Expense]:
        """Update an expense"""
        db_expense = ExpenseService.get_expense_by_id(db, expense_id, user_id)
        
        if not db_expense:
            return None
        
        # Update only provided fields
        update_data = expense_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        
        db.commit()
        db.refresh(db_expense)
        return db_expense
    
    @staticmethod
    def delete_expense(db: Session, expense_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete an expense"""
        db_expense = ExpenseService.get_expense_by_id(db, expense_id, user_id)
        
        if not db_expense:
            return False
        
        db.delete(db_expense)
        db.commit()
        return True
    
    @staticmethod
    def get_category_summary(
        db: Session,
        user_id: uuid.UUID,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[dict]:
        """Get spending summary by category"""
        query = db.query(
            Expense.category,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).filter(Expense.user_id == user_id)
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        results = query.group_by(Expense.category).all()
        
        return [
            {
                "category": category,
                "total_amount": float(total),
                "expense_count": count
            }
            for category, total, count in results
        ]
    
    @staticmethod
    def get_monthly_summary(
        db: Session,
        user_id: uuid.UUID,
        year: Optional[int] = None
    ) -> List[dict]:
        """Get monthly spending summary"""
        query = db.query(
            extract('year', Expense.date).label('year'),
            extract('month', Expense.date).label('month'),
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count')
        ).filter(Expense.user_id == user_id)
        
        if year:
            query = query.filter(extract('year', Expense.date) == year)
        
        results = query.group_by('year', 'month').order_by('year', 'month').all()
        
        return [
            {
                "year": int(year),
                "month": int(month),
                "total_amount": float(total),
                "expense_count": count
            }
            for year, month, total, count in results
        ]