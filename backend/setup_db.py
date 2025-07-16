#!/usr/bin/env python3
"""
Database setup script for Plant Health Monitoring API
Uses credentials from .env file
"""
import asyncio
import asyncpg
import sys
from app.core.config import settings

async def setup_database():
    """Setup PostgreSQL database and user for the application"""
    
    # Try to connect with admin credentials from .env
    print(f"Trying to connect as admin user: {settings.POSTGRES_ADMIN_USER}")
    
    conn = None
    try:
        conn = await asyncpg.connect(settings.ADMIN_DATABASE_URL)
        print("✅ Connected to PostgreSQL with admin credentials!")
    except Exception as e:
        print(f"❌ Failed to connect with admin credentials: {e}")
        print(f"Make sure the admin password '{settings.POSTGRES_ADMIN_PASSWORD}' is correct in .env file")
    
    if not conn:
        print("\n❌ Could not connect to PostgreSQL with common credentials.")
        print("Please ensure PostgreSQL is running and you know the postgres user password.")
        print("You can also run these SQL commands manually:")
        print_manual_setup()
        return False
    
    try:
        # Create database
        try:
            await conn.execute(f"CREATE DATABASE {settings.DB_NAME};")
            print(f"✅ Created database '{settings.DB_NAME}'")
        except asyncpg.DuplicateDatabaseError:
            print(f"ℹ️  Database '{settings.DB_NAME}' already exists")
        except Exception as e:
            print(f"⚠️  Database creation: {e}")
        
        # Create user
        try:
            await conn.execute(f"CREATE USER {settings.DB_USER} WITH PASSWORD '{settings.DB_PASSWORD}';")
            print(f"✅ Created user '{settings.DB_USER}'")
        except asyncpg.DuplicateObjectError:
            print(f"ℹ️  User '{settings.DB_USER}' already exists")
        except Exception as e:
            print(f"⚠️  User creation: {e}")
        
        # Grant privileges
        await conn.execute(f"GRANT ALL PRIVILEGES ON DATABASE {settings.DB_NAME} TO {settings.DB_USER};")
        await conn.execute(f"ALTER USER {settings.DB_USER} CREATEDB;")
        print(f"✅ Granted privileges to '{settings.DB_USER}'")
        
        # Connect to the new database and grant schema privileges
        await conn.close()
        
        # Try to connect to the app database with app user
        try:
            test_conn = await asyncpg.connect(settings.DATABASE_URL)
            print(f"✅ Successfully connected as {settings.DB_USER} to {settings.DB_NAME}")
            await test_conn.close()
            return True
        except Exception as e:
            print(f"⚠️  Test connection failed: {e}")
            print("Database setup completed but connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False
    finally:
        if conn:
            await conn.close()

def print_manual_setup():
    """Print manual setup instructions"""
    print("\nManual setup SQL commands:")
    print(f"CREATE DATABASE {settings.DB_NAME};")
    print(f"CREATE USER {settings.DB_USER} WITH PASSWORD '{settings.DB_PASSWORD}';")
    print(f"GRANT ALL PRIVILEGES ON DATABASE {settings.DB_NAME} TO {settings.DB_USER};")
    print(f"\\c {settings.DB_NAME}")
    print(f"GRANT ALL ON SCHEMA public TO {settings.DB_USER};")

if __name__ == "__main__":
    success = asyncio.run(setup_database())
    if success:
        print("\n🌱 Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed. Please check the manual setup instructions above.")
        sys.exit(1)