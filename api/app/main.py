from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.config import settings
from app.api.routers import (
    auth, accounts, transactions, categories, ml,
    user_details, account_master, money_name_master,
    transaction_master, online_payment_name_master,
    statement_details_extract, aggregated
)
from app.db.session import engine
from app.db.base import Base
from app.middleware.performance_middleware import (
    PerformanceMonitoringMiddleware,
    RequestCachingMiddleware,
    RateLimitingMiddleware,
    ExceptionHandlingMiddleware
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    swagger_ui_parameters={
        "docExpansion": "none",  # Collapse all operations by default
        "defaultModelsExpandDepth": -1,  # Collapse models by default
    }
)

# Performance and monitoring middleware (order matters)
app.add_middleware(ExceptionHandlingMiddleware)
app.add_middleware(PerformanceMonitoringMiddleware)
app.add_middleware(RequestCachingMiddleware, cache_timeout=300)  # 5 minutes
app.add_middleware(RateLimitingMiddleware, requests_per_minute=100)  # 100 req/min

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
    from app.core.performance import get_performance_monitor
    from app.core.exceptions import create_success_response

    # Get system stats
    monitor = get_performance_monitor()
    system_stats = monitor.get_system_stats()
    metrics_summary = monitor.get_metrics_summary()

    return create_success_response("System is healthy", {
        "status": "healthy",
        "system": system_stats,
        "metrics": metrics_summary,
        "timestamp": "2025-10-20T08:42:47.976Z"
    })

@app.get("/performance")
def performance_metrics():
    """Get detailed performance metrics"""
    from app.core.performance import get_performance_monitor
    from app.core.exceptions import create_success_response

    monitor = get_performance_monitor()
    return create_success_response("Performance metrics retrieved", {
        "metrics": monitor.get_metrics_summary(),
        "system": monitor.get_system_stats()
    })
