#!/usr/bin/env python3
"""
Debug script to test JWT authentication step by step
"""

import requests
import json
import jwt
import os
from datetime import datetime, timedelta, timezone

# API base URL
BASE_URL = "http://localhost:8000"

# JWT Configuration (should match your server)
SECRET_KEY = "a4f1d7fb6fe5183dea6ced6ba9c26bbf0d462b28412c005a6ced25cf42a596f6"
ALGORITHM = "HS256"

def test_jwt_creation():
    """Test JWT token creation manually"""
    print("=== Testing JWT Token Creation ===\n")
    
    # Test payload
    payload = {
        "sub": 1,
        "email": "test@example.com",
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60)
    }
    
    try:
        # Create token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print(f"✅ Token created successfully: {token[:50]}...")
        
        # Decode token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Token decoded successfully: {decoded}")
        
        return token
    except Exception as e:
        print(f"❌ JWT creation/decoding failed: {e}")
        return None

def test_user_registration():
    """Test user registration"""
    print("\n=== Testing User Registration ===\n")
    
    register_data = {
        "username": "debuguser",
        "email": "debug@example.com",
        "password": "debugpassword123",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            user = response.json()
            print(f"✅ User registered: {user['username']}")
            return user
        else:
            print(f"❌ Registration failed")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_user_authentication():
    """Test user authentication"""
    print("\n=== Testing User Authentication ===\n")
    
    auth_data = {
        "email": "debug@example.com",
        "password": "debugpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/auth", json=auth_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            auth_response = response.json()
            token = auth_response['access_token']
            print(f"✅ Authentication successful!")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Authentication failed")
            return None
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with token"""
    print("\n=== Testing Protected Endpoint ===\n")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Protected endpoint accessed successfully!")
            print(f"   Username: {profile['username']}")
            return True
        else:
            print(f"❌ Protected endpoint access failed")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def test_invalid_token():
    """Test with invalid token"""
    print("\n=== Testing Invalid Token ===\n")
    
    headers = {
        "Authorization": "Bearer invalid_token_here",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ Correctly rejected invalid token")
            return True
        else:
            print(f"❌ Unexpected response for invalid token")
            return False
    except Exception as e:
        print(f"❌ Invalid token test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 JWT Authentication Debug Script\n")
    
    # Test 1: JWT creation
    test_jwt_creation()
    
    # Test 2: User registration
    user = test_user_registration()
    
    # Test 3: User authentication
    token = test_user_authentication()
    
    # Test 4: Protected endpoint
    if token:
        test_protected_endpoint(token)
    
    # Test 5: Invalid token
    test_invalid_token()
    
    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    main() 