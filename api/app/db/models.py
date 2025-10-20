from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    __tablename__ = "tb_bb_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    accounts = relationship("Account", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    user_details = relationship("UserDetails", back_populates="user", uselist=False)


class UserDetails(Base):
    __tablename__ = "tb_bb_user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    date_of_birth = Column(DateTime(timezone=True), nullable=True)
    profile_picture = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="user_details")


class AccountMaster(Base):
    __tablename__ = "tb_bb_account_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_name = Column(String, index=True)
    account_type = Column(String)  # checking, savings, credit_card, etc.
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="account_master")
    transaction_master = relationship("TransactionMaster", back_populates="account")
    statement_details_extract = relationship("StatementDetailsExtract", back_populates="account")


class MoneyNameMaster(Base):
    __tablename__ = "tb_bb_money_name_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)  # e.g., "Salary", "Rent", "Groceries"
    type = Column(String)  # income, expense
    category = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="money_name_master")
    transaction_master = relationship("TransactionMaster", back_populates="money_name")


class TransactionMaster(Base):
    __tablename__ = "tb_bb_transaction_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("account_master.id"))
    money_name_id = Column(Integer, ForeignKey("money_name_master.id"), nullable=True)
    amount = Column(Float)
    description = Column(String, nullable=True)
    transaction_date = Column(DateTime(timezone=True))
    transaction_type = Column(String)  # income, expense, transfer
    payment_method = Column(String, nullable=True)  # cash, card, online, etc.
    tags = Column(JSON, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transaction_master")
    account = relationship("AccountMaster", back_populates="transaction_master")
    money_name = relationship("MoneyNameMaster", back_populates="transaction_master")


class OnlinePaymentNameMaster(Base):
    __tablename__ = "tb_bb_online_payment_name_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_name = Column(String, index=True)  # e.g., "PayPal", "Venmo", "Zelle"
    provider = Column(String, nullable=True)
    account_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="online_payment_name_master")


class StatementDetailsExtract(Base):
    __tablename__ = "tb_bb_statement_details_extract"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("account_master.id"), nullable=True)
    statement_date = Column(DateTime(timezone=True))
    transaction_date = Column(DateTime(timezone=True))
    description = Column(String)
    amount = Column(Float)
    balance = Column(Float, nullable=True)
    category = Column(String, nullable=True)
    extracted_data = Column(JSON, nullable=True)  # Additional extracted fields
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="statement_details_extract")
    account = relationship("AccountMaster", back_populates="statement_details_extract")


class RefreshToken(Base):
    __tablename__ = "tb_bb_refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True))
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="refresh_tokens")


class Account(Base):
    __tablename__ = "tb_bb_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    type = Column(String)  # checking, savings, credit_card, etc.
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    account_master = relationship("AccountMaster", back_populates="user")
    money_name_master = relationship("MoneyNameMaster", back_populates="user")
    transaction_master = relationship("TransactionMaster", back_populates="user")
    online_payment_name_master = relationship("OnlinePaymentNameMaster", back_populates="user")
    statement_details_extract = relationship("StatementDetailsExtract", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class Category(Base):
    __tablename__ = "tb_bb_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # income, expense
    color = Column(String, default="#000000")
    icon = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "tb_bb_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime(timezone=True))
    type = Column(String)  # income, expense, transfer
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(String, nullable=True)  # daily, weekly, monthly, yearly
    tags = Column(Text, nullable=True)  # JSON string for tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Loan(Base):
    __tablename__ = "tb_bb_loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    principal_amount = Column(Float)
    interest_rate = Column(Float)
    term_months = Column(Integer)
    monthly_payment = Column(Float)
    remaining_balance = Column(Float)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True), nullable=True)
    lender = Column(String)
    loan_type = Column(String)  # personal, mortgage, auto, etc.
    status = Column(String, default="active")  # active, paid_off, defaulted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Investment(Base):
    __tablename__ = "tb_bb_investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)  # stock, bond, mutual_fund, crypto, etc.
    symbol = Column(String, nullable=True)
    quantity = Column(Float)
    purchase_price = Column(Float)
    current_price = Column(Float, nullable=True)
    purchase_date = Column(DateTime(timezone=True))
    brokerage = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
