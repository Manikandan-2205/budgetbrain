from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import auth, accounts, transactions, categories, ml
from app.db.session import engine
from app.db.models import Base


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


@app.get("/")
def read_root():
    return {"message": "Welcome to BudgetBrain API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
