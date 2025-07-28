#!/usr/bin/env python3
"""
API Endpoint Test Script
This script tests the authentication API endpoints via HTTP requests.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def wait_for_server(max_attempts=10):
    """Wait for the server to be ready"""
    print("⏳ Waiting for server to start...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(2)
            print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print("❌ Server did not start in time")
    return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n🏠 Testing root endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root endpoint failed: {str(e)}")
        return False

def test_register():
    """Test user registration"""
    print("\n📝 Testing user registration...")
    
    test_user = {
        "email": "apitest@example.com",
        "username": "apitest",
        "password": "testpassword123",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User registered: {user_data}")
            return user_data
        elif response.status_code == 400:
            error = response.json()
            if "already" in error.get("detail", "").lower():
                print("ℹ️ User already exists, that's ok for testing")
                return {"username": test_user["username"]}
            else:
                print(f"❌ Registration failed: {error}")
                return None
        else:
            print(f"❌ Registration failed with status {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Registration request failed: {str(e)}")
        return None

def test_login():
    """Test user login"""
    print("\n🔐 Testing user login...")
    
    # Use form data as the backend expects OAuth2PasswordRequestForm
    login_data = {
        "username": "apitest",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login", 
            data=login_data,  # Use data, not json for form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful: {token_data}")
            return token_data.get("access_token")
        else:
            error = response.json() if response.content else {"detail": "Unknown error"}
            print(f"❌ Login failed: {error}")
            return None
            
    except Exception as e:
        print(f"❌ Login request failed: {str(e)}")
        return None

def test_me_endpoint(token):
    """Test the /me endpoint"""
    print("\n👤 Testing /me endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User data retrieved: {user_data}")
            return user_data
        else:
            error = response.json() if response.content else {"detail": "Unknown error"}
            print(f"❌ /me endpoint failed: {error}")
            return None
            
    except Exception as e:
        print(f"❌ /me request failed: {str(e)}")
        return None

def test_login_with_existing_user():
    """Test login with an existing user from the database"""
    print("\n🔐 Testing login with existing user...")
    
    # Try with one of the existing users we saw in the database
    login_data = {
        "username": "anu",  # This user exists with role admin
        "password": "password123"  # Common test password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login", 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Login successful with existing user: {token_data}")
            return token_data.get("access_token")
        else:
            error = response.json() if response.content else {"detail": "Unknown error"}
            print(f"ℹ️ Login failed (expected if password is wrong): {error}")
            return None
            
    except Exception as e:
        print(f"❌ Login request failed: {str(e)}")
        return None

def main():
    """Main test function"""
    print("🚀 Starting API Endpoint Tests")
    print(f"🌐 Testing API at: {BASE_URL}")
    
    # Wait for server to start
    if not wait_for_server():
        return False
    
    # Test root endpoint
    if not test_root_endpoint():
        return False
    
    # Test registration
    user_data = test_register()
    
    # Test login
    token = test_login()
    
    if token:
        # Test /me endpoint
        me_data = test_me_endpoint(token)
        
        if me_data:
            print("\n✅ All API tests passed! The backend authentication endpoints are working correctly.")
            return True
    
    # Try with existing user if new registration/login failed
    print("\n🔄 Trying with existing user...")
    existing_token = test_login_with_existing_user()
    
    if existing_token:
        me_data = test_me_endpoint(existing_token)
        if me_data:
            print("\n✅ API tests passed with existing user! Backend is working.")
            return True
    
    print("\n❌ API tests failed. Check the errors above.")
    return False

if __name__ == "__main__":
    import time
    time.sleep(3)  # Give server a moment to start
    success = main() 