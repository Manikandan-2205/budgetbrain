from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from app.db.base import Base


class AggregatedModel(Base):
    __tablename__ = "tb_bb_aggregated"

    id = Column(Integer, primary_key=True, index=True)

    # From User
    user_id = Column(Integer)
    user_email = Column(String)
    user_username = Column(String)
    user_hashed_password = Column(String)
    user_is_active = Column(Boolean)
    user_created_at = Column(DateTime(timezone=True))
    user_updated_at = Column(DateTime(timezone=True))

    # From UserDetails
    user_details_id = Column(Integer)
    user_details_user_id = Column(Integer)
    user_details_first_name = Column(String, nullable=True)
    user_details_last_name = Column(String, nullable=True)
    user_details_phone = Column(String, nullable=True)
    user_details_address = Column(Text, nullable=True)
    user_details_date_of_birth = Column(DateTime(timezone=True), nullable=True)
    user_details_profile_picture = Column(String, nullable=True)
    user_details_created_at = Column(DateTime(timezone=True))
    user_details_updated_at = Column(DateTime(timezone=True))

    # From AccountMaster
    account_master_id = Column(Integer)
    account_master_user_id = Column(Integer)
    account_master_account_name = Column(String)
    account_master_account_type = Column(String)
    account_master_bank_name = Column(String, nullable=True)
    account_master_account_number = Column(String, nullable=True)
    account_master_balance = Column(Float)
    account_master_currency = Column(String)
    account_master_is_active = Column(Boolean)
    account_master_created_at = Column(DateTime(timezone=True))
    account_master_updated_at = Column(DateTime(timezone=True))

    # From MoneyNameMaster
    money_name_master_id = Column(Integer)
    money_name_master_user_id = Column(Integer)
    money_name_master_name = Column(String)
    money_name_master_type = Column(String)
    money_name_master_category = Column(String, nullable=True)
    money_name_master_is_default = Column(Boolean)
    money_name_master_created_at = Column(DateTime(timezone=True))

    # From TransactionMaster
    transaction_master_id = Column(Integer)
    transaction_master_user_id = Column(Integer)
    transaction_master_account_id = Column(Integer)
    transaction_master_money_name_id = Column(Integer, nullable=True)
    transaction_master_amount = Column(Float)
    transaction_master_description = Column(String, nullable=True)
    transaction_master_transaction_date = Column(DateTime(timezone=True))
    transaction_master_transaction_type = Column(String)
    transaction_master_payment_method = Column(String, nullable=True)
    transaction_master_tags = Column(JSON, nullable=True)
    transaction_master_is_recurring = Column(Boolean)
    transaction_master_recurring_frequency = Column(String, nullable=True)
    transaction_master_created_at = Column(DateTime(timezone=True))
    transaction_master_updated_at = Column(DateTime(timezone=True))

    # From OnlinePaymentNameMaster
    online_payment_name_master_id = Column(Integer)
    online_payment_name_master_user_id = Column(Integer)
    online_payment_name_master_payment_name = Column(String)
    online_payment_name_master_provider = Column(String, nullable=True)
    online_payment_name_master_account_email = Column(String, nullable=True)
    online_payment_name_master_is_active = Column(Boolean)
    online_payment_name_master_created_at = Column(DateTime(timezone=True))
    online_payment_name_master_updated_at = Column(DateTime(timezone=True))

    # From StatementDetailsExtract
    statement_details_extract_id = Column(Integer)
    statement_details_extract_user_id = Column(Integer)
    statement_details_extract_account_id = Column(Integer, nullable=True)
    statement_details_extract_statement_date = Column(DateTime(timezone=True))
    statement_details_extract_transaction_date = Column(DateTime(timezone=True))
    statement_details_extract_description = Column(String)
    statement_details_extract_amount = Column(Float)
    statement_details_extract_balance = Column(Float, nullable=True)
    statement_details_extract_category = Column(String, nullable=True)
    statement_details_extract_extracted_data = Column(JSON, nullable=True)
    statement_details_extract_is_processed = Column(Boolean)
    statement_details_extract_created_at = Column(DateTime(timezone=True))

    # From RefreshToken
    refresh_token_id = Column(Integer)
    refresh_token_user_id = Column(Integer)
    refresh_token_token = Column(String)
    refresh_token_expires_at = Column(DateTime(timezone=True))
    refresh_token_is_revoked = Column(Boolean)
    refresh_token_created_at = Column(DateTime(timezone=True))

    # From Account
    account_id = Column(Integer)
    account_user_id = Column(Integer)
    account_name = Column(String)
    account_type = Column(String)
    account_balance = Column(Float)
    account_currency = Column(String)
    account_created_at = Column(DateTime(timezone=True))
    account_updated_at = Column(DateTime(timezone=True))

    # From Category
    category_id = Column(Integer)
    category_name = Column(String)
    category_type = Column(String)
    category_color = Column(String)
    category_icon = Column(String, nullable=True)
    category_is_default = Column(Boolean)
    category_created_at = Column(DateTime(timezone=True))

    # From Transaction
    transaction_id = Column(Integer)
    transaction_user_id = Column(Integer)
    transaction_account_id = Column(Integer)
    transaction_category_id = Column(Integer, nullable=True)
    transaction_amount = Column(Float)
    transaction_description = Column(String)
    transaction_date = Column(DateTime(timezone=True))
    transaction_type = Column(String)
    transaction_is_recurring = Column(Boolean)
    transaction_recurring_frequency = Column(String, nullable=True)
    transaction_tags = Column(Text, nullable=True)
    transaction_created_at = Column(DateTime(timezone=True))
    transaction_updated_at = Column(DateTime(timezone=True))

    # From Loan
    loan_id = Column(Integer)
    loan_user_id = Column(Integer)
    loan_name = Column(String)
    loan_principal_amount = Column(Float)
    loan_interest_rate = Column(Float)
    loan_term_months = Column(Integer)
    loan_monthly_payment = Column(Float)
    loan_remaining_balance = Column(Float)
    loan_start_date = Column(DateTime(timezone=True))
    loan_end_date = Column(DateTime(timezone=True), nullable=True)
    loan_lender = Column(String)
    loan_loan_type = Column(String)
    loan_status = Column(String)
    loan_created_at = Column(DateTime(timezone=True))
    loan_updated_at = Column(DateTime(timezone=True))

    # From Investment
    investment_id = Column(Integer)
    investment_user_id = Column(Integer)
    investment_name = Column(String)
    investment_type = Column(String)
    investment_symbol = Column(String, nullable=True)
    investment_quantity = Column(Float)
    investment_purchase_price = Column(Float)
    investment_current_price = Column(Float, nullable=True)
    investment_purchase_date = Column(DateTime(timezone=True))
    investment_brokerage = Column(String, nullable=True)
    investment_notes = Column(Text, nullable=True)
    investment_created_at = Column(DateTime(timezone=True))
    investment_updated_at = Column(DateTime(timezone=True))