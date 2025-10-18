# Create file: backend/app/services/dashboard_service.py

from sqlalchemy.orm import Session
from app.services.expense_service import ExpenseService
from app.services.investment_service import InvestmentService
from datetime import date, timedelta
from decimal import Decimal
import uuid

class DashboardService:
    
    @staticmethod
    def get_complete_dashboard(db: Session, user_id: uuid.UUID) -> dict:
        """Get complete financial dashboard data"""
        
        # Current month date range
        today = date.today()
        first_day_of_month = today.replace(day=1)
        
        # Last month date range
        if today.month == 1:
            last_month = 12
            last_month_year = today.year - 1
        else:
            last_month = today.month - 1
            last_month_year = today.year
        
        first_day_last_month = date(last_month_year, last_month, 1)
        last_day_last_month = first_day_of_month - timedelta(days=1)
        
        # === EXPENSES DATA ===
        # Current month expenses
        current_month_total = ExpenseService.get_total_amount(
            db, user_id, start_date=first_day_of_month, end_date=today
        )
        current_month_count = ExpenseService.get_expense_count(
            db, user_id, start_date=first_day_of_month, end_date=today
        )
        
        # Last month expenses
        last_month_total = ExpenseService.get_total_amount(
            db, user_id, start_date=first_day_last_month, end_date=last_day_last_month
        )
        
        # All time expenses
        total_expenses_all_time = ExpenseService.get_total_amount(db, user_id)
        total_expense_count = ExpenseService.get_expense_count(db, user_id)
        
        # Category breakdown
        expense_categories = ExpenseService.get_category_summary(
            db, user_id, start_date=first_day_of_month
        )
        
        # === INVESTMENTS DATA ===
        portfolio = InvestmentService.calculate_portfolio_summary(db, user_id)
        asset_allocation = InvestmentService.get_asset_allocation(db, user_id)
        top_performers = InvestmentService.get_top_performers(db, user_id, limit=5)
        
        # === COMBINED METRICS ===
        # Net worth (investments - doesn't include cash)
        net_worth = float(portfolio.total_current_value)
        
        # Month over month expense change
        if last_month_total > 0:
            expense_change_percentage = float(
                ((current_month_total - last_month_total) / last_month_total) * 100
            )
        else:
            expense_change_percentage = 0.0
        
        # Savings rate (if we have income data in future)
        # For now, just show investment vs expenses ratio
        
        return {
            "summary": {
                "net_worth": net_worth,
                "total_invested": float(portfolio.total_invested),
                "investment_gains": float(portfolio.total_gain_loss),
                "investment_gains_percentage": portfolio.total_gain_loss_percentage,
                "current_month_expenses": float(current_month_total),
                "last_month_expenses": float(last_month_total),
                "expense_change_percentage": expense_change_percentage,
                "total_investments": portfolio.total_investments,
                "total_expenses_count": total_expense_count,
            },
            "expenses": {
                "current_month_total": float(current_month_total),
                "current_month_count": current_month_count,
                "all_time_total": float(total_expenses_all_time),
                "all_time_count": total_expense_count,
                "top_categories": expense_categories[:5],  # Top 5 categories
            },
            "investments": {
                "portfolio_value": float(portfolio.total_current_value),
                "total_invested": float(portfolio.total_invested),
                "total_gains": float(portfolio.total_gain_loss),
                "gains_percentage": portfolio.total_gain_loss_percentage,
                "asset_allocation": asset_allocation,
                "top_performers": [
                    {
                        "id": str(inv.id),
                        "asset_name": inv.asset_name,
                        "asset_type": inv.asset_type,
                        "percentage_gain": inv.percentage_gain,
                        "absolute_gain": float(inv.absolute_gain),
                        "current_value": float(inv.current_value)
                    }
                    for inv in top_performers
                ]
            },
            "month_overview": {
                "current_month": today.strftime("%B %Y"),
                "days_in_month": today.day,
                "average_daily_expense": float(current_month_total / today.day) if today.day > 0 else 0
            }
        }
    
    @staticmethod
    def get_financial_health_score(db: Session, user_id: uuid.UUID) -> dict:
        """Calculate financial health score (0-100)"""
        score = 100
        issues = []
        recommendations = []
        
        # Get data
        portfolio = InvestmentService.calculate_portfolio_summary(db, user_id)
        today = date.today()
        first_day_of_month = today.replace(day=1)
        monthly_expenses = ExpenseService.get_total_amount(
            db, user_id, start_date=first_day_of_month
        )
        
        # Check 1: Investment diversity (-20 if less than 3 asset types)
        if portfolio.total_investments > 0:
            asset_types = len(portfolio.asset_type_breakdown)
            if asset_types < 3:
                score -= 20
                issues.append("Low investment diversity")
                recommendations.append("Consider diversifying across more asset types")
        else:
            score -= 30
            issues.append("No investments")
            recommendations.append("Start investing to build wealth")
        
        # Check 2: Investment performance (-15 if negative returns)
        if portfolio.total_gain_loss_percentage < 0:
            score -= 15
            issues.append("Portfolio in loss")
            recommendations.append("Review and rebalance your portfolio")
        elif portfolio.total_gain_loss_percentage > 15:
            score += 10  # Bonus for good returns
        
        # Check 3: Expense tracking (-10 if no expenses this month)
        if monthly_expenses == 0:
            score -= 10
            issues.append("No expenses tracked this month")
            recommendations.append("Track your expenses regularly")
        
        # Check 4: Emergency fund (FD investments)
        fd_count = sum(
            1 for asset in portfolio.asset_type_breakdown
            if asset["asset_type"] == "FD"
        )
        if fd_count == 0:
            score -= 15
            issues.append("No emergency fund (FD)")
            recommendations.append("Maintain 6 months of expenses in FD")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine rating
        if score >= 80:
            rating = "Excellent"
            color = "green"
        elif score >= 60:
            rating = "Good"
            color = "blue"
        elif score >= 40:
            rating = "Fair"
            color = "yellow"
        else:
            rating = "Needs Improvement"
            color = "red"
        
        return {
            "score": score,
            "rating": rating,
            "color": color,
            "issues": issues,
            "recommendations": recommendations
        }