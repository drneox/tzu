#!/usr/bin/env python3
"""
Utility script to show the current admin credentials.
This script is used by Docker containers to display login information.
"""

import sys
import os
import secrets
import string
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

# Add the api directory to the path to import modules
sys.path.insert(0, '/app')

try:
    import crud
    import models
    import database
    import schemas
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def generate_random_password(length=12):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_-+=[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def get_or_update_admin_credentials():
    """Get existing admin credentials or update them with a new password"""
    try:
        db = database.SessionLocal()
        try:
            # Get the admin user
            admin_user = crud.get_user_by_username(db, "admin")
            
            if admin_user:
                # Generate a new password
                new_password = generate_random_password()
                
                # Update the password
                hashed_password = crud.get_password_hash(new_password)
                admin_user.password_hash = hashed_password
                db.commit()
                
                return {
                    "username": admin_user.username,
                    "password": new_password,
                    "email": admin_user.email,
                    "name": admin_user.name,
                    "updated": True
                }
            else:
                # Create new admin user if doesn't exist
                password = generate_random_password()
                
                user_data = schemas.UserCreate(
                    username="admin",
                    password=password,
                    name="Administrator", 
                    email="admin@example.com"
                )
                
                user = crud.create_user(db, user_data)
                db.commit()
                
                return {
                    "username": user.username,
                    "password": password,
                    "email": user.email,
                    "name": user.name,
                    "updated": False
                }
                
        finally:
            db.close()
            
    except OperationalError:
        print("❌ Could not connect to database. Make sure PostgreSQL is running.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    """Main function to display credentials"""
    try:
        credentials = get_or_update_admin_credentials()
        
        print()
        print("=" * 60)
        if credentials["updated"]:
            print("🔐 UPDATED USER CREDENTIALS:")
        else:
            print("🔐 NEW USER CREDENTIALS:")
        print("=" * 60)
        print(f"👤 Username: {credentials['username']}")
        print(f"🔑 Password: {credentials['password']}")
        print("=" * 60)
        print("⚠️  IMPORTANT: Save these credentials in a safe place!")
        print("🔄 You can change the password after logging in.")
        print("=" * 60)
        print()
        
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
