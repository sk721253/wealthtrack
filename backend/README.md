# Update backend/README.md

# 💰 WealthTrack - Personal Wealth Management System

A comprehensive personal finance platform to track expenses, manage investments, and build wealth with intelligent insights.

## 🚀 Features

### ✅ Week 1 - Expense Tracker (Completed)

- User Authentication (Register, Login, JWT)
- Expense Tracking (CRUD operations)
- Category Management & Filtering
- Monthly Summaries & Analytics
- Data Export (CSV)

### ✅ Week 2 - Investment Tracker (Completed)

- Multi-asset Investment Tracking (Stocks, Mutual Funds, FD, Gold, Crypto, Bonds)
- Real-time Portfolio Valuation
- Gains/Losses Calculation
- Asset Allocation Analysis
- Top/Worst Performers Tracking
- Platform-wise Breakdown
- Combined Financial Dashboard
- Financial Health Score
- Bulk Operations
- Complete Data Export

### 🔮 Future Features

- AI-Powered Recommendations
- Budget Planning & Alerts
- Tax Optimization
- Goal-Based Planning
- Real-time Price Updates
- Mobile App

## 🛠️ Tech Stack

- **Backend**: FastAPI 0.115.0
- **Database**: PostgreSQL 16.x
- **ORM**: SQLAlchemy 2.0.36
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.10.3
- **Server**: Uvicorn 0.32.0

## 📋 Prerequisites

- Python 3.11 or higher
- PostgreSQL 16.x
- pip (Python package manager)
- Virtual environment (venv)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd wealthtrack/backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE wealthtrack;

# Exit
\q
```

### 5. Configure environment variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and update:
# - DATABASE_URL with your PostgreSQL credentials
# - SECRET_KEY (generate using: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

### 7. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Authentication

| Method | Endpoint             | Description       |
| ------ | -------------------- | ----------------- |
| POST   | `/api/auth/register` | Register new user |
| POST   | `/api/auth/login`    | Login user        |
| GET    | `/api/auth/me`       | Get current user  |

### Expenses

| Method | Endpoint                            | Description        |
| ------ | ----------------------------------- | ------------------ |
| POST   | `/api/expenses/`                    | Create expense     |
| GET    | `/api/expenses/`                    | Get all expenses   |
| GET    | `/api/expenses/{id}`                | Get single expense |
| PUT    | `/api/expenses/{id}`                | Update expense     |
| DELETE | `/api/expenses/{id}`                | Delete expense     |
| GET    | `/api/expenses/summary/by-category` | Category summary   |
| GET    | `/api/expenses/summary/by-month`    | Monthly summary    |

### Investments

| Method | Endpoint                              | Description           |
| ------ | ------------------------------------- | --------------------- |
| POST   | `/api/investments/`                   | Create investment     |
| GET    | `/api/investments/`                   | Get all investments   |
| GET    | `/api/investments/{id}`               | Get single investment |
| PUT    | `/api/investments/{id}`               | Update investment     |
| PATCH  | `/api/investments/{id}/price`         | Update price          |
| DELETE | `/api/investments/{id}`               | Delete investment     |
| POST   | `/api/investments/bulk-update-prices` | Bulk price update     |

### Analytics

| Method | Endpoint                                      | Description          |
| ------ | --------------------------------------------- | -------------------- |
| GET    | `/api/investments/analytics/asset-allocation` | Asset allocation     |
| GET    | `/api/investments/analytics/top-performers`   | Top performers       |
| GET    | `/api/investments/analytics/worst-performers` | Worst performers     |
| GET    | `/api/investments/analytics/platform-summary` | Platform breakdown   |
| GET    | `/api/investments/analytics/statistics`       | Detailed statistics  |
| GET    | `/api/investments/analytics/maturing-soon`    | Maturing investments |

### Dashboard

| Method | Endpoint                      | Description            |
| ------ | ----------------------------- | ---------------------- |
| GET    | `/api/dashboard/`             | Complete dashboard     |
| GET    | `/api/dashboard/health-score` | Financial health score |

### Export

| Method | Endpoint                      | Description               |
| ------ | ----------------------------- | ------------------------- |
| GET    | `/api/export/expenses/csv`    | Export expenses CSV       |
| GET    | `/api/export/investments/csv` | Export investments CSV    |
| GET    | `/api/export/complete`        | Export complete data JSON |

## 🧪 Testing

### Create Test Data

```bash
# Create expense test data
python create_test_data.py

# Create investment test data
python create_investment_test_data.py

# Run complete Week 2 tests
python test_week2_complete.py

# Generate summary report
python week2_summary.py
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── database.py                # Database configuration
│   ├── dependencies.py            # Dependency injection
│   ├── core/
│   │   ├── config.py             # Settings
│   │   └── exceptions.py         # Custom exceptions
│   ├── models/
│   │   ├── user.py               # User model
│   │   ├── expense.py            # Expense model
│   │   └── investment.py         # Investment model
│   ├── schemas/
│   │   ├── user.py               # User schemas
│   │   ├── expense.py            # Expense schemas
│   │   ├── investment.py         # Investment schemas
│   │   └── token.py              # Token schemas
│   ├── routes/
│   │   ├── auth.py               # Authentication routes
│   │   ├── expenses.py           # Expense routes
│   │   ├── investments.py        # Investment routes
│   │   ├── dashboard.py          # Dashboard routes
│   │   └── export.py             # Export routes
│   ├── services/
│   │   ├── auth_service.py       # Auth business logic
│   │   ├── expense_service.py    # Expense logic
│   │   ├── investment_service.py # Investment logic
│   │   ├── dashboard_service.py  # Dashboard logic
│   │   └── export_service.py     # Export logic
│   └── utils/
│       ├── security.py           # Security utilities
│       └── validators.py         # Validation helpers
├── tests/                         # Test files
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── INVESTMENT_API_DOCS.md
└── INVESTMENT_SCHEMA.md
```

## 🔐 Security

- Passwords hashed using bcrypt
- JWT tokens with expiry
- Protected routes require authentication
- SQL injection prevention via ORM
- Input validation with Pydantic
- CORS configured

## 📊 Database Schema

### Users Table

- id, email, full_name, hashed_password
- is_active, is_verified
- created_at, updated_at

### Expenses Table

- id, user_id, title, amount, category
- date, payment_method, notes
- created_at, updated_at

### Investments Table

- id, user_id, asset_type, asset_name, symbol
- quantity, purchase_price, current_price
- purchase_date, maturity_date
- platform, interest_rate, notes
- created_at, updated_at

## 🚀 Deployment

### Production Setup

```bash
# Set environment to production
DEBUG=False

# Use PostgreSQL in production
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Strong secret key
SECRET_KEY=<generate-strong-key>

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Environment Variables

| Variable                    | Description           | Example          |
| --------------------------- | --------------------- | ---------------- |
| DATABASE_URL                | PostgreSQL connection | postgresql://... |
| SECRET_KEY                  | JWT secret key        | random-secret    |
| ALGORITHM                   | JWT algorithm         | HS256            |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry          | 30               |
| APP_NAME                    | Application name      | WealthTrack      |
| DEBUG                       | Debug mode            | True/False       |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License

## 👨‍💻 Author

Your Name - your.email@example.com

## 🙏 Acknowledgments

- FastAPI Documentation
- SQLAlchemy Documentation
- Pydantic Documentation

## 📞 Support

For support, create an issue on GitHub.

---

**Made with ❤️ for better financial management**

**Version**: 2.0.0  
**Last Updated**: October 2025
