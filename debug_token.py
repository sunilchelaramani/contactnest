#!/usr/bin/env python3
"""
Detailed JWT token debugging script
"""

import requests
import json
import jwt
import base64

# API base URL
BASE_URL = "http://localhost:8000"

# JWT Configuration
SECRET_KEY = "a4f1d7fb6fe5183dea6ced6ba9c26bbf0d462b28412c005a6ced25cf42a596f6"
ALGORITHM = "HS256"

def decode_jwt_parts(token):
    """Decode JWT token parts without verification"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            print("❌ Invalid JWT format (should have 3 parts)")
            return None
        
        header = json.loads(base64.urlsafe_b64decode(parts[0] + '==').decode('utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8'))
        
        print(f"Header: {json.dumps(header, indent=2)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        return header, payload
    except Exception as e:
        print(f"❌ Error decoding JWT parts: {e}")
        return None

def test_token_validation():
    """Test token validation step by step"""
    print("=== Testing Token Validation ===\n")
    
    # 1. Get a fresh token
    auth_data = {
        "email": "debug@example.com",
        "password": "debugpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/auth", json=auth_data)
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.text}")
            return
        
        auth_response = response.json()
        token = auth_response['access_token']
        print(f"✅ Got token: {token[:50]}...")
        
        # 2. Decode token parts
        print("\n--- Token Structure ---")
        result = decode_jwt_parts(token)
        if not result:
            return
        
        header, payload = result
        
        # 3. Test manual validation
        print("\n--- Manual Validation ---")
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"✅ Manual validation successful: {decoded}")
        except jwt.ExpiredSignatureError:
            print("❌ Token has expired")
        except jwt.InvalidTokenError as e:
            print(f"❌ Invalid token: {e}")
        except Exception as e:
            print(f"❌ Validation error: {e}")
        
        # 4. Test API validation
        print("\n--- API Validation ---")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ API validation successful!")
        else:
            print("❌ API validation failed")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_token_with_different_formats():
    """Test token with different formats"""
    print("\n=== Testing Different Token Formats ===\n")
    
    # Get a valid token
    auth_data = {
        "email": "debug@example.com",
        "password": "debugpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/auth", json=auth_data)
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.text}")
            return
        
        token = response.json()['access_token']
        
        # Test 1: Valid token
        print("1. Testing valid token...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # Test 2: Token without Bearer prefix
        print("2. Testing token without Bearer...")
        headers = {"Authorization": token}
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # Test 3: Token with extra spaces
        print("3. Testing token with extra spaces...")
        headers = {"Authorization": f"Bearer  {token}  "}
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # Test 4: Token in different header case
        print("4. Testing different header case...")
        headers = {"authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/users/me/profile", headers=headers)
        print(f"   Status: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    print("🔍 Detailed JWT Token Debug\n")
    test_token_validation()
    test_token_with_different_formats() 