from fastapi import FastAPI
from api.routes.v1 import auth_routes, user_routes

# tags_metadata = [
#     {"name": "Authentication", "description": "JWT-based user authentication (no OAuth)."},
#     {"name": "User Management", "description": "User profile, account, and settings."},
#     {"name": "Health Check", "description": "Basic API health and status checks."},
# ]

app = FastAPI(
    title="💰 BudgetBrain API - Core Services",
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "BudgetBrain Dev Team",
        "email": "support@budgetbrain.dev",
        "url": "http://www.budgetbrain.dev/support",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ✅ Mount versioned routes
# app.include_router(auth_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")

@app.get("/api/v1/health", tags=["Health Check"])
def health_check():
    return {"isSuccess": True, "message": "API is running", "data": None}
