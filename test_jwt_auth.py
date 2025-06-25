#!/usr/bin/env python3
"""
Test script to demonstrate JWT authentication with the ContactNest API
"""

import requests
import json

# API base URL - adjust this to match your server
BASE_URL = "http://localhost:8000"

def test_jwt_authentication():
    """Test the complete JWT authentication flow"""
    
    print("=== ContactNest JWT Authentication Test ===\n")
    
    # 1. Register a new user
    print("1. Registering a new user...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=register_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ User registered successfully: {user['username']}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # 2. Authenticate and get JWT token
    print("\n2. Authenticating user...")
    auth_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/auth", json=auth_data)
        if response.status_code == 200:
            auth_response = response.json()
            token = auth_response['access_token']
            print(f"✅ Authentication successful!")
            print(f"   Token: {token[:50]}...")
            print(f"   User: {auth_response['user']['username']}")
        else:
            print(f"❌ Authentication failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return
    
    # 3. Test protected endpoint with JWT token
    print("\n3. Testing protected endpoint...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profile retrieved successfully!")
            print(f"   Username: {profile['username']}")
            print(f"   Email: {profile['email']}")
            print(f"   Role: {profile['role']}")
        else:
            print(f"❌ Profile retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Profile retrieval error: {e}")
    
    # 4. Test contacts endpoint with JWT token
    print("\n4. Testing contacts endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/", headers=headers)
        if response.status_code == 200:
            contacts = response.json()
            print(f"✅ Contacts retrieved successfully!")
            print(f"   Number of contacts: {len(contacts)}")
        else:
            print(f"❌ Contacts retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Contacts retrieval error: {e}")
    
    # 5. Test without JWT token (should fail)
    print("\n5. Testing endpoint without JWT token...")
    try:
        response = requests.get(f"{BASE_URL}/users/me/profile")
        if response.status_code == 401:
            print("✅ Correctly rejected request without token")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n=== Test completed ===")

def test_admin_flow():
    """Test admin user creation and admin-only endpoints"""
    
    print("\n=== Admin User Test ===\n")
    
    # 1. Register an admin user
    print("1. Registering an admin user...")
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "adminpassword123",
        "role": "admin"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=admin_data)
        if response.status_code == 201:
            admin = response.json()
            print(f"✅ Admin user registered: {admin['username']}")
        else:
            print(f"❌ Admin registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Admin registration error: {e}")
        return
    
    # 2. Authenticate admin
    print("\n2. Authenticating admin...")
    auth_data = {
        "email": "admin@example.com",
        "password": "adminpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/auth", json=auth_data)
        if response.status_code == 200:
            auth_response = response.json()
            admin_token = auth_response['access_token']
            print(f"✅ Admin authenticated!")
        else:
            print(f"❌ Admin authentication failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Admin authentication error: {e}")
        return
    
    # 3. Test admin-only endpoint
    print("\n3. Testing admin-only endpoint...")
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Admin can access all users!")
            print(f"   Number of users: {len(users)}")
        else:
            print(f"❌ Admin access failed: {response.text}")
    except Exception as e:
        print(f"❌ Admin access error: {e}")

if __name__ == "__main__":
    test_jwt_authentication()
    test_admin_flow() 