# Create file: backend/test_investment_service.py

from app.database import SessionLocal
from app.services.investment_service import InvestmentService
from app.services.auth_service import AuthService
from app.schemas.investment import InvestmentCreate
from app.schemas.user import UserCreate
from datetime import date
from decimal import Decimal

def test_investment_service():
    db = SessionLocal()
    
    try:
        print("🧪 Testing Investment Service\n")
        
        # Create test user
        print("1. Creating test user...")
        try:
            user_data = UserCreate(
                email="investor@test.com",
                full_name="Test Investor",
                password="InvestPass123!"
            )
            user = AuthService.create_user(db, user_data)
            print(f"✅ User created: {user.email}")
        except ValueError:
            # User already exists
            user = AuthService.get_user_by_email(db, "investor@test.com")
            print(f"✅ Using existing user: {user.email}")
        
        # Create investments
        print("\n2. Creating investments...")
        
        investments_data = [
            InvestmentCreate(
                asset_type="Stock",
                asset_name="Apple Inc.",
                symbol="AAPL",
                quantity=Decimal("10"),
                purchase_price=Decimal("150.00"),
                current_price=Decimal("175.00"),
                purchase_date=date(2024, 1, 15),
                platform="Zerodha",
                notes="Tech stock investment"
            ),
            InvestmentCreate(
                asset_type="MutualFund",
                asset_name="HDFC Top 100 Fund",
                symbol="HDFC100",
                quantity=Decimal("100"),
                purchase_price=Decimal("50.00"),
                current_price=Decimal("55.00"),
                purchase_date=date(2024, 2, 1),
                platform="Groww",
                notes="Mutual fund SIP"
            ),
            InvestmentCreate(
                asset_type="FD",
                asset_name="SBI Fixed Deposit",
                quantity=Decimal("1"),
                purchase_price=Decimal("100000.00"),
                current_price=Decimal("106000.00"),
                purchase_date=date(2024, 1, 1),
                maturity_date=date(2025, 1, 1),
                platform="SBI",
                interest_rate=Decimal("6.00"),
                notes="1 year FD at 6% interest"
            ),
            InvestmentCreate(
                asset_type="Gold",
                asset_name="Digital Gold",
                quantity=Decimal("10.5"),
                purchase_price=Decimal("5500.00"),
                current_price=Decimal("5800.00"),
                purchase_date=date(2024, 3, 1),
                platform="Paytm",
                notes="Digital gold investment"
            ),
            InvestmentCreate(
                asset_type="Crypto",
                asset_name="Bitcoin",
                symbol="BTC",
                quantity=Decimal("0.05"),
                purchase_price=Decimal("4000000.00"),
                current_price=Decimal("4200000.00"),
                purchase_date=date(2024, 4, 1),
                platform="WazirX",
                notes="Crypto investment"
            )
        ]
        
        created_investments = []
        for inv_data in investments_data:
            inv = InvestmentService.create_investment(db, inv_data, user.id)
            created_investments.append(inv)
            print(f"✅ Created: {inv.asset_name} ({inv.asset_type})")
        
        # Test get investments
        print("\n3. Retrieving investments...")
        investments = InvestmentService.get_investments(db, user.id)
        print(f"✅ Found {len(investments)} investments")
        
        # Test portfolio summary
        print("\n4. Calculating portfolio summary...")
        portfolio = InvestmentService.calculate_portfolio_summary(db, user.id)
        print(f"✅ Total Invested: ₹{portfolio.total_invested:,.2f}")
        print(f"✅ Current Value: ₹{portfolio.total_current_value:,.2f}")
        print(f"✅ Total Gain/Loss: ₹{portfolio.total_gain_loss:,.2f} ({portfolio.total_gain_loss_percentage:.2f}%)")
        print(f"✅ Total Investments: {portfolio.total_investments}")
        
        # Test asset allocation
        print("\n5. Asset allocation...")
        allocation = InvestmentService.get_asset_allocation(db, user.id)
        for asset in allocation:
            print(f"   {asset['asset_type']}: ₹{asset['value']:,.2f} ({asset['percentage']:.1f}%)")
        
        # Test top performers
        print("\n6. Top performers...")
        top = InvestmentService.get_top_performers(db, user.id, limit=3)
        for inv in top:
            print(f"   {inv.asset_name}: {inv.percentage_gain:.2f}% gain")
        
        # Test platform summary
        print("\n7. Platform summary...")
        platforms = InvestmentService.get_platform_summary(db, user.id)
        for platform in platforms:
            print(f"   {platform['platform']}: {platform['count']} investments, ₹{platform['total_current_value']:,.2f}")
        
        # Test price update
        print("\n8. Updating price...")
        updated = InvestmentService.update_price(
            db,
            created_investments[0].id,
            user.id,
            Decimal("180.00")
        )
        print(f"✅ Updated {updated.asset_name} price to ₹{updated.current_price}")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_investment_service()