import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, Any, List, Optional
import time

# Import centralized API client
from services.api_client import get_api_client, init_api_client, require_auth

# Get API client instance
api_client = get_api_client()

# Custom CSS for better styling
def load_css():
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
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #f5c6cb;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f77b4;
    }
    .api-status {
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .api-status-healthy {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .api-status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)

def show_api_status():
    """Show API connection status"""
    health = api_client.health_check()
    if health.get("success"):
        st.markdown('<div class="api-status api-status-healthy">✅ API Connected</div>',
                   unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status api-status-error">❌ API Disconnected</div>',
                   unsafe_allow_html=True)
        if st.button("🔄 Retry Connection"):
            st.rerun()

# Session state management
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
    if 'login_time' not in st.session_state:
        st.session_state.login_time = None

def set_authenticated(user: Dict[str, Any], token: str):
    st.session_state.authenticated = True
    st.session_state.user = user
    st.session_state.token = token
    st.session_state.login_time = datetime.now()
    api_client.token = token
    api_client.user = user

def logout():
    api_client.logout()
    st.session_state.current_page = 'login'
    st.rerun()

# Authentication functions
def show_login_page():
    st.title("🔐 Login to BudgetBrain")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields")
                return

            with st.spinner("Logging in..."):
                try:
                    response = api_client.login(username, password)
                    if response.get("success"):
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Login failed: {response.get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

    if st.button("Don't have an account? Register here"):
        st.session_state.current_page = 'register'
        st.rerun()

def show_register_page():
    st.title("📝 Register for BudgetBrain")

    with st.form("register_form"):
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        submitted = st.form_submit_button("Register", type="primary")

        if submitted:
            if not all([username, email, password, confirm_password]):
                st.error("Please fill in all fields")
                return

            if password != confirm_password:
                st.error("Passwords do not match")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters long")
                return

            with st.spinner("Creating account..."):
                try:
                    response = api_client.register(username, email, password)
                    if response.get("success"):
                        st.success("Registration successful! Please login.")
                        time.sleep(2)
                        st.session_state.current_page = 'login'
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {response.get('message', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

    if st.button("Already have an account? Login here"):
        st.session_state.current_page = 'login'
        st.rerun()

# Dashboard functions
def show_dashboard():
    st.title("📊 Dashboard")

    try:
        # Get aggregated data
        aggregated_response = api_client.get_aggregated_data()
        transactions_response = api_client.get_transactions(limit=1000)

        if aggregated_response.get("success") and transactions_response.get("success"):
            transactions = transactions_response.get("data", [])

            # Convert to DataFrame for analysis
            if transactions:
                df = pd.DataFrame(transactions)

                # Key Metrics
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    total_income = df[df['amount'] > 0]['amount'].sum()
                    st.metric("Total Income", f"${total_income:,.2f}")

                with col2:
                    total_expenses = abs(df[df['amount'] < 0]['amount'].sum())
                    st.metric("Total Expenses", f"${total_expenses:,.2f}")

                with col3:
                    net_balance = total_income - total_expenses
                    st.metric("Net Balance", f"${net_balance:,.2f}")

                with col4:
                    transaction_count = len(df)
                    st.metric("Total Transactions", transaction_count)

                # Charts
                st.subheader("📈 Financial Overview")

                # Income vs Expenses over time
                if 'created_at' in df.columns:
                    df['created_at'] = pd.to_datetime(df['created_at'])
                    df['date'] = df['created_at'].dt.date

                    daily_summary = df.groupby('date').agg({
                        'amount': lambda x: x[x > 0].sum() - abs(x[x < 0].sum())
                    }).reset_index()

                    fig = px.line(daily_summary, x='date', y='amount',
                                title='Daily Net Flow',
                                labels={'amount': 'Amount ($)', 'date': 'Date'})
                    st.plotly_chart(fig, use_container_width=True)

                # Expense Categories
                expense_df = df[df['amount'] < 0].copy()
                if not expense_df.empty:
                    expense_df['amount'] = expense_df['amount'].abs()
                    category_expenses = expense_df.groupby('category_id')['amount'].sum().reset_index()

                    fig2 = px.pie(category_expenses, values='amount', names='category_id',
                                title='Expense Categories')
                    st.plotly_chart(fig2, use_container_width=True)

                # Recent Transactions
                st.subheader("🕒 Recent Transactions")
                recent_df = df.sort_values('created_at', ascending=False).head(10)
                st.dataframe(recent_df[['created_at', 'amount', 'description']].style.format({
                    'amount': '${:.2f}',
                    'created_at': lambda x: x.strftime('%Y-%m-%d %H:%M') if hasattr(x, 'strftime') else str(x)
                }))

            else:
                st.info("No transactions found. Start by adding some transactions!")
        else:
            st.error("Failed to load dashboard data")

    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")

# Transaction management
def show_transactions_page():
    st.title("💳 Transactions")

    tab1, tab2 = st.tabs(["📋 View Transactions", "➕ Add Transaction"])

    with tab1:
        try:
            response = api_client.get_transactions(limit=100)
            if response.get("success"):
                transactions = response.get("data", [])
                if transactions:
                    df = pd.DataFrame(transactions)
                    st.dataframe(df[['id', 'amount', 'description', 'created_at']].style.format({
                        'amount': '${:.2f}',
                        'created_at': lambda x: x.strftime('%Y-%m-%d %H:%M') if hasattr(x, 'strftime') else str(x)
                    }))

                    # Transaction statistics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Transactions", len(df))
                    with col2:
                        avg_amount = df['amount'].mean()
                        st.metric("Average Amount", f"${avg_amount:.2f}")
                else:
                    st.info("No transactions found.")
            else:
                st.error("Failed to load transactions")
        except Exception as e:
            st.error(f"Error loading transactions: {str(e)}")

    with tab2:
        with st.form("add_transaction"):
            st.subheader("Add New Transaction")

            amount = st.number_input("Amount", step=0.01, format="%.2f")
            description = st.text_input("Description")
            transaction_type = st.selectbox("Type", ["income", "expense", "transfer"])

            # Get accounts for selection
            try:
                accounts_response = api_client.get_accounts()
                if accounts_response.get("success"):
                    accounts = accounts_response.get("data", [])
                    if accounts:
                        account_options = {acc['id']: acc['name'] for acc in accounts}
                        selected_account = st.selectbox("Account",
                                                      options=list(account_options.keys()),
                                                      format_func=lambda x: account_options[x])
                    else:
                        st.warning("No accounts found. Please create an account first.")
                        selected_account = None
                else:
                    st.error("Failed to load accounts")
                    selected_account = None
            except:
                selected_account = None

            submitted = st.form_submit_button("Add Transaction")

            if submitted:
                if not description or amount == 0:
                    st.error("Please fill in all required fields")
                    return

                # Adjust amount based on type
                if transaction_type == "expense":
                    amount = -abs(amount)

                transaction_data = {
                    "amount": amount,
                    "description": description,
                    "account_id": selected_account
                }

                try:
                    response = api_client.create_transaction(transaction_data)
                    if response.get("success"):
                        st.success("Transaction added successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Failed to add transaction: {response.get('message')}")
                except Exception as e:
                    st.error(f"Error adding transaction: {str(e)}")

# Account management
def show_accounts_page():
    st.title("🏦 Accounts")

    tab1, tab2 = st.tabs(["📋 View Accounts", "➕ Add Account"])

    with tab1:
        try:
            response = api_client.get_accounts()
            if response.get("success"):
                accounts = response.get("data", [])
                if accounts:
                    df = pd.DataFrame(accounts)
                    st.dataframe(df[['id', 'name', 'balance', 'currency']].style.format({
                        'balance': '${:.2f}'
                    }))

                    # Account statistics
                    total_balance = df['balance'].sum()
                    st.metric("Total Balance Across All Accounts", f"${total_balance:,.2f}")
                else:
                    st.info("No accounts found.")
            else:
                st.error("Failed to load accounts")
        except Exception as e:
            st.error(f"Error loading accounts: {str(e)}")

    with tab2:
        with st.form("add_account"):
            st.subheader("Add New Account")

            name = st.text_input("Account Name")
            account_type = st.selectbox("Account Type",
                                      ["checking", "savings", "credit_card", "investment"])
            balance = st.number_input("Initial Balance", step=0.01, format="%.2f")
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "INR"])

            submitted = st.form_submit_button("Add Account")

            if submitted:
                if not name:
                    st.error("Please enter an account name")
                    return

                account_data = {
                    "name": name,
                    "account_type": account_type,
                    "balance": balance,
                    "currency": currency
                }

                try:
                    response = api_client.create_account(account_data)
                    if response.get("success"):
                        st.success("Account added successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"Failed to add account: {response.get('message')}")
                except Exception as e:
                    st.error(f"Error adding account: {str(e)}")

# Main app
def main():
    st.set_page_config(
        page_title="BudgetBrain - Personal Finance Manager",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css()
    init_session_state()
    init_api_client()  # Initialize API client from cache

    # Sidebar navigation
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown('<div class="sidebar-header">💰 BudgetBrain</div>', unsafe_allow_html=True)

            # API Status
            show_api_status()

            if st.session_state.user:
                st.write(f"👤 {st.session_state.user['username']}")
                st.write(f"📧 {st.session_state.user['email']}")

            st.markdown("---")

            pages = {
                "Dashboard": "dashboard",
                "Transactions": "transactions",
                "Accounts": "accounts",
                "Statement Upload": "statement_upload",
                "Analytics": "analytics",
                "AI Suggestions": "ai_suggestions"
            }

            for page_name, page_key in pages.items():
                if st.button(page_name, key=f"nav_{page_key}",
                           help=f"Go to {page_name}",
                           use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()

            st.markdown("---")
            if st.button("🚪 Logout", type="secondary", use_container_width=True):
                logout()

    # Main content
    if not st.session_state.authenticated:
        if st.session_state.current_page == 'register':
            show_register_page()
        else:
            show_login_page()
    else:
        if st.session_state.current_page == 'dashboard':
            show_dashboard()
        elif st.session_state.current_page == 'transactions':
            show_transactions_page()
        elif st.session_state.current_page == 'accounts':
            show_accounts_page()
        elif st.session_state.current_page == 'categories':
            st.title("📂 Categories")
            st.info("Categories management coming soon!")
        elif st.session_state.current_page == 'analytics':
            st.title("📊 Advanced Analytics")
            st.info("Advanced analytics coming soon!")
        elif st.session_state.current_page == 'ai_suggestions':
            from pages.ai_suggestions import show_ai_suggestions_page
            show_ai_suggestions_page()
        elif st.session_state.current_page == 'analytics':
            from pages.analytics import show_analytics_page
            show_analytics_page()
        elif st.session_state.current_page == 'statement_upload':
            from pages.statement_upload import show_statement_upload_page
            show_statement_upload_page()
        else:
            show_dashboard()

if __name__ == "__main__":
    main()
