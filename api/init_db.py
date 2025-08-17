import secrets
import string
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import crud
import models
import database
import schemas

def generate_random_password(length=12):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_-+=[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def wait_for_database(max_retries=30, delay=1):
    """Wait until the database is available"""
    for attempt in range(max_retries):
        try:
            db = database.SessionLocal()
            # Try a simple query
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            db.close()
            print(f"✅ Database available after {attempt + 1} attempt(s)")
            return True
        except OperationalError as e:
            print(f"⏳ Attempt {attempt + 1}/{max_retries}: Waiting for database... ({str(e)[:50]}...)")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(delay)
    
    print("❌ Could not connect to database after all attempts")
    return False

def create_default_user(db: Session):
    """Create a default admin user if no user exists"""
    try:
        # Check if any user already exists
        user = db.query(models.User).first()
        if not user:
            # Generate a secure random password
            password = generate_random_password()
            
            # Create admin user
            user_data = schemas.UserCreate(
                username="admin",
                password=password,
                name="Administrator",
                email="admin@example.com"
            )
            
            # Create user using existing function
            user = crud.create_user(db, user_data)
            
            # Display generated password (in production this should go to secure logging)
            print("\n" + "="*50)
            print("DEFAULT USER CREDENTIALS CREATED:")
            print(f"Username: {user_data.username}")
            print(f"Password: {password}")
            print("="*50)
            print("\nPlease change this password after first login.")
            
            return True
        else:
            print("👤 Admin user already exists")
            return False
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        raise

def init_db():
    """Initialize database and create default user"""
    print("🔄 Starting database initialization process...")
    
    # Wait for database to be available
    if not wait_for_database():
        print("❌ Could not establish database connection")
        return False
    
    db = database.SessionLocal()
    try:
        print("👤 Checking existing users...")
        create_default_user(db)
        db.commit()
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        print("✅ Initialization completed")

if __name__ == "__main__":
    init_db()
