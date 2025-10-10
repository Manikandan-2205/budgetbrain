from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from db.session import Base, engine
from api.routes import auth_routes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


tags_metadata = [
    {
        "name": "Authentication",
        "description": "User registration and JWT token generation (Login).",
    },
    {
        "name": "Health Check",
        "description": "Basic API health and status checks.",
    },
]


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


app.include_router(auth_routes.router)


@app.get(
    "/",
    tags=["Health Check"],
    summary="API Health Status",
    description="Returns a simple JSON message indicating the API service is operational.",
)
def root():
    return {"message": "Welcome to BudgetBrain API 🚀"}
