"""
Tests de integración para flujos completos de la aplicación
"""
import pytest
from tests.conftest import client

class TestIntegrationFlows:
    """Tests de integración para flujos completos"""
    
    def test_complete_user_system_workflow(self, admin_auth_headers):
        """Test flujo completo: crear usuario, login, crear sistema, evaluar"""
        # 1. Crear usuario analista (requiere admin)
        user_data = {
            "username": "integrationuser",
            "email": "integration@example.com",
            "name": "Integration User",
            "password": "integration123",
            "role": "analyst"
        }
        user_response = client.post("/users", json=user_data, headers=admin_auth_headers)
        assert user_response.status_code == 200
        
        # 2. Login
        login_data = {"username": "integrationuser", "password": "integration123"}
        token_response = client.post("/token", data=login_data)
        assert token_response.status_code == 200
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Verificar usuario actual
        me_response = client.get("/users/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "integrationuser"
        
        # 4. Crear sistema de información
        system_data = {"title": "Sistema Integración", "description": "Sistema para test de integración"}
        system_response = client.post("/new", json=system_data, headers=headers)
        assert system_response.status_code == 200
        system_id = system_response.json()["id"]
        
        # 5. Obtener lista de sistemas y verificar que aparece
        systems_response = client.get("/information_systems", headers=headers)
        assert systems_response.status_code == 200
        system_titles = [s["title"] for s in systems_response.json()]
        assert "Sistema Integración" in system_titles
        
        # 6. Crear amenaza para el sistema
        threat_data = {"title": "Amenaza Integración", "type": "Malware", "description": "Amenaza para test de integración"}
        threat_response = client.post(f"/information_systems/{system_id}/threats", json=threat_data, headers=headers)
        assert threat_response.status_code == 200
        
        # 7. Evaluar el sistema
        evaluate_response = client.post(f"/evaluate/{system_id}", headers=headers)
        assert evaluate_response.status_code in [200, 422]
    
    def test_authentication_flow(self, admin_auth_headers):
        """Test flujo de autenticación completo"""
        # 1. Acceso sin autenticación debe fallar
        response = client.get("/users/me")
        assert response.status_code == 401
        
        # 2. Crear usuario (requiere admin)
        user_data = {"username": "authuser", "email": "authuser@example.com", "name": "Auth User", "password": "authpass123"}
        client.post("/users", json=user_data, headers=admin_auth_headers)
        
        # 3. Login con credenciales correctas
        token_response = client.post("/token", data={"username": "authuser", "password": "authpass123"})
        assert token_response.status_code == 200
        
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 4. Acceso con token válido debe funcionar
        me_response = client.get("/users/me", headers=headers)
        assert me_response.status_code == 200
        
        # 5. Acceso con token inválido debe fallar
        invalid_response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
        assert invalid_response.status_code == 401
    
    def test_crud_operations_flow(self, admin_auth_headers):
        """Test flujo CRUD completo para sistemas de información"""
        # Setup: crear usuario analista y obtener token
        user_data = {"username": "cruduser", "email": "crud@example.com", "name": "CRUD User", "password": "crud123", "role": "analyst"}
        client.post("/users", json=user_data, headers=admin_auth_headers)
        
        token_response = client.post("/token", data={"username": "cruduser", "password": "crud123"})
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # CREATE
        create_response = client.post("/new", json={"title": "Sistema CRUD", "description": "Para test CRUD"}, headers=headers)
        assert create_response.status_code == 200
        system_id = create_response.json()["id"]
        
        # READ
        read_response = client.get(f"/information_systems/{system_id}", headers=headers)
        assert read_response.status_code == 200
        assert read_response.json()["title"] == "Sistema CRUD"
        
        # UPDATE
        update_response = client.put(f"/information_systems/{system_id}", json={"title": "Sistema CRUD Actualizado", "description": "Desc actualizada"}, headers=headers)
        assert update_response.status_code in [200, 405]
        
        # DELETE: Analyst can delete own systems
        delete_response = client.delete(f"/information_systems/{system_id}", headers=headers)
        assert delete_response.status_code in [200, 405]
        
        if delete_response.status_code == 200:
            get_deleted_response = client.get(f"/information_systems/{system_id}", headers=headers)
            assert get_deleted_response.status_code == 404
    
    def test_threat_management_flow(self, admin_auth_headers):
        """Test flujo completo de gestión de amenazas"""
        # Setup: usuario analista
        user_data = {"username": "threatuser", "email": "threat@example.com", "name": "Threat User", "password": "threat123", "role": "analyst"}
        client.post("/users", json=user_data, headers=admin_auth_headers)
        
        token_response = client.post("/token", data={"username": "threatuser", "password": "threat123"})
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Crear sistema
        system_response = client.post("/new", json={"title": "Sistema Amenazas", "description": "Para gestión de amenazas"}, headers=headers)
        assert system_response.status_code == 200
        system_id = system_response.json()["id"]
        
        # Crear múltiples amenazas
        threats_data = [
            {"title": "SQL Injection", "type": "Injection", "description": "Ataque SQL"},
            {"title": "Cross-Site Scripting", "type": "Injection", "description": "Ataque XSS"},
            {"title": "Brute Force", "type": "Authentication", "description": "Ataque fuerza bruta"},
        ]
        
        created_threats = []
        for threat_data in threats_data:
            response = client.post(f"/information_systems/{system_id}/threats", json=threat_data, headers=headers)
            assert response.status_code == 200
            created_threats.append(response.json())
        
        # Verificar que se crearon todas las amenazas
        threats_response = client.get(f"/information_systems/{system_id}/threats", headers=headers)
        assert threats_response.status_code == 200
        threat_titles = [t["title"] for t in threats_response.json()]
        assert "SQL Injection" in threat_titles
        assert "Cross-Site Scripting" in threat_titles
        assert "Brute Force" in threat_titles
        
        # Actualizar una amenaza
        update_response = client.put(f"/threat/{created_threats[0]['id']}/risk", json={"impact": "High", "probability": "High", "risk_level": "Critical"}, headers=headers)
        assert update_response.status_code == 200
        
        # Analyst puede eliminar amenazas que creó
        delete_response = client.delete(f"/threat/{created_threats[1]['id']}", headers=headers)
        assert delete_response.status_code == 200
    
    def test_error_handling_flow(self, admin_auth_headers):
        """Test manejo de errores en flujos típicos"""
        # Setup básico: usuario analista
        user_data = {"username": "erroruser", "email": "error@example.com", "name": "Error User", "password": "error123", "role": "analyst"}
        client.post("/users", json=user_data, headers=admin_auth_headers)
        
        token_response = client.post("/token", data={"username": "erroruser", "password": "error123"})
        token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Error 404
        not_found_response = client.get("/information_systems/00000000-0000-0000-0000-000000000000", headers=headers)
        assert not_found_response.status_code == 404
        
        # Error 401
        unauth_response = client.get("/information_systems")
        assert unauth_response.status_code == 401
        
        # Error 400: usuario duplicado
        duplicate_response = client.post("/users", json={"username": "erroruser", "email": "error2@example.com", "name": "Error User 2", "password": "different123"}, headers=admin_auth_headers)
        assert duplicate_response.status_code == 400
        
        # Error 422: datos inválidos
        invalid_response = client.post("/new", json={"description": "Sin título"}, headers=headers)
        assert invalid_response.status_code in [422, 400]
