from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentUpdate, PortfolioSummary
from typing import Optional, List
from datetime import date, timedelta, datetime
from decimal import Decimal
from collections import defaultdict
import uuid

class InvestmentService:
    
    @staticmethod
    def create_investment(db: Session, investment_data: InvestmentCreate, user_id: uuid.UUID) -> Investment:
        """Create a new investment"""
        db_investment = Investment(
            **investment_data.model_dump(),
            user_id=user_id
        )
        db.add(db_investment)
        db.commit()
        db.refresh(db_investment)
        return db_investment
    
    @staticmethod
    def get_investment_by_id(db: Session, investment_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Investment]:
        """Get a single investment by ID"""
        return db.query(Investment).filter(
            Investment.id == investment_id,
            Investment.user_id == user_id
        ).first()
    
    @staticmethod
    def get_investments(
        db: Session,
        user_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        asset_type: Optional[str] = None,
        platform: Optional[str] = None
    ) -> List[Investment]:
        """Get list of investments with filters"""
        query = db.query(Investment).filter(Investment.user_id == user_id)
        
        if asset_type:
            query = query.filter(Investment.asset_type == asset_type)
        if platform:
            query = query.filter(Investment.platform == platform)
        
        investments = query.order_by(desc(Investment.purchase_date)).offset(skip).limit(limit).all()
        return investments
    
    @staticmethod
    def update_investment(
        db: Session,
        investment_id: uuid.UUID,
        user_id: uuid.UUID,
        investment_data: InvestmentUpdate
    ) -> Optional[Investment]:
        """Update an investment"""
        db_investment = InvestmentService.get_investment_by_id(db, investment_id, user_id)
        
        if not db_investment:
            return None
        
        update_data = investment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_investment, field, value)
        
        db.commit()
        db.refresh(db_investment)
        return db_investment
    
    @staticmethod
    def update_price(
        db: Session,
        investment_id: uuid.UUID,
        user_id: uuid.UUID,
        new_price: Decimal
    ) -> Optional[Investment]:
        """Quick update of current price"""
        db_investment = InvestmentService.get_investment_by_id(db, investment_id, user_id)
        
        if not db_investment:
            return None
        
        db_investment.current_price = new_price
        db.commit()
        db.refresh(db_investment)
        return db_investment
    
    @staticmethod
    def delete_investment(db: Session, investment_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """Delete an investment"""
        db_investment = InvestmentService.get_investment_by_id(db, investment_id, user_id)
        
        if not db_investment:
            return False
        
        db.delete(db_investment)
        db.commit()
        return True
    
    @staticmethod
    def get_investment_count(
        db: Session,
        user_id: uuid.UUID,
        asset_type: Optional[str] = None,
        platform: Optional[str] = None
    ) -> int:
        """Get count of investments"""
        query = db.query(func.count(Investment.id)).filter(Investment.user_id == user_id)
        
        if asset_type:
            query = query.filter(Investment.asset_type == asset_type)
        if platform:
            query = query.filter(Investment.platform == platform)
        
        return query.scalar()
    
    @staticmethod
    def calculate_portfolio_summary(db: Session, user_id: uuid.UUID) -> PortfolioSummary:
        """Calculate complete portfolio summary"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        if not investments:
            return PortfolioSummary(
                total_invested=Decimal("0.00"),
                total_current_value=Decimal("0.00"),
                total_gain_loss=Decimal("0.00"),
                total_gain_loss_percentage=0.0,
                total_investments=0,
                asset_type_breakdown=[]
            )
        
        total_invested = sum(inv.invested_amount for inv in investments)
        total_current_value = sum(inv.current_value for inv in investments)
        total_gain_loss = total_current_value - total_invested
        
        total_gain_loss_percentage = float((total_gain_loss / total_invested) * 100) if total_invested > 0 else 0.0
        
        asset_breakdown = {}
        for inv in investments:
            if inv.asset_type not in asset_breakdown:
                asset_breakdown[inv.asset_type] = {
                    "asset_type": inv.asset_type,
                    "count": 0,
                    "invested": Decimal("0.00"),
                    "current_value": Decimal("0.00"),
                    "gain_loss": Decimal("0.00"),
                    "percentage_of_portfolio": 0.0
                }
            
            asset_breakdown[inv.asset_type]["count"] += 1
            asset_breakdown[inv.asset_type]["invested"] += inv.invested_amount
            asset_breakdown[inv.asset_type]["current_value"] += inv.current_value
            asset_breakdown[inv.asset_type]["gain_loss"] += inv.absolute_gain
        
        for asset_data in asset_breakdown.values():
            if total_current_value > 0:
                asset_data["percentage_of_portfolio"] = float(
                    (asset_data["current_value"] / total_current_value) * 100
                )
        
        asset_type_breakdown = sorted(
            asset_breakdown.values(),
            key=lambda x: x["current_value"],
            reverse=True
        )
        
        for asset in asset_type_breakdown:
            asset["invested"] = float(asset["invested"])
            asset["current_value"] = float(asset["current_value"])
            asset["gain_loss"] = float(asset["gain_loss"])
        
        return PortfolioSummary(
            total_invested=total_invested,
            total_current_value=total_current_value,
            total_gain_loss=total_gain_loss,
            total_gain_loss_percentage=total_gain_loss_percentage,
            total_investments=len(investments),
            asset_type_breakdown=asset_type_breakdown
        )
    
    @staticmethod
    def get_asset_allocation(db: Session, user_id: uuid.UUID) -> List[dict]:
        """Get asset allocation breakdown"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        if not investments:
            return []
        
        total_value = sum(inv.current_value for inv in investments)
        
        allocation = {}
        for inv in investments:
            if inv.asset_type not in allocation:
                allocation[inv.asset_type] = Decimal("0.00")
            allocation[inv.asset_type] += inv.current_value
        
        result = []
        for asset_type, value in allocation.items():
            percentage = float((value / total_value) * 100) if total_value > 0 else 0.0
            result.append({
                "asset_type": asset_type,
                "value": float(value),
                "percentage": percentage
            })
        
        result.sort(key=lambda x: x["value"], reverse=True)
        return result
    
    @staticmethod
    def get_top_performers(db: Session, user_id: uuid.UUID, limit: int = 5) -> List[Investment]:
        """Get top performing investments by percentage gain"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        sorted_investments = sorted(
            investments,
            key=lambda x: x.percentage_gain,
            reverse=True
        )
        
        return sorted_investments[:limit]
    
    @staticmethod
    def get_worst_performers(db: Session, user_id: uuid.UUID, limit: int = 5) -> List[Investment]:
        """Get worst performing investments by percentage gain"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        sorted_investments = sorted(
            investments,
            key=lambda x: x.percentage_gain
        )
        
        return sorted_investments[:limit]
    
    @staticmethod
    def get_maturing_soon(db: Session, user_id: uuid.UUID, days: int = 30) -> List[Investment]:
        """Get investments maturing within specified days"""
        today = date.today()
        cutoff_date = today + timedelta(days=days)
        
        investments = db.query(Investment).filter(
            Investment.user_id == user_id,
            Investment.maturity_date.isnot(None),
            Investment.maturity_date <= cutoff_date,
            Investment.maturity_date >= today
        ).order_by(Investment.maturity_date).all()
        
        return investments
    
    @staticmethod
    def get_platform_summary(db: Session, user_id: uuid.UUID) -> List[dict]:
        """Get investment summary grouped by platform"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        if not investments:
            return []
        
        platform_data = {}
        for inv in investments:
            platform = inv.platform or "Unknown"
            
            if platform not in platform_data:
                platform_data[platform] = {
                    "platform": platform,
                    "count": 0,
                    "total_invested": Decimal("0.00"),
                    "total_current_value": Decimal("0.00"),
                    "total_gain_loss": Decimal("0.00")
                }
            
            platform_data[platform]["count"] += 1
            platform_data[platform]["total_invested"] += inv.invested_amount
            platform_data[platform]["total_current_value"] += inv.current_value
            platform_data[platform]["total_gain_loss"] += inv.absolute_gain
        
        result = []
        for platform, data in platform_data.items():
            gain_loss_pct = float(
                (data["total_gain_loss"] / data["total_invested"] * 100)
                if data["total_invested"] > 0 else 0
            )
            result.append({
                "platform": platform,
                "count": data["count"],
                "total_invested": float(data["total_invested"]),
                "total_current_value": float(data["total_current_value"]),
                "total_gain_loss": float(data["total_gain_loss"]),
                "gain_loss_percentage": gain_loss_pct
            })
        
        result.sort(key=lambda x: x["total_current_value"], reverse=True)
        return result
    
    @staticmethod
    def bulk_update_prices(db: Session, user_id: uuid.UUID, price_updates: List[dict]) -> dict:
        """
        Bulk update prices for multiple investments
        price_updates format: [{"id": "uuid", "current_price": 123.45}, ...]
        """
        updated_count = 0
        failed_updates = []
        
        for update in price_updates:
            try:
                investment_id = uuid.UUID(update["id"])
                new_price = Decimal(str(update["current_price"]))
                
                investment = InvestmentService.update_price(db, investment_id, user_id, new_price)
                
                if investment:
                    updated_count += 1
                else:
                    failed_updates.append({
                        "id": update["id"],
                        "error": "Investment not found"
                    })
            except Exception as e:
                failed_updates.append({
                    "id": update.get("id", "unknown"),
                    "error": str(e)
                })
        
        return {
            "updated_count": updated_count,
            "failed_count": len(failed_updates),
            "failed_updates": failed_updates
        }
    
    #Trend Analysis
    @staticmethod
    def get_performance_trends(db: Session, user_id: uuid.UUID, days: int = 30) -> dict:
        """
        Get investment performance trends
        Note: This is simplified. In production, you'd track historical prices
        """
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        if not investments:
            return {
                "message": "No investments found",
                "trends": []
            }
        
        # Group by purchase date to show portfolio growth over time
        date_investments = defaultdict(list)
        for inv in investments:
            date_investments[inv.purchase_date].append(inv)
        
        # Create timeline
        sorted_dates = sorted(date_investments.keys())
        timeline = []
        cumulative_invested = Decimal("0")
        
        for inv_date in sorted_dates:
            invs = date_investments[inv_date]
            for inv in invs:
                cumulative_invested += inv.invested_amount
            
            # Calculate current value at this point
            current_value = sum(
                inv.current_value for inv in investments
                if inv.purchase_date <= inv_date
            )
            
            timeline.append({
                "date": inv_date.isoformat(),
                "invested_amount": float(cumulative_invested),
                "investments_count": sum(len(date_investments[d]) for d in sorted_dates if d <= inv_date)
            })
        
        return {
            "timeline": timeline,
            "total_data_points": len(timeline)
        }
    
    @staticmethod
    def get_investment_statistics(db: Session, user_id: uuid.UUID) -> dict:
        """Get detailed investment statistics"""
        investments = db.query(Investment).filter(Investment.user_id == user_id).all()
        
        if not investments:
            return {
                "message": "No investments found"
            }
        
        # Calculate various statistics
        total_invested = sum(inv.invested_amount for inv in investments)
        total_value = sum(inv.current_value for inv in investments)
        total_gains = sum(inv.absolute_gain for inv in investments)
        
        # Average holding period
        avg_days_held = sum(inv.days_held for inv in investments) / len(investments)
        
        # Best and worst investment
        best_investment = max(investments, key=lambda x: x.percentage_gain)
        worst_investment = min(investments, key=lambda x: x.percentage_gain)
        
        # Gains vs losses
        profitable = [inv for inv in investments if inv.absolute_gain > 0]
        loss_making = [inv for inv in investments if inv.absolute_gain < 0]
        break_even = [inv for inv in investments if inv.absolute_gain == 0]
        
        # Asset type performance
        asset_performance = {}
        for inv in investments:
            if inv.asset_type not in asset_performance:
                asset_performance[inv.asset_type] = {
                    "count": 0,
                    "total_invested": Decimal("0"),
                    "total_value": Decimal("0"),
                    "total_gains": Decimal("0")
                }
            
            asset_performance[inv.asset_type]["count"] += 1
            asset_performance[inv.asset_type]["total_invested"] += inv.invested_amount
            asset_performance[inv.asset_type]["total_value"] += inv.current_value
            asset_performance[inv.asset_type]["total_gains"] += inv.absolute_gain
        
        # Calculate percentages for each asset type
        for asset_type, data in asset_performance.items():
            if data["total_invested"] > 0:
                data["percentage_gain"] = float((data["total_gains"] / data["total_invested"]) * 100)
            else:
                data["percentage_gain"] = 0.0
            
            # Convert Decimals to float
            data["total_invested"] = float(data["total_invested"])
            data["total_value"] = float(data["total_value"])
            data["total_gains"] = float(data["total_gains"])
        
        return {
            "overview": {
                "total_investments": len(investments),
                "total_invested": float(total_invested),
                "total_value": float(total_value),
                "total_gains": float(total_gains),
                "overall_percentage": float((total_gains / total_invested * 100) if total_invested > 0 else 0),
                "average_days_held": int(avg_days_held)
            },
            "performance": {
                "profitable_count": len(profitable),
                "loss_making_count": len(loss_making),
                "break_even_count": len(break_even),
                "win_rate": float(len(profitable) / len(investments) * 100) if investments else 0
            },
            "extremes": {
                "best_performer": {
                    "asset_name": best_investment.asset_name,
                    "asset_type": best_investment.asset_type,
                    "percentage_gain": best_investment.percentage_gain,
                    "absolute_gain": float(best_investment.absolute_gain)
                },
                "worst_performer": {
                    "asset_name": worst_investment.asset_name,
                    "asset_type": worst_investment.asset_type,
                    "percentage_gain": worst_investment.percentage_gain,
                    "absolute_gain": float(worst_investment.absolute_gain)
                }
            },
            "asset_type_performance": asset_performance
        }