#!/usr/bin/env python3
"""
Health check script for backend
"""
import sys
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os

def check_database_health():
    """Check that database is available and has necessary tables"""
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            print("❌ DATABASE_URL is not defined")
            return False
        
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            # Verify basic connection
            result = conn.execute(text("SELECT 1"))
            if not result.fetchone():
                print("❌ Cannot execute basic queries")
                return False
            
            # Verify that main tables exist
            required_tables = ['users', 'risks', 'threats', 'information_systems']
            for table in required_tables:
                result = conn.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema='public' AND table_name='{table}'
                """))
                if not result.fetchone():
                    print(f"❌ Required table '{table}' does not exist")
                    return False
            
            print("✅ Database is healthy")
            return True
            
    except OperationalError as e:
        print(f"❌ Database connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Checking system health...")
    
    if check_database_health():
        print("✅ All checks passed")
        sys.exit(0)
    else:
        print("❌ Some checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
