from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class AggregatedBase(BaseModel):
    # From User
    user_id: int
    user_email: str
    user_username: str
    user_hashed_password: str
    user_is_active: bool
    user_created_at: datetime
    user_updated_at: Optional[datetime] = None

    # From UserDetails
    user_details_id: Optional[int] = None
    user_details_user_id: Optional[int] = None
    user_details_first_name: Optional[str] = None
    user_details_last_name: Optional[str] = None
    user_details_phone: Optional[str] = None
    user_details_address: Optional[str] = None
    user_details_date_of_birth: Optional[datetime] = None
    user_details_profile_picture: Optional[str] = None
    user_details_created_at: Optional[datetime] = None
    user_details_updated_at: Optional[datetime] = None

    # From AccountMaster
    account_master_id: Optional[int] = None
    account_master_user_id: Optional[int] = None
    account_master_account_name: Optional[str] = None
    account_master_account_type: Optional[str] = None
    account_master_bank_name: Optional[str] = None
    account_master_account_number: Optional[str] = None
    account_master_balance: Optional[float] = None
    account_master_currency: Optional[str] = None
    account_master_is_active: Optional[bool] = None
    account_master_created_at: Optional[datetime] = None
    account_master_updated_at: Optional[datetime] = None

    # From MoneyNameMaster
    money_name_master_id: Optional[int] = None
    money_name_master_user_id: Optional[int] = None
    money_name_master_name: Optional[str] = None
    money_name_master_type: Optional[str] = None
    money_name_master_category: Optional[str] = None
    money_name_master_is_default: Optional[bool] = None
    money_name_master_created_at: Optional[datetime] = None

    # From TransactionMaster
    transaction_master_id: Optional[int] = None
    transaction_master_user_id: Optional[int] = None
    transaction_master_account_id: Optional[int] = None
    transaction_master_money_name_id: Optional[int] = None
    transaction_master_amount: Optional[float] = None
    transaction_master_description: Optional[str] = None
    transaction_master_transaction_date: Optional[datetime] = None
    transaction_master_transaction_type: Optional[str] = None
    transaction_master_payment_method: Optional[str] = None
    transaction_master_tags: Optional[Any] = None
    transaction_master_is_recurring: Optional[bool] = None
    transaction_master_recurring_frequency: Optional[str] = None
    transaction_master_created_at: Optional[datetime] = None
    transaction_master_updated_at: Optional[datetime] = None

    # From OnlinePaymentNameMaster
    online_payment_name_master_id: Optional[int] = None
    online_payment_name_master_user_id: Optional[int] = None
    online_payment_name_master_payment_name: Optional[str] = None
    online_payment_name_master_provider: Optional[str] = None
    online_payment_name_master_account_email: Optional[str] = None
    online_payment_name_master_is_active: Optional[bool] = None
    online_payment_name_master_created_at: Optional[datetime] = None
    online_payment_name_master_updated_at: Optional[datetime] = None

    # From StatementDetailsExtract
    statement_details_extract_id: Optional[int] = None
    statement_details_extract_user_id: Optional[int] = None
    statement_details_extract_account_id: Optional[int] = None
    statement_details_extract_statement_date: Optional[datetime] = None
    statement_details_extract_transaction_date: Optional[datetime] = None
    statement_details_extract_description: Optional[str] = None
    statement_details_extract_amount: Optional[float] = None
    statement_details_extract_balance: Optional[float] = None
    statement_details_extract_category: Optional[str] = None
    statement_details_extract_extracted_data: Optional[Any] = None
    statement_details_extract_is_processed: Optional[bool] = None
    statement_details_extract_created_at: Optional[datetime] = None

    # From RefreshToken
    refresh_token_id: Optional[int] = None
    refresh_token_user_id: Optional[int] = None
    refresh_token_token: Optional[str] = None
    refresh_token_expires_at: Optional[datetime] = None
    refresh_token_is_revoked: Optional[bool] = None
    refresh_token_created_at: Optional[datetime] = None

    # From Account
    account_id: Optional[int] = None
    account_user_id: Optional[int] = None
    account_name: Optional[str] = None
    account_type: Optional[str] = None
    account_balance: Optional[float] = None
    account_currency: Optional[str] = None
    account_created_at: Optional[datetime] = None
    account_updated_at: Optional[datetime] = None

    # From Category
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    category_type: Optional[str] = None
    category_color: Optional[str] = None
    category_icon: Optional[str] = None
    category_is_default: Optional[bool] = None
    category_created_at: Optional[datetime] = None

    # From Transaction
    transaction_id: Optional[int] = None
    transaction_user_id: Optional[int] = None
    transaction_account_id: Optional[int] = None
    transaction_category_id: Optional[int] = None
    transaction_amount: Optional[float] = None
    transaction_description: Optional[str] = None
    transaction_date: Optional[datetime] = None
    transaction_type: Optional[str] = None
    transaction_is_recurring: Optional[bool] = None
    transaction_recurring_frequency: Optional[str] = None
    transaction_tags: Optional[str] = None
    transaction_created_at: Optional[datetime] = None
    transaction_updated_at: Optional[datetime] = None

    # From Loan
    loan_id: Optional[int] = None
    loan_user_id: Optional[int] = None
    loan_name: Optional[str] = None
    loan_principal_amount: Optional[float] = None
    loan_interest_rate: Optional[float] = None
    loan_term_months: Optional[int] = None
    loan_monthly_payment: Optional[float] = None
    loan_remaining_balance: Optional[float] = None
    loan_start_date: Optional[datetime] = None
    loan_end_date: Optional[datetime] = None
    loan_lender: Optional[str] = None
    loan_loan_type: Optional[str] = None
    loan_status: Optional[str] = None
    loan_created_at: Optional[datetime] = None
    loan_updated_at: Optional[datetime] = None

    # From Investment
    investment_id: Optional[int] = None
    investment_user_id: Optional[int] = None
    investment_name: Optional[str] = None
    investment_type: Optional[str] = None
    investment_symbol: Optional[str] = None
    investment_quantity: Optional[float] = None
    investment_purchase_price: Optional[float] = None
    investment_current_price: Optional[float] = None
    investment_purchase_date: Optional[datetime] = None
    investment_brokerage: Optional[str] = None
    investment_notes: Optional[str] = None
    investment_created_at: Optional[datetime] = None
    investment_updated_at: Optional[datetime] = None


class AggregatedCreate(AggregatedBase):
    pass


class AggregatedUpdate(AggregatedBase):
    pass


class Aggregated(AggregatedBase):
    id: int

    class Config:
        orm_mode = True