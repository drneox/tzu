import secrets
import string
from sqlalchemy.orm import Session
from . import crud, models, database, schemas

def generate_random_password(length=12):
    """Genera una contraseña aleatoria segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_-+=[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def create_default_user(db: Session):
    """Crea un usuario administrador por defecto si no existe ningún usuario"""
    # Verifica si ya existe algún usuario
    user = db.query(models.User).first()
    if not user:
        # Genera una contraseña aleatoria segura
        password = generate_random_password()
        
        # Crea el usuario admin
        user_data = schemas.UserCreate(
            username="admin",
            password=password,
            name="Administrador",
            email="admin@example.com"
        )
        
        # Crea el usuario usando la función existente
        user = crud.create_user(db, user_data)
        
        # Muestra la contraseña generada (en un entorno de producción esto debería ir a un log seguro)
        print("\n" + "="*50)
        print("CREDENCIALES DE USUARIO POR DEFECTO CREADAS:")
        print(f"Usuario: {user_data.username}")
        print(f"Contraseña: {password}")
        print("="*50)
        print("\nPor favor, cambie esta contraseña después de iniciar sesión por primera vez.")
        
        return True
    return False

def init_db():
    """Inicializa la base de datos y crea las tablas y usuario por defecto"""
    # Crear todas las tablas
    models.Base.metadata.create_all(bind=database.engine)
    
    # Crear una sesión
    db = database.SessionLocal()
    try:
        # Crear usuario por defecto
        create_default_user(db)
    finally:
        db.close()
