# Create file: backend/create_test_data.py

import requests
from datetime import date, timedelta
import random

# Configuration
BASE_URL = "http://localhost:8000"
EMAIL = "test@example.com"
PASSWORD = "SecurePass123!"

# Categories with typical expenses
EXPENSE_DATA = [
    # Food expenses
    {"title": "Breakfast at Café", "amount": 250, "category": "Food", "payment": "UPI"},
    {"title": "Lunch Buffet", "amount": 450, "category": "Food", "payment": "Cash"},
    {"title": "Dinner at Restaurant", "amount": 800, "category": "Food", "payment": "Credit Card"},
    {"title": "Monthly Groceries", "amount": 5000, "category": "Food", "payment": "Debit Card"},
    {"title": "Online Food Order", "amount": 350, "category": "Food", "payment": "UPI"},
    
    # Transport
    {"title": "Petrol", "amount": 2000, "category": "Transport", "payment": "Cash"},
    {"title": "Uber Ride", "amount": 180, "category": "Transport", "payment": "UPI"},
    {"title": "Metro Card Recharge", "amount": 500, "category": "Transport", "payment": "Debit Card"},
    {"title": "Auto Rickshaw", "amount": 80, "category": "Transport", "payment": "Cash"},
    
    # Entertainment
    {"title": "Movie Tickets", "amount": 600, "category": "Entertainment", "payment": "Credit Card"},
    {"title": "Netflix Subscription", "amount": 649, "category": "Entertainment", "payment": "Credit Card"},
    {"title": "Gaming", "amount": 1500, "category": "Entertainment", "payment": "UPI"},
    {"title": "Concert Tickets", "amount": 2500, "category": "Entertainment", "payment": "Debit Card"},
    
    # Shopping
    {"title": "Clothes Shopping", "amount": 3000, "category": "Shopping", "payment": "Credit Card"},
    {"title": "Electronics", "amount": 15000, "category": "Shopping", "payment": "EMI"},
    {"title": "Books", "amount": 800, "category": "Shopping", "payment": "UPI"},
    {"title": "Shoes", "amount": 2500, "category": "Shopping", "payment": "Debit Card"},
    
    # Bills
    {"title": "Electricity Bill", "amount": 1500, "category": "Bills", "payment": "Net Banking"},
    {"title": "Internet Bill", "amount": 999, "category": "Bills", "payment": "Auto Debit"},
    {"title": "Mobile Recharge", "amount": 599, "category": "Bills", "payment": "UPI"},
    {"title": "Water Bill", "amount": 300, "category": "Bills", "payment": "Cash"},
    
    # Healthcare
    {"title": "Doctor Consultation", "amount": 500, "category": "Healthcare", "payment": "Cash"},
    {"title": "Medicines", "amount": 850, "category": "Healthcare", "payment": "UPI"},
    {"title": "Gym Membership", "amount": 2000, "category": "Healthcare", "payment": "Card"},
    
    # Education
    {"title": "Online Course", "amount": 1999, "category": "Education", "payment": "Credit Card"},
    {"title": "Books & Stationery", "amount": 650, "category": "Education", "payment": "Cash"},
]

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

def create_expenses(token):
    """Create test expenses for the last 30 days"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Generate expenses for last 30 days
    today = date.today()
    created_count = 0
    
    for day_offset in range(30):
        expense_date = today - timedelta(days=day_offset)
        
        # Random 1-3 expenses per day
        num_expenses = random.randint(1, 3)
        
        for _ in range(num_expenses):
            expense_template = random.choice(EXPENSE_DATA)
            
            # Add some variation to amount
            amount_variation = random.uniform(0.8, 1.2)
            amount = round(expense_template["amount"] * amount_variation, 2)
            
            expense = {
                "title": expense_template["title"],
                "amount": amount,
                "category": expense_template["category"],
                "date": expense_date.isoformat(),
                "payment_method": expense_template["payment"],
                "notes": f"Expense on {expense_date.strftime('%B %d, %Y')}"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/expenses/",
                json=expense,
                headers=headers
            )
            
            if response.status_code == 201:
                created_count += 1
                print(f"✅ Created: {expense['title']} - ₹{expense['amount']}")
            else:
                print(f"❌ Failed: {expense['title']}")
    
    print(f"\n🎉 Successfully created {created_count} expenses!")

def main():
    print("🚀 Creating test data for WealthTrack...\n")
    
    # Login
    token = login()
    if not token:
        return
    
    # Create expenses
    print("\n📝 Creating expenses for last 30 days...\n")
    create_expenses(token)
    
    print("\n✅ Test data creation complete!")
    print(f"🌐 View at: {BASE_URL}/docs")

if __name__ == "__main__":
    main()