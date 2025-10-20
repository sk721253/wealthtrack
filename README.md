# 💰 WealthTrack - Personal Wealth Management System

A comprehensive full-stack web application to track expenses, manage investments, and build wealth with intelligent insights.

![WealthTrack Dashboard](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![React](https://img.shields.io/badge/React-18.3-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.6-blue)

## 🚀 Features

### ✅ Expense Tracking

- Create, read, update, and delete expenses
- Category-based filtering and organization
- Monthly and category-wise summaries
- CSV export functionality
- Payment method tracking

### 📈 Investment Portfolio Management

- Multi-asset support (Stocks, Mutual Funds, FD, Gold, Crypto, Bonds)
- Real-time portfolio valuation
- Gains/Losses calculation with percentage tracking
- Asset allocation analysis
- Platform-wise breakdown
- Top/Worst performers tracking
- Bulk price updates

### 📊 Dashboard & Analytics

- Combined financial overview
- Net worth calculation
- Financial health score with recommendations
- Monthly expense trends
- Investment performance metrics
- Visual charts and statistics

### 🔐 Security

- JWT-based authentication
- Bcrypt password hashing
- Protected API routes
- Secure token management

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL 16.x
- **ORM**: SQLAlchemy 2.0.36
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic 2.10.3
- **Server**: Uvicorn 0.32.0

### Frontend

- **Framework**: React 18.3.1 with TypeScript 5.6
- **Routing**: React Router 6.26.0
- **State Management**: Zustand 4.5.0
- **HTTP Client**: Axios 1.7.0
- **Styling**: Tailwind CSS 3.4.0
- **Icons**: Lucide React 0.454.0
- **Notifications**: Sonner 1.5.0
- **Date Handling**: date-fns 4.1.0
- **Forms**: React Hook Form 7.53.0
- **Validation**: Zod 3.23.0

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 20.x LTS
- **PostgreSQL**: 16.x
- **npm**: 10.x (comes with Node.js)

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/wealthtrack.git
cd wealthtrack
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and update:
# - DATABASE_URL with your PostgreSQL credentials
# - SECRET_KEY (generate using: python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### 3. Database Setup

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE wealthtrack;

# Exit
\q
```

### 4. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will run on `http://localhost:8000`

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Verify REACT_APP_API_URL is set to http://localhost:8000
```

### 6. Run Frontend

```bash
npm start
```

Frontend will run on `http://localhost:3000`

## 📚 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Backend Tests

```bash
cd backend
python test_week2_complete.py
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📁 Project Structure

```
wealthtrack/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── store/          # Zustand stores
│   │   ├── types/          # TypeScript types
│   │   ├── utils/          # Utilities
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── .env.example
│   └── README.md
└── README.md
```

## 🌐 Deployment

### Backend (Railway/Render)

1. Create account on Railway or Render
2. Connect GitHub repository
3. Add environment variables
4. Deploy backend

### Frontend (Vercel/Netlify)

1. Create account on Vercel or Netlify
2. Connect GitHub repository
3. Set build command: `npm run build`
4. Set publish directory: `build`
5. Add environment variables
6. Deploy frontend

## 📊 Features Overview

### Expense Management

- ✅ CRUD operations for expenses
- ✅ Category filtering
- ✅ Date range filtering
- ✅ Monthly summaries
- ✅ CSV export

### Investment Tracking

- ✅ Multiple asset types support
- ✅ Real-time portfolio valuation
- ✅ Automatic gain/loss calculation
- ✅ Performance analytics
- ✅ Asset allocation breakdown

### Dashboard

- ✅ Financial overview
- ✅ Health score calculation
- ✅ Top performers display
- ✅ Expense trends
- ✅ Recommendations

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Your Name - [your.email@example.com](mailto:your.email@example.com)

## 🙏 Acknowledgments

- FastAPI Documentation
- React Documentation
- Tailwind CSS
- Lucide Icons

## 📞 Support

For support, email your.email@example.com or create an issue on GitHub.

---

**Made with ❤️ for better financial management**

**Version**: 2.0.0  
**Last Updated**: October 2025
