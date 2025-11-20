"""
Test script to verify backend setup
"""
import sys
import os

print("🔍 Testing Meta Ads Analyzer Backend Setup...")
print("=" * 60)

# Test 1: Python version
print(f"\n✓ Python version: {sys.version}")

# Test 2: Check imports
print("\n📦 Testing imports...")
try:
    from flask import Flask
    print("  ✓ Flask installed")
except ImportError as e:
    print(f"  ✗ Flask not installed: {e}")
    sys.exit(1)

try:
    from flask_sqlalchemy import SQLAlchemy
    print("  ✓ Flask-SQLAlchemy installed")
except ImportError as e:
    print(f"  ✗ Flask-SQLAlchemy not installed: {e}")
    sys.exit(1)

try:
    import bcrypt
    print("  ✓ bcrypt installed")
except ImportError as e:
    print(f"  ✗ bcrypt not installed: {e}")
    sys.exit(1)

try:
    import jwt
    print("  ✓ PyJWT installed")
except ImportError as e:
    print(f"  ✗ PyJWT not installed: {e}")
    sys.exit(1)

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    print("  ✓ cryptography installed")
except ImportError as e:
    print(f"  ✗ cryptography not installed: {e}")
    sys.exit(1)

try:
    import openai
    print("  ✓ openai installed")
except ImportError as e:
    print(f"  ✗ openai not installed: {e}")
    sys.exit(1)

# Test 3: Check .env file
print("\n🔐 Testing environment configuration...")
from dotenv import load_dotenv
load_dotenv()

env_vars = [
    'FLASK_SECRET_KEY',
    'JWT_SECRET',
    'ENCRYPTION_SECRET',
]

for var in env_vars:
    value = os.getenv(var)
    if value and value != f'your-{var.lower().replace("_", "-")}':
        print(f"  ✓ {var} is set")
    else:
        print(f"  ⚠ {var} is using default/example value (should be changed)")

# Test 4: Create app and database
print("\n🗄️  Testing database setup...")
try:
    from app import create_app
    from app.database import db

    app = create_app()

    with app.app_context():
        # Try to create all tables
        db.create_all()
        print("  ✓ Database tables created successfully")

        # Test User model
        from app.models.user import User
        import uuid

        # Create a test user
        test_user = User(
            id=str(uuid.uuid4()),
            email='test@example.com'
        )
        test_user.set_password('testpassword123')

        print("  ✓ User model works")
        print(f"    - Password hashing: {len(test_user.password_hash)} chars")
        print(f"    - Password check: {test_user.check_password('testpassword123')}")

except Exception as e:
    print(f"  ✗ Database setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test encryption
print("\n🔒 Testing encryption...")
try:
    from app.utils.encryption import encrypt_token, decrypt_token

    test_token = "test_access_token_12345"
    encrypted = encrypt_token(test_token)
    decrypted = decrypt_token(encrypted)

    if decrypted == test_token:
        print("  ✓ Encryption/decryption works")
    else:
        print(f"  ✗ Encryption failed: {test_token} != {decrypted}")

except Exception as e:
    print(f"  ✗ Encryption test failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Test JWT
print("\n🎫 Testing JWT...")
try:
    from app.utils.jwt_helper import generate_token, verify_token

    token = generate_token('user123', 'test@example.com')
    payload = verify_token(token)

    if payload and payload['user_id'] == 'user123':
        print("  ✓ JWT generation and verification works")
    else:
        print("  ✗ JWT verification failed")

except Exception as e:
    print(f"  ✗ JWT test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ Backend setup test complete!")
print("\nYou can now run: python run.py")
