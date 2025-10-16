# 💰 WealthTrack - Personal Wealth Management System

A comprehensive personal finance platform to track expenses, investments, and build wealth with AI-powered insights.

## 🚀 Features

### Week 1 - MVP (Completed)

- ✅ User Authentication (Register, Login, JWT)
- ✅ Expense Tracking (CRUD operations)
- ✅ Category Management
- ✅ Date-based Filtering
- ✅ Expense Summaries (By Category, By Month)
- ✅ Pagination & Search

### Upcoming Features

- 📊 Investment Tracking
- 📈 Portfolio Dashboard
- 🤖 AI-Powered Insights
- 📱 Mobile Responsive Frontend
- 📧 Email Notifications
- 📊 Advanced Analytics

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

| Method | Endpoint             | Description       | Auth Required |
| ------ | -------------------- | ----------------- | ------------- |
| POST   | `/api/auth/register` | Register new user | No            |
| POST   | `/api/auth/login`    | Login user        | No            |
| GET    | `/api/auth/me`       | Get current user  | Yes           |

### Expenses

| Method | Endpoint                            | Description        | Auth Required |
| ------ | ----------------------------------- | ------------------ | ------------- |
| POST   | `/api/expenses/`                    | Create expense     | Yes           |
| GET    | `/api/expenses/`                    | Get all expenses   | Yes           |
| GET    | `/api/expenses/{id}`                | Get single expense | Yes           |
| PUT    | `/api/expenses/{id}`                | Update expense     | Yes           |
| DELETE | `/api/expenses/{id}`                | Delete expense     | Yes           |
| GET    | `/api/expenses/summary/by-category` | Category summary   | Yes           |
| GET    | `/api/expenses/summary/by-month`    | Monthly summary    | Yes           |

## 🧪 Testing

### Manual Testing with Swagger UI

1. Go to http://localhost:8000/docs
2. Register a new user
3. Login to get access token
4. Click "Authorize" and enter: `Bearer <your_token>`
5. Test all endpoints

### Create Test Data

```bash
python create_test_data.py
```

### Using Thunder Client (VS Code)

1. Install Thunder Client extension
2. Import the Thunder Client collection
3. Set environment variables
4. Run tests

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── dependencies.py         # Dependency injection
│   ├── core/
│   │   ├── config.py          # Settings & configuration
│   │   └── exceptions.py      # Custom exceptions
│   ├── models/
│   │   ├── user.py            # User model
│   │   └── expense.py         # Expense model
│   ├── schemas/
│   │   ├── user.py            # User schemas
│   │   ├── expense.py         # Expense schemas
│   │   └── token.py           # Token schemas
│   ├── routes/
│   │   ├── auth.py            # Authentication routes
│   │   └── expenses.py        # Expense routes
│   ├── services/
│   │   ├── auth_service.py    # Auth business logic
│   │   └── expense_service.py # Expense business logic
│   └── utils/
│       ├── security.py        # Security utilities
│       └── validators.py      # Validation helpers
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## 🔐 Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 30 minutes
- All sensitive routes require authentication
- SQL injection prevention through SQLAlchemy ORM
- Input validation using Pydantic
- CORS configured for security

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
# Windows: Check Services
# Mac/Linux: sudo service postgresql status

# Verify DATABASE_URL in .env
# Format: postgresql://username:password@localhost:5432/database_name
```

### Import Errors

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### Token Authentication Fails

```bash
# Check SECRET_KEY in .env
# Ensure token is passed as: Bearer <token>
# Token may have expired (default: 30 min)
```

## 📊 Database Schema

### Users Table

```sql
- id: UUID (Primary Key)
- email: VARCHAR (Unique)
- full_name: VARCHAR
- hashed_password: VARCHAR
- is_active: BOOLEAN
- is_verified: BOOLEAN
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

### Expenses Table

```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- title: VARCHAR(200)
- amount: NUMERIC(10,2)
- category: VARCHAR(50)
- date: DATE
- payment_method: VARCHAR(50)
- notes: VARCHAR(500)
- created_at: TIMESTAMP
- updated_at: TIMESTAMP
```

## 🎯 Expense Categories

- Food
- Transport
- Entertainment
- Shopping
- Bills
- Healthcare
- Education
- Other

## 💡 Usage Examples

### Register User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123!"
```

### Create Expense

```bash
curl -X POST "http://localhost:8000/api/expenses/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Grocery Shopping",
    "amount": 2500.00,
    "category": "Food",
    "date": "2025-01-15",
    "payment_method": "Credit Card",
    "notes": "Weekly groceries"
  }'
```

### Get Expenses with Filters

```bash
curl "http://localhost:8000/api/expenses/?category=Food&start_date=2025-01-01" \
  -H "Authorization: Bearer <your_token>"
```

## 🚀 Deployment

### Local Development

```bash
uvicorn app.main:app --reload
```

### Production (Railway/Render)

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## 📝 Environment Variables

| Variable                    | Description                  | Example                                  |
| --------------------------- | ---------------------------- | ---------------------------------------- |
| DATABASE_URL                | PostgreSQL connection string | postgresql://user:pass@localhost:5432/db |
| SECRET_KEY                  | JWT secret key               | random-secret-key-here                   |
| ALGORITHM                   | JWT algorithm                | HS256                                    |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry time            | 30                                       |
| APP_NAME                    | Application name             | WealthTrack                              |
| DEBUG                       | Debug mode                   | True/False                               |

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Your Name - [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/wealthtrack](https://github.com/yourusername/wealthtrack)

## 🙏 Acknowledgments

- FastAPI Documentation
- SQLAlchemy Documentation
- Pydantic Documentation
- Real Python Tutorials

## 📞 Support

For support, email your.email@example.com or create an issue on GitHub.

---

Made with ❤️ for better financial management
