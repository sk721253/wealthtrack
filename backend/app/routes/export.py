# Create file: backend/app/routes/export.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.services.export_service import ExportService

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/expenses/csv")
def export_expenses_csv(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export all expenses as CSV"""
    csv_data = ExportService.export_expenses_csv(db, current_user.id)
    
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"}
    )

@router.get("/investments/csv")
def export_investments_csv(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export all investments as CSV"""
    csv_data = ExportService.export_investments_csv(db, current_user.id)
    
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=investments.csv"}
    )

@router.get("/complete")
def export_complete_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export complete financial data as JSON"""
    data = ExportService.export_complete_portfolio(db, current_user.id)
    return data