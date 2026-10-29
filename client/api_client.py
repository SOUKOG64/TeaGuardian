import json
import os

import requests


API_BASE_URL = os.getenv("TEAGUARDIAN_API_BASE_URL", "http://127.0.0.1:8000/api/v1")


class ApiClient:
    def __init__(self, token_store):
        self.token_store = token_store

    def _headers(self):
        token_data = self.token_store.read()
        headers = {"Content-Type": "application/json"}
        if token_data and token_data.get("access_token"):
            headers["Authorization"] = f"Bearer {token_data['access_token']}"
        return headers

    def register(self, name, email, password):
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"name": name, "email": email, "password": password},
            timeout=10,
        )
        data = response.json()
        if response.ok:
            self.token_store.write(data)
        return response, data

    def login(self, email, password):
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=10,
        )
        data = response.json()
        if response.ok:
            self.token_store.write(data)
        return response, data

    def refresh(self):
        token_data = self.token_store.read()
        if not token_data or not token_data.get("refresh_token"):
            return None, {"detail": "No refresh token"}
        response = requests.post(
            f"{API_BASE_URL}/auth/refresh",
            json={"refresh_token": token_data["refresh_token"]},
            timeout=10,
        )
        data = response.json()
        if response.ok:
            self.token_store.write(data)
        return response, data

    def get(self, path):
        response = requests.get(f"{API_BASE_URL}{path}", headers=self._headers(), timeout=10)
        return response, response.json()

    def post(self, path, payload):
        response = requests.post(
            f"{API_BASE_URL}{path}",
            headers=self._headers(),
            json=payload,
            timeout=10,
        )
        return response, response.json()

    def patch(self, path, payload):
        response = requests.patch(
            f"{API_BASE_URL}{path}",
            headers=self._headers(),
            json=payload,
            timeout=10,
        )
        return response, response.json()

    def delete(self, path):
        response = requests.delete(f"{API_BASE_URL}{path}", headers=self._headers(), timeout=10)
        return response, response.json()

    def logout(self):
        self.token_store.clear()
