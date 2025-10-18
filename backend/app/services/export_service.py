# Create file: backend/app/services/export_service.py

from sqlalchemy.orm import Session
from app.models import Expense, Investment
from datetime import date
import csv
import io
import uuid

class ExportService:
    
    @staticmethod
    def export_expenses_csv(db: Session, user_id: uuid.UUID) -> str:
        """Export expenses to CSV format"""
        expenses = db.query(Expense).filter(Expense.user_id == user_id).order_by(Expense.date.desc()).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Date", "Title", "Amount", "Category", "Payment Method", "Notes"
        ])
        
        # Write data
        for expense in expenses:
            writer.writerow([
                expense.date.strftime("%Y-%m-%d"),
                expense.title,
                float(expense.amount),
                expense.category,
                expense.payment_method or "",
                expense.notes or ""
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_investments_csv(db: Session, user_id: uuid.UUID) -> str:
        """Export investments to CSV format"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).order_by(Investment.purchase_date.desc()).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "Asset Type", "Asset Name", "Symbol", "Quantity", "Purchase Price",
            "Current Price", "Purchase Date", "Invested Amount", "Current Value",
            "Absolute Gain", "Percentage Gain", "Days Held", "Platform", "Notes"
        ])
        
        # Write data
        for inv in investments:
            writer.writerow([
                inv.asset_type,
                inv.asset_name,
                inv.symbol or "",
                float(inv.quantity),
                float(inv.purchase_price),
                float(inv.current_price),
                inv.purchase_date.strftime("%Y-%m-%d"),
                float(inv.invested_amount),
                float(inv.current_value),
                float(inv.absolute_gain),
                inv.percentage_gain,
                inv.days_held,
                inv.platform or "",
                inv.notes or ""
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_complete_portfolio(db: Session, user_id: uuid.UUID) -> dict:
        """Export complete financial data as JSON"""
        from app.services.expense_service import ExpenseService
        from app.services.investment_service import InvestmentService
        from app.services.dashboard_service import DashboardService
        
        # Get all data
        expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        # Get summaries
        expense_summary = {
            "total_amount": float(ExpenseService.get_total_amount(db, user_id)),
            "total_count": ExpenseService.get_expense_count(db, user_id),
            "by_category": ExpenseService.get_category_summary(db, user_id)
        }
        
        portfolio_summary = InvestmentService.calculate_portfolio_summary(db, user_id)
        dashboard_data = DashboardService.get_complete_dashboard(db, user_id)
        
        # Format expenses
        expense_list = [
            {
                "id": str(exp.id),
                "date": exp.date.isoformat(),
                "title": exp.title,
                "amount": float(exp.amount),
                "category": exp.category,
                "payment_method": exp.payment_method,
                "notes": exp.notes
            }
            for exp in expenses
        ]
        
        # Format investments
        investment_list = [
            {
                "id": str(inv.id),
                "asset_type": inv.asset_type,
                "asset_name": inv.asset_name,
                "symbol": inv.symbol,
                "quantity": float(inv.quantity),
                "purchase_price": float(inv.purchase_price),
                "current_price": float(inv.current_price),
                "purchase_date": inv.purchase_date.isoformat(),
                "maturity_date": inv.maturity_date.isoformat() if inv.maturity_date else None,
                "invested_amount": float(inv.invested_amount),
                "current_value": float(inv.current_value),
                "absolute_gain": float(inv.absolute_gain),
                "percentage_gain": inv.percentage_gain,
                "days_held": inv.days_held,
                "platform": inv.platform,
                "interest_rate": float(inv.interest_rate) if inv.interest_rate else None,
                "notes": inv.notes
            }
            for inv in investments
        ]
        
        return {
            "export_date": date.today().isoformat(),
            "user_id": str(user_id),
            "expenses": {
                "summary": expense_summary,
                "data": expense_list
            },
            "investments": {
                "summary": {
                    "total_invested": float(portfolio_summary.total_invested),
                    "total_current_value": float(portfolio_summary.total_current_value),
                    "total_gain_loss": float(portfolio_summary.total_gain_loss),
                    "gain_loss_percentage": portfolio_summary.total_gain_loss_percentage,
                    "total_investments": portfolio_summary.total_investments,
                    "asset_allocation": portfolio_summary.asset_type_breakdown
                },
                "data": investment_list
            },
            "dashboard": dashboard_data
        }