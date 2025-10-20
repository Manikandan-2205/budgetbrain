# BudgetBrain API

AI-powered personal finance management API built with FastAPI, PostgreSQL, and JWT authentication.

## Features

- **User Authentication**: JWT-based authentication system
- **Account Management**: Track multiple bank accounts
- **Transaction Tracking**: Record income and expenses
- **Category Management**: Organize transactions with categories
- **AI-Powered Suggestions**: Get smart categorization suggestions using OpenAI
- **Bank Statement Upload**: Auto-file transactions from bank statements
- **Loan & Investment Tracking**: Monitor loans and investments
- **Swagger Documentation**: Interactive API documentation

## Setup

1. **Database Setup**:
   - Ensure PostgreSQL is running on localhost:5432
   - Run the table creation script:
     ```sql
     -- Connect to your PostgreSQL database and run:
     \i create_tables.sql
     ```
     Or use your preferred PostgreSQL client to execute `create_tables.sql`

2. **Install API Dependencies**:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   - Copy `api/.env.example` to `api/.env`
   - Update the database URL and other settings if needed

4. **Run the API** (Terminal 1):
   ```bash
   cd api
   # On Windows (Command Prompt):
   run_api.bat
   # On Windows (PowerShell):
   .\run_api.ps1
   # Or manually:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Run the UI** (Terminal 2):
   ```bash
   cd ui
   pip install -r requirements.txt
   # On Windows (Command Prompt):
   run_ui.bat
   # On Windows (PowerShell):
   .\run_ui.ps1
   # Or manually:
   streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   ```

6. **Access the Application**:
   - **API Documentation**: http://localhost:8000/docs
   - **BudgetBrain UI**: http://localhost:8501
   - **API Base URL**: http://localhost:8000/api

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Accounts
- `GET /api/accounts` - List user accounts
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/{account_id}` - Update account
- `DELETE /api/accounts/{account_id}` - Delete account

### Transactions
- `GET /api/transactions` - List user transactions
- `POST /api/transactions` - Create new transaction
- `PUT /api/transactions/{transaction_id}` - Update transaction
- `DELETE /api/transactions/{transaction_id}` - Delete transaction

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create new category

### AI/ML Features
- `POST /api/ml/suggestions` - Get AI categorization suggestions
- `POST /api/ml/upload-statement` - Upload and process bank statements

## Database Schema

The application uses PostgreSQL with the following main tables:
- `users` - User accounts
- `accounts` - Bank accounts
- `categories` - Transaction categories
- `transactions` - Financial transactions
- `loans` - Loan tracking
- `investments` - Investment tracking

## Security

- JWT tokens for authentication
- Password hashing with bcrypt
- CORS enabled for frontend integration
- Input validation with Pydantic

## Testing

Use the Swagger UI at `/docs` to test API endpoints with JWT token authentication.
