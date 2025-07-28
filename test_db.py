#!/usr/bin/env python3
"""
Database and Authentication Test Script
This script tests the database initialization and authentication functionality.
"""

import sqlite3
import sys
import os
import asyncio
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append('.')

from app.core.database import create_tables, SessionLocal, engine
from app.core.config import settings
from app.api.auth import create_user, authenticate_user
from app.models.user import User, UserCreate, UserRole

def test_database_connection():
    """Test database connection and table creation"""
    print("🔧 Testing database connection...")
    
    try:
        # Create tables
        create_tables()
        print("✅ Database tables created successfully")
        
        # Check if tables exist using SQLite directly
        conn = sqlite3.connect('docbot.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        print(f"📊 Tables found: {[table[0] for table in tables]}")
        
        if not tables:
            print("❌ No tables found in database!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def test_user_operations():
    """Test user creation and authentication"""
    print("\n👤 Testing user operations...")
    
    db = SessionLocal()
    try:
        # Test user creation
        test_user = UserCreate(
            email="test@example.com",
            username="testuser",
            password="testpassword123",
            role=UserRole.USER
        )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == test_user.username).first()
        if existing_user:
            print("ℹ️ Test user already exists, deleting...")
            db.delete(existing_user)
            db.commit()
        
        # Create user
        new_user = create_user(db, test_user)
        print(f"✅ User created: {new_user.username} (ID: {new_user.id})")
        
        # Test authentication
        auth_user, error = authenticate_user(db, test_user.username, test_user.password)
        if auth_user:
            print(f"✅ Authentication successful for user: {auth_user.username}")
        else:
            print(f"❌ Authentication failed: {error}")
            return False
            
        # Test wrong password
        auth_user, error = authenticate_user(db, test_user.username, "wrongpassword")
        if not auth_user:
            print(f"✅ Authentication correctly failed for wrong password: {error}")
        else:
            print("❌ Authentication should have failed for wrong password!")
            
        return True
        
    except Exception as e:
        print(f"❌ User operations failed: {str(e)}")
        return False
    finally:
        db.close()

def test_database_content():
    """Check database content"""
    print("\n📋 Checking database content...")
    
    try:
        conn = sqlite3.connect('docbot.db')
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute("SELECT id, username, email, role FROM users;")
        users = cursor.fetchall()
        print(f"👥 Users in database ({len(users)}):")
        for user in users:
            print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")
            
        # Check documents table
        cursor.execute("SELECT id, filename, uploader_id FROM documents;")
        documents = cursor.fetchall()
        print(f"📄 Documents in database ({len(documents)}):")
        for doc in documents:
            print(f"  - ID: {doc[0]}, Filename: {doc[1]}, Uploader: {doc[2]}")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database content check failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Database and Authentication Tests")
    print(f"📍 Database URL: {settings.DATABASE_URL}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    # Test database
    db_ok = test_database_connection()
    
    if db_ok:
        # Test user operations
        user_ok = test_user_operations()
        
        # Check database content
        content_ok = test_database_content()
        
        if db_ok and user_ok and content_ok:
            print("\n✅ All tests passed! Database and authentication are working correctly.")
            return True
        else:
            print("\n❌ Some tests failed. Check the errors above.")
            return False
    else:
        print("\n❌ Database connection failed. Cannot proceed with other tests.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 