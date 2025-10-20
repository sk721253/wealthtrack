# Continue backend/create_investment_test_data.py


import requests
from datetime import date, timedelta
import random
from decimal import Decimal


# Continue backend/create_investment_test_data.py

BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"  # Use your test user email
PASSWORD = "SecurePass123!"  # Use your password

# Investment templates with realistic data
INVESTMENT_TEMPLATES = {
    "Stock": [
        {"name": "Reliance Industries", "symbol": "RELIANCE", "price_range": (2400, 2650), "platform": "Zerodha"},
        {"name": "TCS", "symbol": "TCS", "price_range": (3500, 3800), "platform": "Zerodha"},
        {"name": "HDFC Bank", "symbol": "HDFCBANK", "price_range": (1600, 1750), "platform": "Groww"},
        {"name": "Infosys", "symbol": "INFY", "price_range": (1400, 1550), "platform": "Upstox"},
        {"name": "ITC", "symbol": "ITC", "price_range": (420, 450), "platform": "Zerodha"},
        {"name": "ICICI Bank", "symbol": "ICICIBANK", "price_range": (1000, 1100), "platform": "Groww"},
    ],
    "MutualFund": [
        {"name": "HDFC Top 100 Fund", "symbol": "HDFC100", "price_range": (600, 680), "platform": "Groww"},
        {"name": "SBI Bluechip Fund", "symbol": "SBIBLUECHIP", "price_range": (75, 82), "platform": "Kuvera"},
        {"name": "ICICI Prudential Technology Fund", "symbol": "ICICITECH", "price_range": (150, 165), "platform": "Groww"},
        {"name": "Axis Midcap Fund", "symbol": "AXISMIDCAP", "price_range": (85, 92), "platform": "Paytm Money"},
        {"name": "Mirae Asset Large Cap Fund", "symbol": "MIRAELARGE", "price_range": (95, 105), "platform": "Groww"},
    ],
    "FD": [
        {"name": "SBI Fixed Deposit", "amount": 100000, "interest": 6.5, "platform": "SBI"},
        {"name": "HDFC Fixed Deposit", "amount": 50000, "interest": 6.75, "platform": "HDFC Bank"},
        {"name": "ICICI Bank FD", "amount": 200000, "interest": 7.0, "platform": "ICICI Bank"},
        {"name": "Axis Bank FD", "amount": 75000, "interest": 6.8, "platform": "Axis Bank"},
    ],
    "Gold": [
        {"name": "Digital Gold", "price_range": (5500, 5900), "platform": "Paytm"},
        {"name": "Gold ETF", "price_range": (5400, 5850), "platform": "Zerodha"},
        {"name": "Sovereign Gold Bond", "price_range": (5200, 5700), "platform": "NSE"},
    ],
    "Crypto": [
        {"name": "Bitcoin", "symbol": "BTC", "price_range": (4000000, 4500000), "platform": "WazirX"},
        {"name": "Ethereum", "symbol": "ETH", "price_range": (250000, 280000), "platform": "CoinDCX"},
        {"name": "Ripple", "symbol": "XRP", "price_range": (50, 65), "platform": "WazirX"},
    ]
}

def login():
    """Login and get access token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": EMAIL, "password": PASSWORD}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful")
        return token
    else:
        print("❌ Login failed:", response.json())
        return None

def create_investments(token):
    """Create diverse investment portfolio"""
    headers = {"Authorization": f"Bearer {token}"}
    created_count = 0
    
    print("\n📊 Creating Investment Portfolio...\n")
    
    # Create Stocks
    print("📈 Creating Stock Investments...")
    for stock in INVESTMENT_TEMPLATES["Stock"][:4]:  # Create 4 stocks
        price_low, price_high = stock["price_range"]
        purchase_price = random.uniform(price_low, price_high * 0.9)
        current_price = random.uniform(purchase_price * 0.95, price_high)
        quantity = random.randint(5, 50)
        days_ago = random.randint(30, 365)
        
        investment = {
            "asset_type": "Stock",
            "asset_name": stock["name"],
            "symbol": stock["symbol"],
            "quantity": quantity,
            "purchase_price": round(purchase_price, 2),
            "current_price": round(current_price, 2),
            "purchase_date": (date.today() - timedelta(days=days_ago)).isoformat(),
            "platform": stock["platform"],
            "notes": f"Purchased {quantity} shares"
        }
        
        response = requests.post(f"{BASE_URL}/api/investments/", json=investment, headers=headers)
        if response.status_code == 201:
            created_count += 1
            inv_data = response.json()
            print(f"  ✅ {stock['name']}: {quantity} shares @ ₹{purchase_price:.2f} → ₹{current_price:.2f} "
                  f"(Gain: {inv_data['percentage_gain']:.2f}%)")
    
    # Create Mutual Funds
    print("\n💼 Creating Mutual Fund Investments...")
    for mf in INVESTMENT_TEMPLATES["MutualFund"][:3]:  # Create 3 MFs
        price_low, price_high = mf["price_range"]
        purchase_price = random.uniform(price_low, price_high * 0.95)
        current_price = random.uniform(purchase_price * 1.0, price_high)
        quantity = random.randint(50, 500)
        days_ago = random.randint(60, 730)
        
        investment = {
            "asset_type": "MutualFund",
            "asset_name": mf["name"],
            "symbol": mf["symbol"],
            "quantity": quantity,
            "purchase_price": round(purchase_price, 2),
            "current_price": round(current_price, 2),
            "purchase_date": (date.today() - timedelta(days=days_ago)).isoformat(),
            "platform": mf["platform"],
            "notes": f"SIP investment - {quantity} units"
        }
        
        response = requests.post(f"{BASE_URL}/api/investments/", json=investment, headers=headers)
        if response.status_code == 201:
            created_count += 1
            inv_data = response.json()
            print(f"  ✅ {mf['name']}: {quantity} units @ ₹{purchase_price:.2f} → ₹{current_price:.2f} "
                  f"(Gain: {inv_data['percentage_gain']:.2f}%)")
    
    # Create Fixed Deposits
    print("\n🏦 Creating Fixed Deposit Investments...")
    for fd in INVESTMENT_TEMPLATES["FD"][:2]:  # Create 2 FDs
        amount = fd["amount"]
        interest_rate = fd["interest"]
        days_ago = random.randint(30, 180)
        maturity_days = 365  # 1 year FD
        
        # Calculate current value with interest
        days_elapsed = days_ago
        current_value = amount * (1 + (interest_rate / 100) * (days_elapsed / 365))
        
        purchase_date = date.today() - timedelta(days=days_ago)
        maturity_date = purchase_date + timedelta(days=maturity_days)
        
        investment = {
            "asset_type": "FD",
            "asset_name": fd["name"],
            "quantity": 1,
            "purchase_price": amount,
            "current_price": round(current_value, 2),
            "purchase_date": purchase_date.isoformat(),
            "maturity_date": maturity_date.isoformat(),
            "platform": fd["platform"],
            "interest_rate": interest_rate,
            "notes": f"1 year FD @ {interest_rate}% interest"
        }
        
        response = requests.post(f"{BASE_URL}/api/investments/", json=investment, headers=headers)
        if response.status_code == 201:
            created_count += 1
            inv_data = response.json()
            days_to_mature = (maturity_date - date.today()).days
            print(f"  ✅ {fd['name']}: ₹{amount:,.2f} @ {interest_rate}% "
                  f"(Current: ₹{current_value:,.2f}, Matures in {days_to_mature} days)")
    
    # Create Gold Investments
    print("\n🥇 Creating Gold Investments...")
    for gold in INVESTMENT_TEMPLATES["Gold"][:2]:  # Create 2 gold investments
        price_low, price_high = gold["price_range"]
        purchase_price = random.uniform(price_low, price_high * 0.95)
        current_price = random.uniform(price_low, price_high)
        quantity = round(random.uniform(5, 25), 2)
        days_ago = random.randint(90, 365)
        
        investment = {
            "asset_type": "Gold",
            "asset_name": gold["name"],
            "quantity": quantity,
            "purchase_price": round(purchase_price, 2),
            "current_price": round(current_price, 2),
            "purchase_date": (date.today() - timedelta(days=days_ago)).isoformat(),
            "platform": gold["platform"],
            "notes": f"{quantity}g gold investment"
        }
        
        response = requests.post(f"{BASE_URL}/api/investments/", json=investment, headers=headers)
        if response.status_code == 201:
            created_count += 1
            inv_data = response.json()
            print(f"  ✅ {gold['name']}: {quantity}g @ ₹{purchase_price:.2f}/g → ₹{current_price:.2f}/g "
                  f"(Gain: {inv_data['percentage_gain']:.2f}%)")
    
    # Create Crypto Investments
    print("\n₿ Creating Cryptocurrency Investments...")
    for crypto in INVESTMENT_TEMPLATES["Crypto"][:2]:  # Create 2 crypto investments
        price_low, price_high = crypto["price_range"]
        purchase_price = random.uniform(price_low, price_high * 0.9)
        current_price = random.uniform(price_low * 0.95, price_high)
        quantity = round(random.uniform(0.01, 0.1), 8)  # Small crypto amounts
        days_ago = random.randint(30, 180)
        
        investment = {
            "asset_type": "Crypto",
            "asset_name": crypto["name"],
            "symbol": crypto["symbol"],
            "quantity": quantity,
            "purchase_price": round(purchase_price, 2),
            "current_price": round(current_price, 2),
            "purchase_date": (date.today() - timedelta(days=days_ago)).isoformat(),
            "platform": crypto["platform"],
            "notes": f"{quantity} {crypto['symbol']} investment"
        }
        
        response = requests.post(f"{BASE_URL}/api/investments/", json=investment, headers=headers)
        if response.status_code == 201:
            created_count += 1
            inv_data = response.json()
            print(f"  ✅ {crypto['name']}: {quantity} {crypto['symbol']} @ ₹{purchase_price:,.2f} → ₹{current_price:,.2f} "
                  f"(Gain: {inv_data['percentage_gain']:.2f}%)")
    
    return created_count

def display_portfolio_summary(token):
    """Display portfolio summary"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n" + "="*70)
    print(" 📊 PORTFOLIO SUMMARY")
    print("="*70)
    
    # Get portfolio data
    response = requests.get(f"{BASE_URL}/api/investments/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        summary = data["portfolio_summary"]
        
        print(f"\n💰 Overall Portfolio:")
        print(f"  Total Invested:    ₹{summary['total_invested']:,.2f}")
        print(f"  Current Value:     ₹{summary['total_current_value']:,.2f}")
        print(f"  Gain/Loss:         ₹{summary['total_gain_loss']:,.2f} "
              f"({summary['total_gain_loss_percentage']:.2f}%)")
        print(f"  Total Investments: {summary['total_investments']}")
        
        print(f"\n📊 Asset Allocation:")
        for asset in summary["asset_type_breakdown"]:
            print(f"  {asset['asset_type']:<15} ₹{asset['current_value']:>12,.2f}  "
                  f"({asset['percentage_of_portfolio']:>5.1f}%)  "
                  f"{asset['count']} investments")
    
    # Get top performers
    response = requests.get(f"{BASE_URL}/api/investments/analytics/top-performers?limit=3", headers=headers)
    if response.status_code == 200:
        performers = response.json()
        if performers:
            print(f"\n🏆 Top Performers:")
            for inv in performers:
                print(f"  {inv['asset_name']:<30} +{inv['percentage_gain']:.2f}%")
    
    # Get platform summary
    response = requests.get(f"{BASE_URL}/api/investments/analytics/platform-summary", headers=headers)
    if response.status_code == 200:
        platforms = response.json()
        if platforms:
            print(f"\n🏢 Platform-wise Summary:")
            for platform in platforms:
                print(f"  {platform['platform']:<20} ₹{platform['total_current_value']:>12,.2f}  "
                      f"({platform['gain_loss_percentage']:>+6.2f}%)")

def main():
    print("🚀 Creating Investment Test Data for WealthTrack...\n")
    
    # Login
    token = login()
    if not token:
        return
    
    # Create investments
    created_count = create_investments(token)
    
    print(f"\n✅ Successfully created {created_count} investments!")
    
    # Display summary
    display_portfolio_summary(token)
    
    print("\n" + "="*70)
    print(" 🎉 Investment Portfolio Created Successfully!")
    print("="*70)
    print(f"\n🌐 View your portfolio at: {BASE_URL}/docs")
    print("\n📝 Next Steps:")
    print("  1. Check GET /api/investments/ to see all investments")
    print("  2. Try GET /api/investments/analytics/asset-allocation")
    print("  3. Update prices with PATCH /api/investments/{id}/price")
    print("  4. Check GET /api/investments/analytics/top-performers")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()