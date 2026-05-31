"""
Tests for authentication and user endpoints
"""
import pytest
from tests.conftest import client

class TestAuthEndpoints:
    """Tests for authentication"""
    
    def test_create_user(self, admin_auth_headers):
        """Test creating a new user (requires admin)"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "newpassword123"
        }
        response = client.post("/users", json=user_data, headers=admin_auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "password" not in data  # Should not return password
        assert data["role"] == "reader"  # Default role
    
    def test_create_user_without_auth(self):
        """Test creating a user without auth returns 401"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "newpassword123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 401

    def test_create_user_as_reader(self, auth_headers):
        """Test creating a user as reader returns 403"""
        user_data = {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "name": "New User 2",
            "password": "newpassword123"
        }
        response = client.post("/users", json=user_data, headers=auth_headers)
        assert response.status_code == 403
    
    def test_create_duplicate_user(self, admin_auth_headers):
        """Test creating duplicate user (requires admin)"""
        user_data = {
            "username": "duplicateuser",
            "email": "duplicate@example.com",
            "name": "Duplicate User",
            "password": "password123"
        }
        
        # Create user for the first time
        response1 = client.post("/users", json=user_data, headers=admin_auth_headers)
        assert response1.status_code == 200
        
        # Try to create the same user again
        response2 = client.post("/users", json=user_data, headers=admin_auth_headers)
        assert response2.status_code == 400
        assert "already registered" in response2.json()["detail"]
    
    def test_login_success(self, test_user):
        """Test successful login"""
        login_data = {
            "username": test_user.username,
            "password": "testpassword123"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, test_user):
        """Test login con contraseña incorrecta"""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self):
        """Test login con usuario que no existe"""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 401
    
    def test_get_current_user(self, auth_headers):
        """Test obtener usuario actual autenticado"""
        response = client.get("/users/me", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "username" in data
        assert "id" in data
    
    def test_get_current_user_without_auth(self):
        """Test obtener usuario actual sin autenticación"""
        response = client.get("/users/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self):
        """Test obtener usuario actual con token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401
