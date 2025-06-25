# Contact Nest

This document explains the JWT (JSON Web Token) authentication system implemented in the ContactNest API.

## Overview

The JWT authentication system provides secure, stateless authentication for the ContactNest API. It includes:

- User registration and authentication
- JWT token generation and validation
- Role-based access control (RBAC)
- Protected endpoints for both users and contacts
- Token expiration and refresh capabilities

## Architecture

### Components

1. **Authentication Utilities** (`app/utils/auth.py`)
   - Password hashing and verification
   - JWT token creation and validation
   - User role definitions

2. **User Service** (`app/application_services/users/users.py`)
   - User CRUD operations
   - Authentication logic
   - JWT dependency injection functions

3. **API Endpoints** (`app/api/`)
   - Protected endpoints with JWT authentication
   - Role-based access control
   - Public endpoints (registration, login)

## JWT Token Structure

### Token Payload
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "user|admin",
  "exp": "expiration_timestamp"
}
```

### Token Response
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

## API Endpoints

### Public Endpoints (No Authentication Required)

#### Register User
```http
POST /users/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "user"
}
```

#### Authenticate User
```http
POST /users/auth
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Protected Endpoints (Authentication Required)

All protected endpoints require the `Authorization` header:
```http
Authorization: Bearer <jwt_token>
```

#### User Endpoints

- `GET /users/me/profile` - Get current user's profile
- `GET /users/{user_id}` - Get user by ID (own profile or admin)
- `PUT /users/{user_id}` - Update user (own profile or admin)
- `DELETE /users/{user_id}` - Delete user (admin only)
- `GET /users/` - Get all users (admin only)
- `GET /users/search?query=john` - Search users (admin only)

#### Contact Endpoints

- `POST /contacts/` - Create new contact
- `GET /contacts/` - List all contacts
- `GET /contacts/{contact_id}` - Get contact details
- `PUT /contacts/{contact_id}` - Update contact
- `DELETE /contacts/{contact_id}` - Delete contact
- `GET /contacts/search?query=john` - Search contacts

## Role-Based Access Control

### User Roles

1. **User** (`user`)
   - Can access their own profile
   - Can manage their own contacts
   - Cannot access other users' data
   - Cannot access admin endpoints

2. **Admin** (`admin`)
   - Can access all user data
   - Can manage all contacts
   - Can access admin-only endpoints
   - Can delete users

### Access Control Logic

```python
# Users can only access their own data unless they're admin
if current_user.role != "admin" and current_user.id != user_id:
    raise HTTPException(status_code=403, detail="Not enough permissions")
```

## Security Features

### Password Security
- Passwords are hashed using bcrypt
- Salt is automatically generated
- Secure password verification

### JWT Security
- Tokens expire after 60 minutes (configurable)
- Uses HS256 algorithm for signing
- Secret key is configurable via environment variable
- Token validation includes expiration check

### Database Security
- Soft deletion (users marked as inactive)
- Active user filtering
- SQL injection protection via SQLAlchemy ORM

## Environment Configuration

### Required Environment Variables

```bash
# JWT Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=contactnest
```

### Default Values
- `SECRET_KEY`: Default development key (change in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 60 minutes
- `ALGORITHM`: HS256

## Usage Examples

### Python Requests

```python
import requests

# 1. Register a user
register_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "user"
}
response = requests.post("http://localhost:8000/users/register", json=register_data)

# 2. Authenticate and get token
auth_data = {
    "email": "john@example.com",
    "password": "securepassword123"
}
response = requests.post("http://localhost:8000/users/auth", json=auth_data)
token = response.json()["access_token"]

# 3. Use token for protected endpoints
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/users/me/profile", headers=headers)
```

### cURL Examples

```bash
# Register user
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john@example.com","password":"securepassword123","role":"user"}'

# Authenticate
curl -X POST "http://localhost:8000/users/auth" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"securepassword123"}'

# Use token
curl -X GET "http://localhost:8000/users/me/profile" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

#### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

#### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### Token Errors

- **Expired Token**: `"Token has expired"`
- **Invalid Token**: `"Invalid token"`
- **Missing Token**: `"Could not validate credentials"`

## Testing

Run the test script to verify JWT functionality:

```bash
python test_jwt_auth.py
```

This script will:
1. Register a test user
2. Authenticate and get a JWT token
3. Test protected endpoints
4. Test admin functionality
5. Verify error handling

## Best Practices

### Security
1. **Change the default SECRET_KEY** in production
2. **Use HTTPS** in production environments
3. **Implement token refresh** for long-running sessions
4. **Log authentication attempts** for security monitoring
5. **Rate limit authentication endpoints** to prevent brute force attacks

### Development
1. **Use environment variables** for configuration
2. **Test all role combinations** thoroughly
3. **Validate input data** at all layers
4. **Handle errors gracefully** with appropriate HTTP status codes
5. **Document API endpoints** with proper descriptions

### Production Deployment
1. **Use a strong SECRET_KEY** (32+ characters, random)
2. **Set appropriate token expiration** times
3. **Monitor token usage** and implement refresh tokens if needed
4. **Implement proper logging** for security events
5. **Use a reverse proxy** (nginx) for additional security

## Troubleshooting

### Common Issues

1. **Token Expired**: Re-authenticate to get a new token
2. **Invalid Token**: Check token format and signature
3. **Permission Denied**: Verify user role and access rights
4. **Database Connection**: Check database configuration

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export LOG_LEVEL=DEBUG
```

This will provide detailed information about JWT token processing and authentication attempts. 