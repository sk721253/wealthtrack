# Create file: backend/final_test.py

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_complete_flow():
    print("\n🚀 Starting WealthTrack Complete Flow Test\n")
    
    # Test 1: Health Check
    print_section("1. HEALTH CHECK")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Health check failed"
    print("✅ Health check passed")
    
    # Test 2: Register User
    print_section("2. USER REGISTRATION")
    user_data = {
        "email": "finaltest@wealthtrack.com",
        "full_name": "Final Test User",
        "password": "FinalTest123!@#"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Registration successful")
    elif response.status_code == 400:
        print("⚠️  User already exists, continuing with login...")
    
    # Test 3: Login
    print_section("3. USER LOGIN")
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 200, "Login failed"
    token = response.json()["access_token"]
    print(f"Token received: {token[:50]}...")
    print("✅ Login successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 4: Get Current User
    print_section("4. GET CURRENT USER")
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Get current user failed"
    print("✅ User info retrieved")
    
    # Test 5: Create Multiple Expenses
    print_section("5. CREATE EXPENSES")
    expenses_to_create = [
        {
            "title": "Grocery Shopping",
            "amount": 2500.00,
            "category": "Food",
            "date": (date.today() - timedelta(days=2)).isoformat(),
            "payment_method": "Credit Card",
            "notes": "Weekly groceries"
        },
        {
            "title": "Uber Ride",
            "amount": 250.00,
            "category": "Transport",
            "date": (date.today() - timedelta(days=1)).isoformat(),
            "payment_method": "UPI",
            "notes": "Office commute"
        },
        {
            "title": "Movie Tickets",
            "amount": 600.00,
            "category": "Entertainment",
            "date": date.today().isoformat(),
            "payment_method": "Debit Card",
            "notes": "Weekend entertainment"
        }
    ]
    
    created_ids = []
    for expense in expenses_to_create:
        response = requests.post(f"{BASE_URL}/api/expenses/", json=expense, headers=headers)
        print(f"Creating: {expense['title']} - Status: {response.status_code}")
        assert response.status_code == 201, f"Failed to create {expense['title']}"
        created_ids.append(response.json()["id"])
    print(f"✅ Created {len(created_ids)} expenses")
    
    # Test 6: Get All Expenses
    print_section("6. GET ALL EXPENSES")
    response = requests.get(f"{BASE_URL}/api/expenses/", headers=headers)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total expenses: {data['total_count']}")
    print(f"Total amount: ₹{data['total_amount']}")
    print(f"Expenses in response: {len(data['expenses'])}")
    assert response.status_code == 200, "Get expenses failed"
    print("✅ Expenses retrieved")
    
    # Test 7: Get Single Expense
    print_section("7. GET SINGLE EXPENSE")
    expense_id = created_ids[0]
    response = requests.get(f"{BASE_URL}/api/expenses/{expense_id}", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200, "Get single expense failed"
    print("✅ Single expense retrieved")
    
    # Test 8: Update Expense
    print_section("8. UPDATE EXPENSE")
    update_data = {
        "amount": 2800.00,
        "notes": "Updated amount - added more items"
    }
    response = requests.put(
        f"{BASE_URL}/api/expenses/{expense_id}",
        json=update_data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print(f"Updated amount: ₹{response.json()['amount']}")
    assert response.status_code == 200, "Update expense failed"
    print("✅ Expense updated")
    
    # Test 9: Filter by Category
    print_section("9. FILTER BY CATEGORY")
    response = requests.get(
        f"{BASE_URL}/api/expenses/?category=Food",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Food expenses: {data['total_count']}")
    print(f"Food total: ₹{data['total_amount']}")
    assert response.status_code == 200, "Filter by category failed"
    print("✅ Category filter works")
    
    # Test 10: Date Range Filter
    print_section("10. FILTER BY DATE RANGE")
    start_date = (date.today() - timedelta(days=7)).isoformat()
    end_date = date.today().isoformat()
    response = requests.get(
        f"{BASE_URL}/api/expenses/?start_date={start_date}&end_date={end_date}",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Expenses in last 7 days: {data['total_count']}")
    assert response.status_code == 200, "Date filter failed"
    print("✅ Date filter works")
    
    # Test 11: Category Summary
    print_section("11. CATEGORY SUMMARY")
    response = requests.get(
        f"{BASE_URL}/api/expenses/summary/by-category",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    summary = response.json()
    print("\nCategory-wise breakdown:")
    for item in summary:
        print(f"  {item['category']}: ₹{item['total_amount']} ({item['expense_count']} expenses)")
    assert response.status_code == 200, "Category summary failed"
    print("✅ Category summary works")
    
    # Test 12: Monthly Summary
    print_section("12. MONTHLY SUMMARY")
    response = requests.get(
        f"{BASE_URL}/api/expenses/summary/by-month",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    summary = response.json()
    print("\nMonthly breakdown:")
    for item in summary:
        print(f"  {item['year']}-{item['month']:02d}: ₹{item['total_amount']} ({item['expense_count']} expenses)")
    assert response.status_code == 200, "Monthly summary failed"
    print("✅ Monthly summary works")
    
    # Test 13: Pagination
    print_section("13. PAGINATION")
    response = requests.get(
        f"{BASE_URL}/api/expenses/?skip=0&limit=2",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total expenses: {data['total_count']}")
    print(f"Returned in this page: {len(data['expenses'])}")
    assert len(data['expenses']) <= 2, "Pagination limit not working"
    print("✅ Pagination works")
    
    # Test 14: Delete Expense
    print_section("14. DELETE EXPENSE")
    expense_id = created_ids[-1]
    response = requests.delete(
        f"{BASE_URL}/api/expenses/{expense_id}",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    assert response.status_code == 204, "Delete expense failed"
    
    # Verify deletion
    response = requests.get(
        f"{BASE_URL}/api/expenses/{expense_id}",
        headers=headers
    )
    print(f"Verification status: {response.status_code}")
    assert response.status_code == 404, "Expense not deleted"
    print("✅ Expense deleted successfully")
    
    # Test 15: Unauthorized Access
    print_section("15. UNAUTHORIZED ACCESS TEST")
    response = requests.get(f"{BASE_URL}/api/expenses/")
    print(f"Status without token: {response.status_code}")
    assert response.status_code == 401, "Unauthorized access should return 401"
    print("✅ Unauthorized access blocked")
    
    # Final Summary
    print_section("FINAL SUMMARY")
    print("✅ All 15 tests passed successfully!")
    print("\n🎉 WealthTrack API is fully functional!")
    print("\n📊 Test Coverage:")
    print("  ✅ Authentication (Register, Login, Get User)")
    print("  ✅ CRUD Operations (Create, Read, Update, Delete)")
    print("  ✅ Filtering (Category, Date Range)")
    print("  ✅ Pagination")
    print("  ✅ Summaries (Category, Monthly)")
    print("  ✅ Security (Unauthorized access)")
    print("\n🚀 Ready for Week 2: Investment Tracker!")

if __name__ == "__main__":
    try:
        test_complete_flow()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")