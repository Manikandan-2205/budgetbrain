#!/usr/bin/env python3
"""
Seed demo data for BudgetBrain application
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.user_details import UserDetails
from app.models.account_master import AccountMaster
from app.models.money_name_master import MoneyNameMaster
from app.models.transaction_master import TransactionMaster
from app.models.online_payment_name_master import OnlinePaymentNameMaster
from app.models.category import Category
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.loan import Loan
from app.models.investment import Investment
from app.models.aggregated import AggregatedModel
from app.models.refresh_token import RefreshToken
from app.models.statement_details_extract import StatementDetailsExtract
from app.models.activity_log import ActivityLog
from app.core.security import get_password_hash
from datetime import datetime

def seed_demo_data():
    """Seed demo data into the database"""
    db = SessionLocal()

    try:
        print("Seeding demo data...")

        # Create demo user (developer role)
        demo_user = User(
            username="manikandan",
            email="mani@gmail.com",
            hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Le0KdskJc2zK5qM2e",  # Pre-hashed password for "123"
            role="developer",
            is_active=True
        )

        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "manikandan").first()
        if existing_user:
            print("Demo user already exists")
            db.close()
            return

        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print(f"Created demo user: {demo_user.username} (ID: {demo_user.id})")

        # Create user details
        user_details = UserDetails(
            user_id=demo_user.id,
            first_name="Manikandan",
            last_name="Developer"
        )
        db.add(user_details)
        db.commit()
        print("Created user details")

        # Seed Indian banks for account master
        indian_banks = [
            "State Bank of India (SBI)",
            "HDFC Bank",
            "ICICI Bank",
            "Axis Bank",
            "Kotak Mahindra Bank",
            "IndusInd Bank",
            "Punjab National Bank (PNB)",
            "Bank of Baroda",
            "Canara Bank",
            "Union Bank of India",
            "IDBI Bank",
            "Federal Bank",
            "South Indian Bank",
            "RBL Bank",
            "Bandhan Bank",
            "IDFC First Bank",
            "Yes Bank",
            "Indian Overseas Bank",
            "Central Bank of India",
            "UCO Bank"
        ]

        for bank_name in indian_banks:
            account_master = AccountMaster(
                user_id=demo_user.id,
                account_name=f"{bank_name} Savings Account",
                account_type="savings",
                bank_name=bank_name,
                currency="INR"
            )
            db.add(account_master)

        db.commit()
        print(f"Created {len(indian_banks)} Indian bank accounts")

        # Seed money name master (income/expense categories)
        money_names = [
            # Income sources
            "Salary",
            "Freelance Income",
            "Business Income",
            "Investment Returns",
            "Rental Income",
            "Interest Income",
            "Gift Money",
            "Bonus",
            "Commission",

            # Expense categories
            "Food & Dining",
            "Transportation",
            "Shopping",
            "Entertainment",
            "Bills & Utilities",
            "Healthcare",
            "Education",
            "Travel",
            "Insurance",
            "Taxes",
            "Home & Garden",
            "Personal Care",
            "Subscriptions",
            "Gifts & Donations",
            "Miscellaneous"
        ]

        for name in money_names:
            money_master = MoneyNameMaster(
                user_id=demo_user.id,
                name=name
            )
            db.add(money_master)

        db.commit()
        print(f"Created {len(money_names)} money name categories")

        # Seed online payment methods
        payment_methods = [
            "Google Pay",
            "PhonePe",
            "Paytm",
            "Amazon Pay",
            "BHIM UPI",
            "Cred",
            "Simpl",
            "Mobikwik",
            "Freecharge",
            "Airtel Money",
            "JioMoney",
            "PayPal",
            "Net Banking",
            "Debit Card",
            "Credit Card",
            "Cash"
        ]

        for method in payment_methods:
            payment_master = OnlinePaymentNameMaster(
                user_id=demo_user.id,
                payment_name=method
            )
            db.add(payment_master)

        db.commit()
        print(f"Created {len(payment_methods)} payment methods")

        # Seed default categories
        default_categories = [
            {"name": "Food & Dining", "type": "expense", "color": "#FF6B6B"},
            {"name": "Transportation", "type": "expense", "color": "#4ECDC4"},
            {"name": "Shopping", "type": "expense", "color": "#45B7D1"},
            {"name": "Entertainment", "type": "expense", "color": "#96CEB4"},
            {"name": "Bills & Utilities", "type": "expense", "color": "#FFEAA7"},
            {"name": "Healthcare", "type": "expense", "color": "#DDA0DD"},
            {"name": "Education", "type": "expense", "color": "#98D8C8"},
            {"name": "Salary", "type": "income", "color": "#6C5CE7"},
            {"name": "Freelance", "type": "income", "color": "#A29BFE"},
            {"name": "Investment", "type": "income", "color": "#74B9FF"},
            {"name": "Other Income", "type": "income", "color": "#55EFC4"},
            {"name": "Transfer", "type": "transfer", "color": "#FDCB6E"}
        ]

        for cat_data in default_categories:
            category = Category(
                name=cat_data["name"],
                type=cat_data["type"],
                color=cat_data["color"],
                is_default=True
            )
            db.add(category)

        db.commit()
        print(f"Created {len(default_categories)} default categories")

        print("\nDemo data seeding completed successfully!")
        print(f"Demo Account Details:")
        print(f"   Username: manikandan")
        print(f"   Password: 123")
        print(f"   Email: mani@gmail.com")
        print(f"   Role: developer")

    except Exception as e:
        print(f"Error seeding demo data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()