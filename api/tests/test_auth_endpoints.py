"""
Tests para endpoints de autenticación y usuarios
"""
import pytest
from tests.conftest import client

class TestAuthEndpoints:
    """Tests para autenticación"""
    
    def test_create_user(self):
        """Test crear un nuevo usuario"""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "name": "New User",
            "password": "newpassword123"
        }
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "password" not in data  # No debe devolver la contraseña
    
    def test_create_duplicate_user(self):
        """Test crear usuario duplicado"""
        user_data = {
            "username": "duplicateuser",
            "email": "duplicate@example.com",
            "name": "Duplicate User",
            "password": "password123"
        }
        
        # Crear usuario por primera vez
        response1 = client.post("/users", json=user_data)
        assert response1.status_code == 200
        
        # Intentar crear el mismo usuario otra vez
        response2 = client.post("/users", json=user_data)
        assert response2.status_code == 400
        assert "ya está registrado" in response2.json()["detail"]
    
    def test_login_success(self, test_user):
        """Test login exitoso"""
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
