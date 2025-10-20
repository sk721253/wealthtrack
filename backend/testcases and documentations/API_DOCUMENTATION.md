# Create file: backend/API_DOCUMENTATION.md

# 🔌 WealthTrack API Documentation

Complete API reference for WealthTrack backend.

## Base URL

```
http://localhost:8000
```

## Authentication

All protected endpoints require JWT token in header:

```
Authorization: Bearer <your_access_token>
```

---

## 🔐 Authentication Endpoints

### 1. Register User

**POST** `/api/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "SecurePass123!"
}
```

**Response (201 Created):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-01-13T10:00:00Z"
}
```

**Validation Rules:**

- Email must be valid format
- Password minimum 8 characters
- Full name minimum 1 character

**Error Responses:**

- `400 Bad Request` - Email already registered
- `422 Unprocessable Entity` - Validation error

---

### 2. Login

**POST** `/api/auth/login`

Login and receive access token.

**Request Body (Form Data):**

```
username: user@example.com
password: SecurePass123!
```

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- `401 Unauthorized` - Invalid credentials

**Note:** Token expires in 30 minutes (default)

---

### 3. Get Current User

**GET** `/api/auth/me`

Get authenticated user information.

**Headers:**

```
Authorization: Bearer <token>
```

**Response (200 OK):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-01-13T10:00:00Z"
}
```

**Error Responses:**

- `401 Unauthorized` - Invalid or expired token

---

## 💰 Expense Endpoints

### 1. Create Expense

**POST** `/api/expenses/`

Create a new expense.

**Headers:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "title": "Weekly Groceries",
  "amount": 2500.5,
  "category": "Food",
  "date": "2025-01-15",
  "payment_method": "Credit Card",
  "notes": "Bought from Big Bazaar"
}
```

**Response (201 Created):**

```json
{
  "id": "789e4567-e89b-12d3-a456-426614174000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Weekly Groceries",
  "amount": 2500.5,
  "category": "Food",
  "date": "2025-01-15",
  "payment_method": "Credit Card",
  "notes": "Bought from Big Bazaar",
  "created_at": "2025-01-13T10:30:00Z",
  "updated_at": null
}
```

**Validation Rules:**

- Title: 1-200 characters
- Amount: Must be > 0, max 2 decimal places
- Category: 1-50 characters
- Date: Valid date format (YYYY-MM-DD)
- Payment method: Optional, max 50 characters
- Notes: Optional, max 500 characters

---

### 2. Get All Expenses

**GET** `/api/expenses/`

Get list of user's expenses with filters.

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skip | integer | No | Number of records to skip (default: 0) |
| limit | integer | No | Max records to return (default: 100, max: 500) |
| category | string | No | Filter by category |
| start_date | date | No | Filter from date (YYYY-MM-DD) |
| end_date | date | No | Filter to date (YYYY-MM-DD) |

**Example Request:**

```
GET /api/expenses/?category=Food&start_date=2025-01-01&limit=10
```

**Response (200 OK):**

```json
{
  "expenses": [
    {
      "id": "789e4567-e89b-12d3-a456-426614174000",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Weekly Groceries",
      "amount": 2500.5,
      "category": "Food",
      "date": "2025-01-15",
      "payment_method": "Credit Card",
      "notes": "Bought from Big Bazaar",
      "created_at": "2025-01-13T10:30:00Z",
      "updated_at": null
    }
  ],
  "total_count": 45,
  "total_amount": 125000.5
}
```

---

### 3. Get Single Expense

**GET** `/api/expenses/{expense_id}`

Get details of a specific expense.

**Headers:**

```
Authorization: Bearer <token>
```

**Path Parameters:**

- `expense_id` (UUID): Expense ID

**Response (200 OK):**

```json
{
  "id": "789e4567-e89b-12d3-a456-426614174000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Weekly Groceries",
  "amount": 2500.5,
  "category": "Food",
  "date": "2025-01-15",
  "payment_method": "Credit Card",
  "notes": "Bought from Big Bazaar",
  "created_at": "2025-01-13T10:30:00Z",
  "updated_at": null
}
```

**Error Responses:**

- `404 Not Found` - Expense doesn't exist or doesn't belong to user

---

### 4. Update Expense

**PUT** `/api/expenses/{expense_id}`

Update an existing expense.

**Headers:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body (all fields optional):**

```json
{
  "title": "Updated Title",
  "amount": 2800.0,
  "category": "Food",
  "notes": "Updated notes"
}
```

**Response (200 OK):**

```json
{
  "id": "789e4567-e89b-12d3-a456-426614174000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Title",
  "amount": 2800.0,
  "category": "Food",
  "date": "2025-01-15",
  "payment_method": "Credit Card",
  "notes": "Updated notes",
  "created_at": "2025-01-13T10:30:00Z",
  "updated_at": "2025-01-13T11:00:00Z"
}
```

**Error Responses:**

- `404 Not Found` - Expense doesn't exist

---

### 5. Delete Expense

**DELETE** `/api/expenses/{expense_id}`

Delete an expense.

**Headers:**

```
Authorization: Bearer <token>
```

**Response (204 No Content)**

No response body.

**Error Responses:**

- `404 Not Found` - Expense doesn't exist

---

### 6. Get Category Summary

**GET** `/api/expenses/summary/by-category`

Get spending summary grouped by category.

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | date | No | Filter from date |
| end_date | date | No | Filter to date |

**Response (200 OK):**

```json
[
  {
    "category": "Food",
    "total_amount": 25000.5,
    "expense_count": 45
  },
  {
    "category": "Transport",
    "total_amount": 8500.0,
    "expense_count": 23
  },
  {
    "category": "Entertainment",
    "total_amount": 5200.0,
    "expense_count": 12
  }
]
```

---

### 7. Get Monthly Summary

**GET** `/api/expenses/summary/by-month`

Get monthly spending summary.

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| year | integer | No | Filter by year (e.g., 2025) |

**Response (200 OK):**

```json
[
  {
    "year": 2025,
    "month": 1,
    "total_amount": 45000.5,
    "expense_count": 67
  },
  {
    "year": 2024,
    "month": 12,
    "total_amount": 38000.0,
    "expense_count": 54
  }
]
```

---

## 📊 Common Response Codes

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | OK - Request successful                 |
| 201  | Created - Resource created successfully |
| 204  | No Content - Successful deletion        |
| 400  | Bad Request - Invalid request data      |
| 401  | Unauthorized - Missing or invalid token |
| 403  | Forbidden - Insufficient permissions    |
| 404  | Not Found - Resource doesn't exist      |
| 422  | Unprocessable Entity - Validation error |
| 500  | Internal Server Error - Server error    |

---

## 🔍 Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message here"
}
```

For validation errors (422):

```json
{
  "detail": "Validation error",
  "errors": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 💡 Best Practices

1. **Always include Authorization header** for protected endpoints
2. **Handle token expiration** - Implement token refresh logic
3. **Validate input** on client-side before sending
4. **Use pagination** for large datasets
5. **Check response codes** before processing data
6. **Store tokens securely** - Never in localStorage for production

---

## 🧪 Testing with cURL

### Complete Flow Example

```bash
# 1. Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","full_name":"Test User","password":"Pass123!@#"}'

# 2. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Pass123!@#" \
  | jq -r '.access_token')

# 3. Create Expense
curl -X POST "http://localhost:8000/api/expenses/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Lunch","amount":250,"category":"Food","date":"2025-01-15"}'

# 4. Get Expenses
curl "http://localhost:8000/api/expenses/" \
  -H "Authorization: Bearer $TOKEN"

# 5. Get Summary
curl "http://localhost:8000/api/expenses/summary/by-category" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📚 Additional Resources

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

_Last Updated: January 13, 2025_

# Create file: backend/INVESTMENT_API_DOCS.md

# 📈 Investment Tracker API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints require JWT token:

```
Authorization: Bearer <your_access_token>
```

---

## Investment Endpoints

### 1. Create Investment

**POST** `/api/investments/`

Create a new investment.

**Request Body:**

```json
{
  "asset_type": "Stock",
  "asset_name": "Reliance Industries",
  "symbol": "RELIANCE",
  "quantity": 20,
  "purchase_price": 2400.0,
  "current_price": 2650.0,
  "purchase_date": "2024-06-15",
  "maturity_date": null,
  "platform": "Zerodha",
  "interest_rate": null,
  "notes": "Long term investment"
}
```

**Asset Types:**

- Stock
- MutualFund
- FD
- Gold
- Crypto
- Bond
- Other

**Response (201 Created):**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user-uuid",
  "asset_type": "Stock",
  "asset_name": "Reliance Industries",
  "symbol": "RELIANCE",
  "quantity": 20,
  "purchase_price": 2400.0,
  "current_price": 2650.0,
  "purchase_date": "2024-06-15",
  "platform": "Zerodha",
  "notes": "Long term investment",
  "invested_amount": 48000.0,
  "current_value": 53000.0,
  "absolute_gain": 5000.0,
  "percentage_gain": 10.42,
  "days_held": 120,
  "is_matured": false,
  "created_at": "2024-10-16T10:00:00Z"
}
```

---

### 2. Get All Investments

**GET** `/api/investments/`

Get list of investments with portfolio summary.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| skip | integer | Records to skip (default: 0) |
| limit | integer | Max records (default: 100) |
| asset_type | string | Filter by asset type |
| platform | string | Filter by platform |

**Response (200 OK):**

```json
{
  "investments": [...],
  "total_count": 15,
  "portfolio_summary": {
    "total_invested": 500000.00,
    "total_current_value": 575000.00,
    "total_gain_loss": 75000.00,
    "total_gain_loss_percentage": 15.00,
    "total_investments": 15,
    "asset_type_breakdown": [...]
  }
}
```

---

### 3. Update Investment Price

**PATCH** `/api/investments/{investment_id}/price`

Quick update of current price.

**Request Body:**

```json
{
  "current_price": 2750.0
}
```

---

### 4. Bulk Update Prices

**POST** `/api/investments/bulk-update-prices`

Update multiple investment prices at once.

**Request Body:**

```json
{
  "updates": [
    { "id": "uuid-1", "current_price": 2750.0 },
    { "id": "uuid-2", "current_price": 180.5 }
  ]
}
```

---

## Analytics Endpoints

### 1. Asset Allocation

**GET** `/api/investments/analytics/asset-allocation`

Get portfolio distribution by asset type.

**Response:**

```json
[
  {
    "asset_type": "Stock",
    "value": 300000.0,
    "percentage": 52.17
  },
  {
    "asset_type": "MutualFund",
    "value": 150000.0,
    "percentage": 26.09
  }
]
```

---

### 2. Top Performers

**GET** `/api/investments/analytics/top-performers?limit=5`

Get best performing investments.

---

### 3. Platform Summary

**GET** `/api/investments/analytics/platform-summary`

Get investment summary grouped by platform.

---

### 4. Investment Statistics

**GET** `/api/investments/analytics/statistics`

Get detailed statistics including win rate, best/worst performers, etc.

---

## Dashboard Endpoints

### 1. Complete Dashboard

**GET** `/api/dashboard/`

Get combined view of expenses and investments.

**Response:**

```json
{
  "summary": {
    "net_worth": 575000.00,
    "total_invested": 500000.00,
    "investment_gains": 75000.00,
    "investment_gains_percentage": 15.00,
    "current_month_expenses": 25000.00,
    "total_investments": 15
  },
  "expenses": {...},
  "investments": {...},
  "month_overview": {...}
}
```

---

### 2. Financial Health Score

**GET** `/api/dashboard/health-score`

Get financial health assessment with recommendations.

**Response:**

```json
{
  "score": 75,
  "rating": "Good",
  "color": "blue",
  "issues": ["Low investment diversity"],
  "recommendations": ["Consider diversifying across more asset types"]
}
```

---

## Export Endpoints

### 1. Export Expenses CSV

**GET** `/api/export/expenses/csv`

Download expenses as CSV file.

---

### 2. Export Investments CSV

**GET** `/api/export/investments/csv`

Download investments as CSV file.

---

### 3. Export Complete Data

**GET** `/api/export/complete`

Export all financial data as JSON.

---

## Example Workflows

### Workflow 1: Track New Stock Purchase

```bash
# 1. Buy stock
curl -X POST "http://localhost:8000/api/investments/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_type": "Stock",
    "asset_name": "TCS",
    "symbol": "TCS",
    "quantity": 10,
    "purchase_price": 3500.00,
    "current_price": 3500.00,
    "purchase_date": "2024-10-16",
    "platform": "Zerodha"
  }'

# 2. Update price daily
curl -X PATCH "http://localhost:8000/api/investments/{id}/price" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"current_price": 3550.00}'

# 3. Check performance
curl "http://localhost:8000/api/investments/analytics/top-performers" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Workflow 2: Monthly Portfolio Review

```bash
# 1. Get complete dashboard
curl "http://localhost:8000/api/dashboard/" \
  -H "Authorization: Bearer $TOKEN"

# 2. Check health score
curl "http://localhost:8000/api/dashboard/health-score" \
  -H "Authorization: Bearer $TOKEN"

# 3. Review asset allocation
curl "http://localhost:8000/api/investments/analytics/asset-allocation" \
  -H "Authorization: Bearer $TOKEN"

# 4. Export data for records
curl "http://localhost:8000/api/export/complete" \
  -H "Authorization: Bearer $TOKEN" > portfolio_backup.json
```

---

_Last Updated: October 16, 2025_
