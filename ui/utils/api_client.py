import requests
import streamlit as st
import os
from typing import Optional, Dict, List, Any


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.token: Optional[str] = st.session_state.get('token')

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Optional[Dict]:
        url = f"{self.base_url}{endpoint}"

        try:
            if files:
                # For file uploads, don't set Content-Type to let requests handle it
                headers = {}
                if self.token:
                    headers["Authorization"] = f"Bearer {self.token}"
                response = requests.request(method, url, files=files, data=data, headers=headers)
            else:
                response = requests.request(method, url, json=data, headers=self._get_headers())

            if response.status_code == 200:
                return response.json() if response.content else None
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
        except requests.RequestException as e:
            st.error(f"Request failed: {str(e)}")
            return None

    def login(self, username: str, password: str) -> bool:
        data = {"username": username, "password": password}
        response = self._make_request("POST", "/auth/login", data)

        if response and "access_token" in response:
            self.token = response["access_token"]
            st.session_state.token = self.token
            st.session_state.username = username
            st.session_state.authenticated = True
            return True
        return False

    def register(self, username: str, email: str, password: str) -> bool:
        data = {"username": username, "email": email, "password": password}
        response = self._make_request("POST", "/auth/register", data)
        return response is not None

    def get_transactions(self, limit: int = 100, skip: int = 0) -> Optional[List[Dict]]:
        params = f"?limit={limit}&skip={skip}"
        return self._make_request("GET", f"/transactions{params}")

    def add_transaction(self, amount: float, description: str, transaction_type: str,
                       date: str, category_id: int, account_id: int = 1) -> bool:
        data = {
            "amount": amount,
            "description": description,
            "type": transaction_type,
            "date": date.isoformat() if hasattr(date, 'isoformat') else str(date),
            "category_id": category_id,
            "account_id": account_id
        }
        response = self._make_request("POST", "/transactions", data)
        return response is not None

    def get_accounts(self) -> Optional[List[Dict]]:
        return self._make_request("GET", "/accounts")

    def add_account(self, name: str, account_type: str, balance: float = 0.0) -> bool:
        data = {
            "name": name,
            "type": account_type,
            "balance": balance
        }
        response = self._make_request("POST", "/accounts", data)
        return response is not None

    def get_categories(self) -> Optional[List[Dict]]:
        return self._make_request("GET", "/categories")

    def get_ai_suggestions(self, description: str, amount: float, transaction_type: str) -> Optional[Dict]:
        data = {
            "description": description,
            "amount": amount,
            "type": transaction_type
        }
        return self._make_request("POST", "/ml/suggestions", data)

    def upload_bank_statement(self, file) -> Optional[Dict]:
        files = {"file": (file.name, file, file.type)}
        return self._make_request("POST", "/ml/upload-statement", files=files)

    def get_user_profile(self) -> Optional[Dict]:
        return self._make_request("GET", "/auth/me")

    def update_user_profile(self, data: Dict) -> bool:
        response = self._make_request("PUT", "/auth/me", data)
        return response is not None
