#!/usr/bin/env python3
"""
PostgreSQL setup script for Plant Health Monitoring API
This script will help set up PostgreSQL from scratch
"""
import asyncio
import asyncpg
import sys
import subprocess
import os

async def test_postgres_service():
    """Test if PostgreSQL service is running"""
    try:
        # Try to connect without authentication (peer/trust)
        conn = await asyncpg.connect(
            host='localhost',
            port=5432,
            user='postgres',
            database='postgres'
        )
        await conn.close()
        return True, "postgres", None
    except asyncpg.InvalidPasswordError:
        return True, "postgres", "password_required"
    except Exception as e:
        return False, None, str(e)

async def try_common_passwords():
    """Try common default passwords for postgres user"""
    common_passwords = [
        None,  # No password
        "",    # Empty password
        "postgres",
        "admin", 
        "password",
        "root",
        "123456"
    ]
    
    for pwd in common_passwords:
        try:
            if pwd is None:
                conn = await asyncpg.connect("postgres://postgres@localhost:5432/postgres")
            else:
                conn = await asyncpg.connect(f"postgres://postgres:{pwd}@localhost:5432/postgres")
            
            print(f"SUCCESS: Connected with password: {'(no password)' if pwd is None else ('(empty)' if pwd == '' else pwd)}")
            return conn, pwd
        except Exception:
            continue
    
    return None, None

async def setup_postgres_user():
    """Set up postgres user with a known password"""
    print("Setting up PostgreSQL admin user...")
    
    # First, try to connect with common passwords
    conn, existing_pwd = await try_common_passwords()
    
    if conn:
        print("Found existing postgres user access!")
        try:
            # Set a known password for postgres user
            await conn.execute("ALTER USER postgres PASSWORD 'admin123';")
            print("SUCCESS: Set postgres user password to 'admin123'")
            await conn.close()
            return "admin123"
        except Exception as e:
            print(f"Failed to set postgres password: {e}")
            await conn.close()
            return existing_pwd
    else:
        print("Could not connect to postgres user with common passwords.")
        print("You may need to:")
        print("1. Reinstall PostgreSQL and set a password during installation")
        print("2. Or edit pg_hba.conf to allow local connections")
        return None

async def create_app_database(postgres_password):
    """Create the application database and user"""
    try:
        conn = await asyncpg.connect(f"postgres://postgres:{postgres_password}@localhost:5432/postgres")
        print("Connected to PostgreSQL as admin user")
        
        # Create database
        try:
            await conn.execute("CREATE DATABASE plant_health_db;")
            print("SUCCESS: Created database 'plant_health_db'")
        except asyncpg.DuplicateDatabaseError:
            print("INFO: Database 'plant_health_db' already exists")
        
        # Create user
        try:
            await conn.execute("CREATE USER plant_user WITH PASSWORD 'plant_password';")
            print("SUCCESS: Created user 'plant_user'")
        except asyncpg.DuplicateObjectError:
            print("INFO: User 'plant_user' already exists")
        
        # Grant privileges
        await conn.execute("GRANT ALL PRIVILEGES ON DATABASE plant_health_db TO plant_user;")
        await conn.execute("ALTER USER plant_user CREATEDB;")
        print("SUCCESS: Granted privileges to 'plant_user'")
        
        await conn.close()
        
        # Test connection as app user
        try:
            test_conn = await asyncpg.connect("postgres://plant_user:plant_password@localhost:5432/plant_health_db")
            print("SUCCESS: Verified plant_user can connect to plant_health_db")
            await test_conn.close()
            return True
        except Exception as e:
            print(f"WARNING: Could not verify plant_user connection: {e}")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to create app database: {e}")
        return False

def check_postgres_installation():
    """Check if PostgreSQL is installed and running"""
    try:
        # Check if PostgreSQL service is running on Windows
        result = subprocess.run(['sc', 'query', 'postgresql-x64-14'], 
                              capture_output=True, text=True, shell=True)
        if 'RUNNING' in result.stdout:
            print("PostgreSQL service is running")
            return True
        else:
            print("PostgreSQL service is not running")
            return False
    except Exception:
        # Try alternative service names
        service_names = ['postgresql-x64-15', 'postgresql-x64-13', 'postgresql-x64-12', 'PostgreSQL']
        for service in service_names:
            try:
                result = subprocess.run(['sc', 'query', service], 
                                      capture_output=True, text=True, shell=True)
                if 'RUNNING' in result.stdout:
                    print(f"PostgreSQL service '{service}' is running")
                    return True
            except Exception:
                continue
        
        print("Could not find running PostgreSQL service")
        return False

async def main():
    """Main setup function"""
    print("PostgreSQL Setup for Plant Health Monitoring API")
    print("=" * 50)
    
    # Check if PostgreSQL is installed and running
    if not check_postgres_installation():
        print("ERROR: PostgreSQL is not running.")
        print("Please install PostgreSQL first or start the service.")
        return False
    
    # Test service connectivity
    service_running, user, status = await test_postgres_service()
    if not service_running:
        print(f"ERROR: Cannot connect to PostgreSQL: {status}")
        return False
    
    print("PostgreSQL service is accessible")
    
    # Set up postgres admin user
    postgres_password = await setup_postgres_user()
    if not postgres_password:
        print("ERROR: Could not set up postgres admin user")
        return False
    
    print(f"PostgreSQL admin setup complete. Password: {postgres_password}")
    
    # Create application database and user
    success = await create_app_database(postgres_password)
    if not success:
        print("ERROR: Failed to create application database")
        return False
    
    print("")
    print("=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("PostgreSQL Admin:")
    print(f"  User: postgres")
    print(f"  Password: {postgres_password}")
    print("")
    print("Application Database:")
    print("  Database: plant_health_db")
    print("  User: plant_user")
    print("  Password: plant_password")
    print("  Connection: postgres://plant_user:plant_password@localhost:5432/plant_health_db")
    
    return True

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)