# ✅ WealthTrack Testing Checklist - Week 1

## Pre-Testing Setup

- [ ] Virtual environment activated
- [ ] All dependencies installed
- [ ] PostgreSQL running
- [ ] Database created and configured
- [ ] .env file configured correctly
- [ ] Server starts without errors

---

## Authentication Tests

### Registration

- [ ] Can register with valid email and password
- [ ] Cannot register with existing email
- [ ] Cannot register with invalid email format
- [ ] Cannot register with weak password (<8 chars)
- [ ] Cannot register with missing full_name
- [ ] User appears in database after registration

### Login

- [ ] Can login with correct credentials
- [ ] Cannot login with wrong password
- [ ] Cannot login with non-existent email
- [ ] Access token is returned
- [ ] Token contains correct payload

### Protected Routes

- [ ] Cannot access /api/auth/me without token
- [ ] Can access /api/auth/me with valid token
- [ ] Cannot access with expired token
- [ ] Cannot access with invalid token format

---

## Expense CRUD Tests

### Create Expense

- [ ] Can create expense with all fields
- [ ] Can create expense with only required fields
- [ ] Cannot create expense without authentication
- [ ] Cannot create expense with negative amount
- [ ] Cannot create expense with invalid date
- [ ] Cannot create expense with empty title
- [ ] Created expense shows in database
- [ ] Created_at timestamp is set

### Read Expenses

- [ ] Can get all expenses
- [ ] Get returns empty array for new user
- [ ] Get returns only user's own expenses
- [ ] Total_count matches number of expenses
- [ ] Total_amount is calculated correctly
- [ ] Expenses ordered by date (newest first)

### Read Single Expense

- [ ] Can get expense by valid ID
- [ ] Cannot get non-existent expense (404)
- [ ] Cannot get another user's expense
- [ ] Returns correct expense details

### Update Expense

- [ ] Can update title
- [ ] Can update amount
- [ ] Can update category
- [ ] Can update multiple fields at once
- [ ] Can update with partial data
- [ ] Cannot update another user's expense
- [ ] Cannot update non-existent expense
- [ ] Updated_at timestamp changes

### Delete Expense

- [ ] Can delete own expense
- [ ] Cannot delete another user's expense
- [ ] Cannot delete non-existent expense
- [ ] Expense removed from database
- [ ] Returns 204 No Content

---

## Filtering & Pagination Tests

### Category Filter

- [ ] Filter by single category works
- [ ] Returns only expenses of that category
- [ ] Returns empty for non-existent category
- [ ] Case-sensitive category matching

### Date Range Filter

- [ ] Filter by start_date works
- [ ] Filter by end_date works
- [ ] Filter by both start and end date works
- [ ] Returns expenses within date range
- [ ] Edge cases: same start and end date

### Pagination

- [ ] Skip parameter works
- [ ] Limit parameter works
- [ ] Skip + Limit combination works
- [ ] Cannot set limit > 500
- [ ] Total_count shows all records (not just page)

### Combined Filters

- [ ] Category + Date range works
- [ ] Category + Pagination works
- [ ] Date range + Pagination works
- [ ] All filters combined work

---

## Summary Endpoints Tests

### Category Summary

- [ ] Returns summary for all categories
- [ ] Total amounts are correct
- [ ] Expense counts are correct
- [ ] Respects date range filters
- [ ] Returns empty array for no expenses

### Monthly Summary

- [ ] Returns monthly breakdown
- [ ] Months are in correct order
- [ ] Amounts are correct per month
- [ ] Respects year filter
- [ ] Handles multi-year data

---

## Data Validation Tests

### Amount Validation

- [ ] Accepts valid decimal amounts
- [ ] Accepts integers as amounts
- [ ] Rejects negative amounts
- [ ] Rejects zero amount
- [ ] Handles 2 decimal places correctly
- [ ] Rejects invalid format (text)

### Date Validation

- [ ] Accepts valid date format (YYYY-MM-DD)
- [ ] Rejects invalid date format
- [ ] Rejects future dates (optional)
- [ ] Handles edge dates (month end, leap year)

### String Validation

- [ ] Title within length limits (1-200)
- [ ] Category within length limits (1-50)
- [ ] Notes within length limits (0-500)
- [ ] Rejects empty required fields
- [ ] Handles special characters

---

## Security Tests

### Authorization

- [ ] Cannot access expenses without auth token
- [ ] Cannot see other users' expenses
- [ ] Cannot update other users' expenses
- [ ] Cannot delete other users' expenses
- [ ] Token in Authorization header required

### SQL Injection

- [ ] Single quotes in input don't break query
- [ ] SQL commands in input don't execute
- [ ] Special characters handled safely

### XSS Prevention

- [ ] HTML tags in input are escaped/sanitized
- [ ] Script tags don't execute
- [ ] Special characters handled correctly

---

## Performance Tests

### Response Time

- [ ] GET /api/expenses/ responds < 1 second
- [ ] POST /api/expenses/ responds < 500ms
- [ ] Summary endpoints respond < 2 seconds
- [ ] With 100 expenses loads quickly

### Database

- [ ] No N+1 query issues
- [ ] Indexes used for common queries
- [ ] Connection pool handles concurrent requests

---

## Error Handling Tests

### API Errors

- [ ] Returns proper HTTP status codes
- [ ] Error messages are clear
- [ ] Validation errors show field details
- [ ] 500 errors don't expose sensitive info

### Database Errors

- [ ] Handles database connection loss
- [ ] Handles constraint violations
- [ ] Rolls back failed transactions

---

## Edge Cases

### Empty States

- [ ] New user with no expenses
- [ ] No expenses in date range
- [ ] No expenses in category
- [ ] Summary with no data

### Boundary Values

- [ ] Very small amount (0.01)
- [ ] Very large amount (9999999.99)
- [ ] Very old date
- [ ] Today's date
- [ ] Maximum title length
- [ ] Maximum notes length

### Special Cases

- [ ] Multiple expenses same date
- [ ] Multiple expenses same amount
- [ ] All expenses same category
- [ ] Expenses spanning multiple years

---

## Integration Tests

### Complete User Flow

- [ ] Register → Login → Create → View → Update → Delete
- [ ] Create multiple expenses → View list → Filter → Summary
- [ ] Create → Logout → Login → View (persistence)

---

## Documentation Tests

### API Documentation

- [ ] Swagger UI loads correctly
- [ ] All endpoints documented
- [ ] Can test from Swagger UI
- [ ] Request/response schemas shown
- [ ] Authentication works in Swagger

### README

- [ ] Setup instructions work
- [ ] All commands execute successfully
- [ ] Environment variables explained
- [ ] Examples are correct

---

## Test Results Summary

**Date Tested**: ******\_\_\_******

**Total Tests**: ******\_\_\_******

**Passed**: ******\_\_\_******

**Failed**: ******\_\_\_******

**Notes**:

---

---

---

---

## Known Issues

1. ***
2. ***
3. ***

---

## Improvements Needed

1. ***
2. ***
3. ***
