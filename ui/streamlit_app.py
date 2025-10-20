import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
from utils.api_client import APIClient
from utils.charts import create_expense_chart, create_income_chart, create_budget_progress_chart
import os

# Page configuration
st.set_page_config(
    page_title="BudgetBrain - AI-Powered Budget Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Theme configuration with multiple themes
def apply_theme(theme_name):
    if theme_name == "Light":
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1f77b4;
                text-align: center;
                margin-bottom: 2rem;
            }
            .metric-card {
                background-color: #f0f2f6;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 0.25rem solid #1f77b4;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .expense-card {
                border-left-color: #ff6b6b !important;
            }
            .income-card {
                border-left-color: #51cf66 !important;
            }
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }
            .stApp {
                background-color: #ffffff;
                color: #000000;
            }
        </style>
        """, unsafe_allow_html=True)
    elif theme_name == "Dark":
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #61dafb;
                text-align: center;
                margin-bottom: 2rem;
            }
            .metric-card {
                background-color: #2d3748;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 0.25rem solid #61dafb;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                color: #ffffff;
            }
            .expense-card {
                border-left-color: #ff6b6b !important;
            }
            .income-card {
                border-left-color: #51cf66 !important;
            }
            .sidebar .sidebar-content {
                background-color: #1a202c;
                color: #ffffff;
            }
            .stApp {
                background-color: #0f1419;
                color: #ffffff;
            }
            .stTextInput, .stTextArea, .stSelectbox, .stDateInput {
                background-color: #2d3748;
                color: #ffffff;
            }
        </style>
        """, unsafe_allow_html=True)
    elif theme_name == "Blue":
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1976d2;
                text-align: center;
                margin-bottom: 2rem;
            }
            .metric-card {
                background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 0.25rem solid #1976d2;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .expense-card {
                border-left-color: #ff6b6b !important;
            }
            .income-card {
                border-left-color: #51cf66 !important;
            }
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, #e3f2fd 0%, #f3e5f5 100%);
            }
            .stApp {
                background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            }
        </style>
        """, unsafe_allow_html=True)
    elif theme_name == "Green":
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #388e3c;
                text-align: center;
                margin-bottom: 2rem;
            }
            .metric-card {
                background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 0.25rem solid #388e3c;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .expense-card {
                border-left-color: #ff6b6b !important;
            }
            .income-card {
                border-left-color: #51cf66 !important;
            }
            .sidebar .sidebar-content {
                background: linear-gradient(180deg, #e8f5e8 0%, #fff3e0 100%);
            }
            .stApp {
                background: linear-gradient(135deg, #e8f5e8 0%, #fff3e0 100%);
            }
        </style>
        """, unsafe_allow_html=True)

# Initialize API client
api_client = APIClient()

def main():
    # Theme selector in sidebar
    with st.sidebar:
        st.title("🎨 Theme Settings")
        theme = st.selectbox(
            "Choose Theme",
            ["Light", "Dark", "Blue", "Green"],
            index=0,
            key="theme_selector"
        )

        # Apply selected theme
        apply_theme(theme)

    # Main header
    st.markdown('<h1 class="main-header">💰 BudgetBrain</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">AI-Powered Personal Finance Management</p>', unsafe_allow_html=True)

    # Authentication
    if not st.session_state.get('authenticated', False):
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("🔐 Login to Your Account")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login", use_container_width=True):
                if api_client.login(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        st.divider()
        st.subheader("📝 Create New Account")

        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")

            if st.form_submit_button("Register", use_container_width=True):
                if api_client.register(new_username, new_email, new_password):
                    st.success("Account created successfully! Please login.")
                else:
                    st.error("Registration failed")

def show_main_app():
    # Sidebar navigation
    with st.sidebar:
        st.subheader(f"👋 Welcome, {st.session_state.get('username', 'User')}")

        page = st.radio(
            "Navigation",
            ["Dashboard", "Transactions", "Accounts", "AI Suggestions", "Analytics", "Settings"]
        )

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.rerun()

    # Main content based on selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Transactions":
        show_transactions()
    elif page == "Accounts":
        show_accounts()
    elif page == "AI Suggestions":
        show_ai_suggestions()
    elif page == "Analytics":
        show_analytics()
    elif page == "Settings":
        show_settings()

def show_dashboard():
    st.header("📊 Dashboard")

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Balance", "$12,450.00", "+2.5%")

    with col2:
        st.metric("Monthly Income", "$5,200.00", "+5.2%")

    with col3:
        st.metric("Monthly Expenses", "$3,150.00", "-1.8%")

    with col4:
        st.metric("Savings Rate", "39.4%", "+3.1%")

    # Recent transactions
    st.subheader("Recent Transactions")
    transactions = api_client.get_transactions(limit=5)

    if transactions:
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(df[['date', 'description', 'amount', 'type']], use_container_width=True)
    else:
        st.info("No transactions found")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Expense Breakdown")
        # Mock data for demo
        expense_data = pd.DataFrame({
            'category': ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Other'],
            'amount': [450, 320, 180, 280, 150]
        })
        st.bar_chart(expense_data.set_index('category'))

    with col2:
        st.subheader("Income vs Expenses")
        # Mock data for demo
        monthly_data = pd.DataFrame({
            'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'income': [5200, 5100, 5300, 5200, 5400, 5200],
            'expenses': [3150, 3200, 3100, 3300, 3250, 3150]
        })
        st.line_chart(monthly_data.set_index('month'))

def show_transactions():
    st.header("💳 Transactions")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("All Transactions")

        # Filters
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            date_from = st.date_input("From Date")
        with col_b:
            date_to = st.date_input("To Date")
        with col_c:
            category_filter = st.selectbox("Category", ["All", "Food", "Transportation", "Entertainment"])

        transactions = api_client.get_transactions()

        if transactions:
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
            df['amount'] = df['amount'].apply(lambda x: f"${x:,.2f}")

            # Apply filters
            if category_filter != "All":
                df = df[df['category_name'] == category_filter]

            st.dataframe(df[['date', 'description', 'amount', 'type', 'category_name']], use_container_width=True)
        else:
            st.info("No transactions found")

    with col2:
        st.subheader("Add Transaction")

        with st.form("add_transaction"):
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            description = st.text_input("Description")
            transaction_type = st.selectbox("Type", ["income", "expense"])
            date = st.date_input("Date")
            category_id = st.selectbox("Category", ["1", "2", "3"])  # Mock categories

            if st.form_submit_button("Add Transaction"):
                if api_client.add_transaction(amount, description, transaction_type, date, category_id):
                    st.success("Transaction added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add transaction")

def show_accounts():
    st.header("🏦 Accounts")

    accounts = api_client.get_accounts()

    if accounts:
        for account in accounts:
            with st.expander(f"{account['name']} - {account['type']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Balance", f"${account['balance']:,.2f}")
                with col2:
                    st.metric("Currency", account['currency'])
                with col3:
                    st.metric("Type", account['type'].title())
    else:
        st.info("No accounts found")

    # Add new account
    st.subheader("Add New Account")
    with st.form("add_account"):
        name = st.text_input("Account Name")
        account_type = st.selectbox("Type", ["checking", "savings", "credit_card"])
        balance = st.number_input("Initial Balance", step=0.01)

        if st.form_submit_button("Create Account"):
            if api_client.add_account(name, account_type, balance):
                st.success("Account created successfully!")
                st.rerun()
            else:
                st.error("Failed to create account")

def show_ai_suggestions():
    st.header("🤖 AI Suggestions")

    # Transaction categorization suggestions
    st.subheader("Smart Categorization")

    with st.form("ai_suggestion"):
        description = st.text_input("Transaction Description")
        amount = st.number_input("Amount", step=0.01)
        trans_type = st.selectbox("Type", ["income", "expense"])

        if st.form_submit_button("Get Suggestions"):
            suggestions = api_client.get_ai_suggestions(description, amount, trans_type)
            if suggestions:
                st.subheader("Suggested Categories:")
                for suggestion in suggestions['suggestions']:
                    st.write(f"• {suggestion['category_name']} (Confidence: {suggestion['confidence']:.2f})")
            else:
                st.error("Failed to get suggestions")

    # Bank statement upload
    st.subheader("Upload Bank Statement")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'csv', 'xlsx'])

    if uploaded_file is not None:
        if st.button("Process Statement"):
            result = api_client.upload_bank_statement(uploaded_file)
            if result:
                st.success(f"Processed {result['total_parsed']} transactions")
                st.dataframe(pd.DataFrame(result['transactions']))
            else:
                st.error("Failed to process statement")

def show_analytics():
    st.header("📈 Analytics")

    # Time period selector
    period = st.selectbox("Time Period", ["Last 30 days", "Last 3 months", "Last 6 months", "Last year"])

    # Mock analytics data
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Spending by Category")
        spending_data = pd.DataFrame({
            'category': ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Healthcare'],
            'amount': [850, 420, 280, 380, 220]
        })
        st.bar_chart(spending_data.set_index('category'))

    with col2:
        st.subheader("Monthly Trend")
        trend_data = pd.DataFrame({
            'month': ['Jul', 'Aug', 'Sep', 'Oct'],
            'income': [5200, 5300, 5100, 5400],
            'expenses': [3150, 3200, 3100, 3300]
        })
        st.line_chart(trend_data.set_index('month'))

    # Budget progress
    st.subheader("Budget Progress")
    budgets = [
        {"category": "Food", "budget": 800, "spent": 650, "percentage": 81.25},
        {"category": "Transportation", "budget": 400, "spent": 320, "percentage": 80.0},
        {"category": "Entertainment", "budget": 300, "spent": 180, "percentage": 60.0},
    ]

    for budget in budgets:
        progress = budget['percentage'] / 100
        st.progress(progress)
        st.write(f"{budget['category']}: ${budget['spent']:.2f} / ${budget['budget']:.2f} ({budget['percentage']:.1f}%)")

def show_settings():
    st.header("⚙️ Settings")

    st.subheader("Profile Settings")
    with st.form("profile_settings"):
        current_username = st.text_input("Username", value=st.session_state.get('username', ''))
        email = st.text_input("Email")

        if st.form_submit_button("Update Profile"):
            st.success("Profile updated successfully!")

    st.subheader("Notification Preferences")
    email_notifications = st.checkbox("Email notifications", value=True)
    budget_alerts = st.checkbox("Budget alerts", value=True)
    weekly_reports = st.checkbox("Weekly reports", value=False)

    st.subheader("Data Export")
    if st.button("Export All Data"):
        st.info("Data export feature coming soon!")

if __name__ == "__main__":
    main()
