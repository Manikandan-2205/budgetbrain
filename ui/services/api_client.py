import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

class APIClient:
    """Centralized API client for BudgetBrain UI"""

    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        self._token = None
        self._user = None
        self._token_expires_at = None

    @property
    def token(self) -> Optional[str]:
        """Get current access token"""
        return self._token

    @token.setter
    def token(self, value: str):
        """Set access token and store in session state"""
        self._token = value
        st.session_state.token = value

    @property
    def user(self) -> Optional[Dict[str, Any]]:
        """Get current user info"""
        return self._user

    @user.setter
    def user(self, value: Dict[str, Any]):
        """Set user info and store in session state"""
        self._user = value
        st.session_state.user = value

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle_response(self, response: requests.Response, operation: str) -> Dict[str, Any]:
        """Handle API response with error handling"""
        try:
            if response.status_code == 401:
                # Token expired or invalid
                _logger.warning(f"Authentication failed for {operation}")
                self.logout()
                st.error("Session expired. Please login again.")
                st.rerun()
                return {"success": False, "message": "Authentication required"}

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            _logger.error(f"API request failed for {operation}: {str(e)}")
            return {
                "success": False,
                "message": f"Connection error: {str(e)}",
                "error_code": "CONNECTION_ERROR"
            }
        except json.JSONDecodeError as e:
            _logger.error(f"Invalid JSON response for {operation}: {str(e)}")
            return {
                "success": False,
                "message": "Invalid response from server",
                "error_code": "INVALID_RESPONSE"
            }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        operation = f"{method} {endpoint}"

        try:
            _logger.info(f"Making API request: {operation}")

            # Add headers if not provided
            if 'headers' not in kwargs:
                kwargs['headers'] = self._get_headers()
            elif self.token and 'Authorization' not in kwargs['headers']:
                kwargs['headers']['Authorization'] = f"Bearer {self.token}"

            response = requests.request(method, url, **kwargs)
            return self._handle_response(response, operation)

        except Exception as e:
            _logger.error(f"Unexpected error in {operation}: {str(e)}")
            return {
                "success": False,
                "message": f"Unexpected error: {str(e)}",
                "error_code": "UNEXPECTED_ERROR"
            }

    # Authentication methods
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user and store tokens"""
        data = {"username": username, "password": password}
        response = self._make_request("POST", "/auth/login", json=data)

        if response.get("success"):
            # Store tokens and user info
            token_data = response.get("data", {})
            self.token = token_data.get("access_token")
            self.user = token_data.get("user", {})

            # Cache in browser local storage (via session state)
            st.session_state.authenticated = True
            st.session_state.login_time = datetime.now()

            _logger.info(f"User {username} logged in successfully")

        return response

    def register(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register new user"""
        data = {"username": username, "email": email, "password": password}
        return self._make_request("POST", "/auth/register", json=data)

    def refresh_token(self) -> Dict[str, Any]:
        """Refresh access token"""
        if not st.session_state.get('token'):
            return {"success": False, "message": "No refresh token available"}

        try:
            refresh_token = st.session_state.get('token')  # In real app, you'd store refresh token separately
            data = {"refresh_token": refresh_token}
            response = self._make_request("POST", "/auth/refresh", json=data)

            if response.get("success"):
                token_data = response.get("data", {})
                self.token = token_data.get("access_token")
                _logger.info("Token refreshed successfully")

            return response
        except Exception as e:
            _logger.error(f"Token refresh failed: {str(e)}")
            return {"success": False, "message": "Token refresh failed"}

    def logout(self):
        """Logout user and clear session"""
        try:
            # Call logout endpoint if token exists
            if self.token:
                self._make_request("POST", "/auth/logout", json={"refresh_token": self.token})
        except:
            pass  # Ignore logout endpoint errors

        # Clear local session
        self.token = None
        self.user = None
        self._token_expires_at = None

        # Clear session state
        for key in ['authenticated', 'user', 'token', 'login_time']:
            if key in st.session_state:
                del st.session_state[key]

        _logger.info("User logged out")

    # Transaction methods
    def get_transactions(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """Get user transactions"""
        return self._make_request("GET", f"/transactions/?skip={skip}&limit={limit}")

    def create_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new transaction"""
        return self._make_request("POST", "/transactions/", json=transaction_data)

    def update_transaction(self, transaction_id: int, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing transaction"""
        return self._make_request("PUT", f"/transactions/{transaction_id}", json=transaction_data)

    def delete_transaction(self, transaction_id: int) -> Dict[str, Any]:
        """Delete transaction"""
        return self._make_request("DELETE", f"/transactions/{transaction_id}")

    # Account methods
    def get_accounts(self) -> Dict[str, Any]:
        """Get user accounts"""
        return self._make_request("GET", "/accounts/")

    def create_account(self, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new account"""
        return self._make_request("POST", "/accounts/", json=account_data)

    def update_account(self, account_id: int, account_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update existing account"""
        return self._make_request("PUT", f"/accounts/{account_id}", json=account_data)

    def delete_account(self, account_id: int) -> Dict[str, Any]:
        """Delete account"""
        return self._make_request("DELETE", f"/accounts/{account_id}")

    # Analytics methods
    def get_aggregated_data(self) -> Dict[str, Any]:
        """Get aggregated financial data"""
        return self._make_request("GET", "/aggregated/")

    def get_categories(self) -> Dict[str, Any]:
        """Get transaction categories"""
        return self._make_request("GET", "/categories/")

    # Utility methods
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return (
            self.token is not None and
            self.user is not None and
            st.session_state.get('authenticated', False)
        )

    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        return self.user

    def initialize_from_cache(self):
        """Initialize client from cached session data"""
        if 'token' in st.session_state and 'user' in st.session_state:
            self.token = st.session_state.token
            self.user = st.session_state.user

            # Check if session is still valid (not expired)
            login_time = st.session_state.get('login_time')
            if login_time:
                # Auto refresh if close to expiration (50 minutes for 60-minute tokens)
                time_since_login = datetime.now() - login_time
                if time_since_login > timedelta(minutes=50):
                    _logger.info("Token near expiration, attempting refresh")
                    refresh_result = self.refresh_token()
                    if not refresh_result.get("success"):
                        _logger.warning("Token refresh failed, clearing session")
                        self.logout()

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url.replace('/api', '')}/health", timeout=5)
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "message": "API is healthy" if response.status_code == 200 else "API is not responding"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Cannot connect to API: {str(e)}",
                "error_code": "CONNECTION_ERROR"
            }

# Global API client instance
api_client = APIClient()

def get_api_client() -> APIClient:
    """Get the global API client instance"""
    return api_client

def init_api_client():
    """Initialize API client from cache"""
    api_client.initialize_from_cache()

def require_auth():
    """Decorator to require authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not api_client.is_authenticated():
                st.error("Please login to access this feature")
                st.session_state.current_page = 'login'
                st.rerun()
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator