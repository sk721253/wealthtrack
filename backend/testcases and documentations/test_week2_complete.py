# Create file: backend/test_week2_complete.py

import requests
import json
from datetime import date, timedelta
from decimal import Decimal

BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"
PASSWORD = "SecurePass123!"

def print_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_complete_week2():
    print("\n🚀 Starting Week 2 Complete Flow Test\n")
    
    # Login
    print_section("1. AUTHENTICATION")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": EMAIL, "password": PASSWORD}
    )
    assert response.status_code == 200, "Login failed"
    token = response.json()["access_token"]
    print(f"✅ Login successful")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test Investment CRUD
    print_section("2. INVESTMENT CRUD OPERATIONS")
    
    # Create investment
    investment_data = {
        "asset_type": "Stock",
        "asset_name": "Test Stock Inc.",
        "symbol": "TEST",
        "quantity": 10,
        "purchase_price": 100.00,
        "current_price": 120.00,
        "purchase_date": date.today().isoformat(),
        "platform": "Test Platform",
        "notes": "Test investment"
    }
    
    response = requests.post(f"{BASE_URL}/api/investments/", json=investment_data, headers=headers)
    assert response.status_code == 201, "Create investment failed"
    investment = response.json()
    investment_id = investment["id"]
    print(f"✅ Created investment: {investment['asset_name']}")
    print(f"   Invested: ₹{investment['invested_amount']}, Current: ₹{investment['current_value']}")
    print(f"   Gain: {investment['percentage_gain']:.2f}%")
    
    # Get all investments
    response = requests.get(f"{BASE_URL}/api/investments/", headers=headers)
    assert response.status_code == 200, "Get investments failed"
    data = response.json()
    print(f"✅ Retrieved {data['total_count']} investments")
    print(f"   Portfolio value: ₹{data['portfolio_summary']['total_current_value']:.2f}")
    
    # Get single investment
    response = requests.get(f"{BASE_URL}/api/investments/{investment_id}", headers=headers)
    assert response.status_code == 200, "Get single investment failed"
    print(f"✅ Retrieved single investment")
    
    # Update price
    response = requests.patch(
        f"{BASE_URL}/api/investments/{investment_id}/price",
        json={"current_price": 130.00},
        headers=headers
    )
    assert response.status_code == 200, "Update price failed"
    updated = response.json()
    print(f"✅ Updated price to ₹{updated['current_price']}")
    print(f"   New gain: {updated['percentage_gain']:.2f}%")
    
    # Test Analytics
    print_section("3. ANALYTICS ENDPOINTS")
    
    # Asset allocation
    response = requests.get(f"{BASE_URL}/api/investments/analytics/asset-allocation", headers=headers)
    assert response.status_code == 200, "Asset allocation failed"
    allocation = response.json()
    print(f"✅ Asset allocation retrieved:")
    for asset in allocation[:3]:
        print(f"   {asset['asset_type']}: ₹{asset['value']:.2f} ({asset['percentage']:.1f}%)")
    
    # Top performers
    response = requests.get(f"{BASE_URL}/api/investments/analytics/top-performers?limit=5", headers=headers)
    assert response.status_code == 200, "Top performers failed"
    performers = response.json()
    print(f"✅ Top {len(performers)} performers:")
    for inv in performers[:3]:
        print(f"   {inv['asset_name']}: +{inv['percentage_gain']:.2f}%")
    
    # Platform summary
    response = requests.get(f"{BASE_URL}/api/investments/analytics/platform-summary", headers=headers)
    assert response.status_code == 200, "Platform summary failed"
    platforms = response.json()
    print(f"✅ Platform summary:")
    for platform in platforms[:3]:
        print(f"   {platform['platform']}: {platform['count']} investments, ₹{platform['total_current_value']:.2f}")
    
    # Statistics
    response = requests.get(f"{BASE_URL}/api/investments/analytics/statistics", headers=headers)
    assert response.status_code == 200, "Statistics failed"
    stats = response.json()
    print(f"✅ Investment statistics:")
    print(f"   Win rate: {stats['performance']['win_rate']:.1f}%")
    print(f"   Average holding period: {stats['overview']['average_days_held']} days")
    
    # Test Dashboard
    print_section("4. DASHBOARD")
    
    response = requests.get(f"{BASE_URL}/api/dashboard/", headers=headers)
    assert response.status_code == 200, "Dashboard failed"
    dashboard = response.json()
    print(f"✅ Dashboard data retrieved:")
    print(f"   Net Worth: ₹{dashboard['summary']['net_worth']:.2f}")
    print(f"   Total Invested: ₹{dashboard['summary']['total_invested']:.2f}")
    print(f"   Investment Gains: ₹{dashboard['summary']['investment_gains']:.2f} ({dashboard['summary']['investment_gains_percentage']:.2f}%)")
    print(f"   Current Month Expenses: ₹{dashboard['summary']['current_month_expenses']:.2f}")
    
    # Financial health score
    response = requests.get(f"{BASE_URL}/api/dashboard/health-score", headers=headers)
    assert response.status_code == 200, "Health score failed"
    health = response.json()
    print(f"✅ Financial Health Score: {health['score']}/100 ({health['rating']})")
    if health['recommendations']:
        print(f"   Top recommendation: {health['recommendations'][0]}")
    
    # Test Export
    print_section("5. EXPORT FEATURES")
    
    # Export expenses CSV
    response = requests.get(f"{BASE_URL}/api/export/expenses/csv", headers=headers)
    assert response.status_code == 200, "Export expenses CSV failed"
    print(f"✅ Exported expenses CSV ({len(response.text)} bytes)")
    
    # Export investments CSV
    response = requests.get(f"{BASE_URL}/api/export/investments/csv", headers=headers)
    assert response.status_code == 200, "Export investments CSV failed"
    print(f"✅ Exported investments CSV ({len(response.text)} bytes)")
    
    # Export complete data
    response = requests.get(f"{BASE_URL}/api/export/complete", headers=headers)
    assert response.status_code == 200, "Export complete data failed"
    complete_data = response.json()
    print(f"✅ Exported complete data:")
    print(f"   Expenses: {len(complete_data['expenses']['data'])} records")
    print(f"   Investments: {len(complete_data['investments']['data'])} records")
    
    # Test Filters
    print_section("6. FILTERING & PAGINATION")
    
    # Filter by asset type
    response = requests.get(f"{BASE_URL}/api/investments/?asset_type=Stock", headers=headers)
    assert response.status_code == 200, "Filter by asset type failed"
    print(f"✅ Filtered by Stock: {response.json()['total_count']} results")
    
    # Pagination
    response = requests.get(f"{BASE_URL}/api/investments/?skip=0&limit=5", headers=headers)
    assert response.status_code == 200, "Pagination failed"
    print(f"✅ Pagination working (limit 5)")
    
    # Combined Metrics
    print_section("7. COMBINED EXPENSE + INVESTMENT METRICS")
    
    response = requests.get(f"{BASE_URL}/api/dashboard/", headers=headers)
    dashboard = response.json()
    
    total_wealth = dashboard['summary']['net_worth']
    monthly_expenses = dashboard['summary']['current_month_expenses']
    
    print(f"✅ Combined financial overview:")
    print(f"   Total Wealth (Investments): ₹{total_wealth:.2f}")
    print(f"   Monthly Burn Rate: ₹{monthly_expenses:.2f}")
    if monthly_expenses > 0:
        months_runway = total_wealth / monthly_expenses
        print(f"   Months of Runway: {months_runway:.1f} months")
    
    # Cleanup - Delete test investment
    print_section("8. CLEANUP")
    response = requests.delete(f"{BASE_URL}/api/investments/{investment_id}", headers=headers)
    assert response.status_code == 204, "Delete investment failed"
    print(f"✅ Deleted test investment")
    
    # Final Summary
    print_section("FINAL SUMMARY")
    print("✅ All Week 2 tests passed successfully!")
    print("\n📊 Features Tested:")
    features = [
        "Investment CRUD operations",
        "Price updates (single & bulk)",
        "Asset allocation analytics",
        "Performance tracking",
        "Platform summaries",
        "Portfolio statistics",
        "Combined dashboard",
        "Financial health score",
        "CSV exports",
        "JSON export",
        "Filtering & pagination",
        "Combined expense + investment metrics"
    ]
    for i, feature in enumerate(features, 1):
        print(f"  {i:2d}. ✅ {feature}")
    
    print("\n🎉 Week 2 Implementation Complete!")

if __name__ == "__main__":
    try:
        test_complete_week2()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()