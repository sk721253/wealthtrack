# Create file: backend/app/routes/dashboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get complete financial dashboard"""
    dashboard_data = DashboardService.get_complete_dashboard(db, current_user.id)
    return dashboard_data

@router.get("/health-score")
def get_financial_health_score(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get financial health score and recommendations"""
    health_score = DashboardService.get_financial_health_score(db, current_user.id)
    return health_score