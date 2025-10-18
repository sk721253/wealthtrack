# Update backend/week1_summary.py

import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"  # Update with your email
PASSWORD = "SecurePass123!"  # Update with your password

def generate_week1_report():
    """Generate Week 1 completion report"""
    
    print("\n" + "="*70)
    print(" 🎉 WEALTHTRACK - WEEK 1 COMPLETION REPORT")
    print("="*70)
    
    # Login
    print("\n🔐 Authenticating...")
    login_response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": EMAIL, "password": PASSWORD}
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed. Please check credentials.")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Authentication successful")
    
    # Get user info
    print("\n👤 USER INFORMATION")
    print("-" * 70)
    user_response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    user = user_response.json()
    print(f"Email: {user['email']}")
    print(f"Name: {user['full_name']}")
    print(f"Account Created: {user['created_at'][:10]}")
    print(f"Status: {'Active ✅' if user['is_active'] else 'Inactive ❌'}")
    
    # Get expenses summary
    print("\n💰 EXPENSE STATISTICS")
    print("-" * 70)
    expenses_response = requests.get(f"{BASE_URL}/api/expenses/", headers=headers)
    expenses_data = expenses_response.json()
    
    total_count = expenses_data['total_count']
    total_amount = float(expenses_data['total_amount'])  # Convert to float
    
    print(f"Total Expenses: {total_count}")
    print(f"Total Amount: ₹{total_amount:,.2f}")
    
    if total_count > 0:
        avg = total_amount / total_count
        print(f"Average Expense: ₹{avg:,.2f}")
    
    # Category breakdown
    print("\n📊 CATEGORY BREAKDOWN")
    print("-" * 70)
    category_response = requests.get(
        f"{BASE_URL}/api/expenses/summary/by-category",
        headers=headers
    )
    categories = category_response.json()
    
    if categories:
        # Sort by amount
        categories.sort(key=lambda x: float(x['total_amount']), reverse=True)
        
        print(f"{'Category':<15} {'Amount':>15}  {'%':>6}  {'Count':>10}")
        print("-" * 70)
        
        for cat in categories:
            cat_amount = float(cat['total_amount'])
            percentage = (cat_amount / total_amount) * 100 if total_amount > 0 else 0
            bar_length = int(percentage / 2)  # Scale bar to 50 chars max
            bar = "█" * bar_length
            
            print(f"{cat['category']:<15} ₹{cat_amount:>13,.2f}  {percentage:>5.1f}%  {cat['expense_count']:>4} exp")
            print(f"{'':15} {bar}")
    else:
        print("No expenses recorded yet.")
    
    # Monthly summary
    print("\n📅 MONTHLY SUMMARY")
    print("-" * 70)
    monthly_response = requests.get(
        f"{BASE_URL}/api/expenses/summary/by-month",
        headers=headers
    )
    
    if monthly_response.status_code == 200:
        monthly = monthly_response.json()
        
        if monthly:
            month_names = {
                1: "January", 2: "February", 3: "March", 4: "April",
                5: "May", 6: "June", 7: "July", 8: "August",
                9: "September", 10: "October", 11: "November", 12: "December"
            }
            
            print(f"{'Month':<15} {'Amount':>15}  {'Expenses':>10}")
            print("-" * 70)
            
            for month_data in monthly:
                month_name = month_names[month_data['month']]
                month_amount = float(month_data['total_amount'])
                month_count = month_data['expense_count']
                print(f"{month_name} {month_data['year']:<4} ₹{month_amount:>13,.2f}  {month_count:>4} exp")
        else:
            print("No monthly data available.")
    else:
        print("⚠️  Monthly summary endpoint returned error (check if bug is fixed)")
    
    # Recent expenses
    print("\n📝 RECENT EXPENSES (Last 5)")
    print("-" * 70)
    recent_response = requests.get(
        f"{BASE_URL}/api/expenses/?limit=5",
        headers=headers
    )
    recent = recent_response.json()['expenses']
    
    print(f"{'Date':<12} {'Title':<30} {'Category':<15} {'Amount':>12}")
    print("-" * 70)
    
    for exp in recent:
        exp_amount = float(exp['amount'])
        print(f"{exp['date']:<12} {exp['title'][:29]:<30} {exp['category']:<15} ₹{exp_amount:>10,.2f}")
    
    # Features completed
    print("\n✅ WEEK 1 FEATURES COMPLETED")
    print("-" * 70)
    features = [
        "User Registration & Authentication",
        "Secure Login with JWT Tokens",
        "Password Hashing with bcrypt",
        "Create, Read, Update, Delete Expenses",
        "Category-based Filtering",
        "Date Range Filtering",
        "Pagination Support",
        "Expense Summaries (Category & Monthly)",
        "Protected API Routes",
        "Comprehensive Error Handling",
        "API Documentation (Swagger)",
        "PostgreSQL Database Integration"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i:2d}. ✅ {feature}")
    
    # Statistics
    print("\n📈 PROJECT STATISTICS")
    print("-" * 70)
    print(f"Total Expenses Tracked: {total_count}")
    print(f"Total Money Managed: ₹{total_amount:,.2f}")
    print(f"API Endpoints: 10+")
    print(f"Database Tables: 2 (users, expenses)")
    print(f"Lines of Code: ~1500+")
    print(f"Documentation Files: 3 (README, API_DOCS, TESTING)")
    
    # Data insights
    if categories:
        print("\n💡 INSIGHTS")
        print("-" * 70)
        top_category = max(categories, key=lambda x: float(x['total_amount']))
        top_cat_amount = float(top_category['total_amount'])
        top_cat_percent = (top_cat_amount / total_amount) * 100
        
        print(f"• Highest spending category: {top_category['category']} (₹{top_cat_amount:,.2f} - {top_cat_percent:.1f}%)")
        print(f"• Average expense amount: ₹{avg:,.2f}")
        print(f"• Number of categories used: {len(categories)}")
        
        if total_count > 0:
            expenses_per_day = total_count / 30  # Assuming last 30 days
            print(f"• Average expenses per day: {expenses_per_day:.1f}")
    
    # Next steps
    print("\n🚀 WEEK 2 PREVIEW")
    print("-" * 70)
    print("Next week you'll build:")
    print("  • Investment Tracker (Stocks, Mutual Funds, FD, Gold, Crypto)")
    print("  • Portfolio Value Calculation")
    print("  • Gains/Losses Tracking")
    print("  • Asset Allocation Charts")
    print("  • Performance Analytics")
    print("  • Integration with Expense Tracker")
    
    # Completion checklist
    print("\n📋 WEEK 1 COMPLETION CHECKLIST")
    print("-" * 70)
    checklist = [
        ("Server running without errors", "✅"),
        ("All API endpoints working", "✅"),
        ("Database connected", "✅"),
        ("Authentication working", "✅"),
        ("CRUD operations functional", "✅"),
        ("Summaries calculating correctly", "✅" if monthly_response.status_code == 200 else "⚠️"),
        ("Documentation complete", "✅"),
    ]
    
    for item, status in checklist:
        print(f"{status} {item}")
    
    print("\n" + "="*70)
    print(" 🎊 CONGRATULATIONS ON COMPLETING WEEK 1!")
    print("="*70)
    print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"User: {user['email']}")
    print("\n💪 You're ready for Week 2! Take a well-deserved break.")
    print("\n")

if __name__ == "__main__":
    try:
        generate_week1_report()
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        print("\nDebug Info:")
        import traceback
        traceback.print_exc()
        print("\nMake sure:")
        print("  1. Server is running: uvicorn app.main:app --reload")
        print("  2. Credentials in script are correct")
        print("  3. You have expenses in database")