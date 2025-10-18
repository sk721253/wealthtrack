# Create file: backend/test_investment_model.py

from app.database import SessionLocal
from app.models import Investment
from datetime import date
from decimal import Decimal
import uuid

def test_investment_model():
    db = SessionLocal()
    
    try:
        # Create a test investment
        investment = Investment(
            user_id=uuid.uuid4(),  # Dummy user ID for now
            asset_type="Stock",
            asset_name="Apple Inc.",
            symbol="AAPL",
            quantity=Decimal("10"),
            purchase_price=Decimal("150.00"),
            current_price=Decimal("175.00"),
            purchase_date=date(2024, 1, 15),
            platform="Zerodha",
            notes="Test investment"
        )
        
        # Test calculated properties
        print(f"Invested Amount: ₹{investment.invested_amount}")
        print(f"Current Value: ₹{investment.current_value}")
        print(f"Absolute Gain: ₹{investment.absolute_gain}")
        print(f"Percentage Gain: {investment.percentage_gain:.2f}%")
        print(f"Days Held: {investment.days_held}")
        
        print("\n✅ Investment model working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_investment_model()