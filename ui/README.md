# BudgetBrain UI

A modern, responsive Streamlit-based frontend for the BudgetBrain personal finance management system.

## Features

### 🎨 **Modern UI/UX**
- Clean, intuitive interface with professional design
- Responsive layout that works on desktop and mobile
- Custom CSS styling for enhanced visual appeal
- Dark/light theme support

### 🔐 **Authentication & Security**
- Secure login and registration system
- JWT token-based authentication
- Role-based access control (User, Admin, Developer)
- Automatic token refresh

### 📊 **Comprehensive Dashboard**
- Real-time financial metrics and KPIs
- Interactive charts and visualizations
- Income vs expenses analysis
- Recent transactions overview
- Financial health scoring

### 💳 **Transaction Management**
- View, add, edit, and delete transactions
- Support for income, expenses, and transfers
- Transaction categorization
- Bulk import capabilities

### 🏦 **Account Management**
- Multiple account support (checking, savings, credit cards, etc.)
- Real-time balance tracking
- Account performance analytics
- Multi-currency support

### 📄 **Statement Upload**
- CSV and Excel file upload support
- Automatic transaction parsing for major banks
- Duplicate detection and prevention
- Batch import with progress tracking

### 📈 **Advanced Analytics**
- Trend analysis and pattern recognition
- Cash flow analysis
- Predictive modeling for future expenses
- Comparative analysis (year-over-year, month-over-month)
- Custom date range filtering

### 🤖 **AI-Powered Insights**
- Smart financial recommendations
- Spending pattern analysis
- Budget optimization suggestions
- Investment advice based on risk profile
- Personalized saving goals

### 🎯 **Financial Goals & Planning**
- Emergency fund tracking
- Debt reduction planning
- Investment growth projections
- Savings rate optimization
- 10-year financial forecasting

## Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Start the API Server First**
```bash
cd ../api
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. **Start the UI**
```bash
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
ui/
├── streamlit_app.py          # Main application entry point
├── requirements.txt          # Python dependencies
├── pages/                    # Page components
│   ├── analytics.py         # Advanced analytics dashboard
│   ├── ai_suggestions.py    # AI-powered financial insights
│   └── statement_upload.py  # Bank statement import functionality
└── README.md                # This file
```

## Key Features Explained

### **Responsive Design**
- Mobile-first approach with adaptive layouts
- Touch-friendly interface elements
- Optimized for various screen sizes
- Progressive enhancement for larger screens

### **Theme Management**
- Automatic dark/light mode detection
- User preference persistence
- Consistent color schemes
- Accessibility-compliant contrast ratios

### **Data Visualization**
- Interactive Plotly charts
- Real-time data updates
- Drill-down capabilities
- Export functionality for reports

### **Security Features**
- End-to-end encryption for data transmission
- Secure token storage and management
- Input validation and sanitization
- XSS and CSRF protection

### **Performance Optimization**
- Lazy loading of components
- Efficient data caching
- Background processing for heavy operations
- Optimized database queries

## Usage Guide

### **Getting Started**
1. Register a new account or login with existing credentials
2. Set up your accounts (checking, savings, credit cards)
3. Add your first transactions manually or import from statements
4. Explore the dashboard for insights
5. Use AI suggestions for personalized advice

### **Importing Bank Statements**
1. Navigate to "Statement Upload" in the sidebar
2. Select your bank type for better parsing
3. Upload CSV or Excel files
4. Review parsed transactions
5. Select target account and import

### **Using Analytics**
1. Access "Analytics" for detailed financial analysis
2. View trends, patterns, and predictions
3. Use comparative analysis for insights
4. Explore future projections

### **AI Financial Assistant**
1. Visit "AI Suggestions" for personalized advice
2. Answer risk assessment questions
3. Review spending insights and recommendations
4. Use investment calculator for planning

## API Integration

The UI communicates with the BudgetBrain API through REST endpoints:

- **Authentication**: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`
- **Transactions**: `/api/transactions/`
- **Accounts**: `/api/accounts/`
- **Analytics**: `/api/aggregated/`

All requests include proper JWT authentication headers.

## Contributing

1. Follow the existing code structure and naming conventions
2. Add proper error handling and user feedback
3. Include docstrings for new functions
4. Test on multiple screen sizes and browsers
5. Ensure accessibility compliance

## Troubleshooting

### **Common Issues**

**Connection Error**: Ensure the API server is running on port 8000
**Authentication Failed**: Check username/password and API connectivity
**File Upload Issues**: Verify file format and size limits
**Chart Not Loading**: Check data availability and network connection

### **Performance Tips**
- Clear browser cache for UI updates
- Use smaller date ranges for better performance
- Close unused browser tabs
- Ensure stable internet connection

## License

This project is part of the BudgetBrain personal finance management system.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API server logs for backend issues
3. Ensure all dependencies are properly installed
4. Verify network connectivity to the API server