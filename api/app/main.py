from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from budgetbrain.api.app.core.config import settings
from budgetbrain.api.app.api.routers import (
    auth, accounts, transactions, categories, ml,
    user_details, account_master, money_name_master,
    transaction_master, online_payment_name_master,
    statement_details_extract, aggregated
)
from budgetbrain.api.app.db.session import engine
from budgetbrain.api.app.db.base import Base


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.api_prefix}/auth", tags=["authentication"])
app.include_router(accounts.router, prefix=f"{settings.api_prefix}/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix=f"{settings.api_prefix}/transactions", tags=["transactions"])
app.include_router(categories.router, prefix=f"{settings.api_prefix}/categories", tags=["categories"])
app.include_router(ml.router, prefix=f"{settings.api_prefix}/ml", tags=["machine learning"])

# New master data routers
app.include_router(user_details.router, prefix=f"{settings.api_prefix}/user", tags=["user details"])
app.include_router(account_master.router, prefix=f"{settings.api_prefix}/master", tags=["account master"])
app.include_router(money_name_master.router, prefix=f"{settings.api_prefix}/master", tags=["money name master"])
app.include_router(transaction_master.router, prefix=f"{settings.api_prefix}/master", tags=["transaction master"])
app.include_router(online_payment_name_master.router, prefix=f"{settings.api_prefix}/master", tags=["online payment master"])
app.include_router(statement_details_extract.router, prefix=f"{settings.api_prefix}/extract", tags=["statement extract"])
app.include_router(aggregated.router, prefix=f"{settings.api_prefix}/aggregated", tags=["aggregated data"])


@app.get("/")
def read_root():
    return {"message": "Welcome to BudgetBrain API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
