"""
Configuración base para los tests de la API TZU
"""
import pytest
import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import MagicMock

# CONFIGURACIÓN DE TEST: Set up test environment variables ANTES de importar módulos
# Esto asegura que los módulos se carguen con la configuración correcta
os.environ["DATABASE_URL"] = "sqlite:///./test.db"  # Base de datos de test
os.environ["OPENAI_API_KEY"] = "test-key"           # API key mock para test
os.environ["ENVIRONMENT"] = "test"                  # Marcar entorno de test

# Mock external modules before importing
sys.modules['any_llm'] = MagicMock()

# Import our modules DESPUÉS de configurar el entorno
import models
import database
from api import app
from database import get_db

# CONFIGURACIÓN DE BASE DE DATOS DE TEST
# Crear motor de base de datos específico para tests con SQLite en memoria
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Override database dependency for tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Create test database tables
models.Base.metadata.create_all(bind=test_engine)

# Override dependency in FastAPI app
app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="session")
def test_client():
    """Create test client"""
    return client

@pytest.fixture(scope="function")
def db_session():
    """Create database session for tests"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user"""
    from crud import create_user
    from schemas import UserCreate
    
    user_data = UserCreate(
        username="testuser", 
        email="test@example.com", 
        name="Test User", 
        password="testpassword123"
    )
    user = create_user(db=db_session, user=user_data)
    return user

@pytest.fixture(scope="function")
def auth_headers(test_user):
    """Create authentication headers with valid token"""
    login_data = {
        "username": test_user.username,
        "password": "testpassword123"
    }
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def test_information_system(db_session, test_user):
    """Create a test information system"""
    from crud import create_information_system
    from schemas import InformationSystemBaseCreate
    
    system_data = InformationSystemBaseCreate(
        title="Test System",
        description="A test information system"
    )
    system = create_information_system(db=db_session, information_system=system_data)
    return system

@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up database after each test"""
    yield
    # Clean up test database
    db = TestingSessionLocal()
    try:
        # Delete all records in reverse order of dependencies
        for table in reversed(models.Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error cleaning up database: {e}")
    finally:
        db.close()
