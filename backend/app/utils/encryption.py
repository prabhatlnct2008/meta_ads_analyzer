import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

def get_encryption_key():
    """Get or generate encryption key from environment"""
    secret = os.getenv('ENCRYPTION_SECRET', 'default-secret-key-change-in-production')
    salt = b'meta_ads_analyzer_salt'  # In production, use a random salt stored separately

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    return key

def encrypt_token(token):
    """Encrypt a token for storage"""
    if not token:
        return None

    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(token.encode())
    return encrypted.decode()

def decrypt_token(encrypted_token):
    """Decrypt a stored token"""
    if not encrypted_token:
        return None

    try:
        f = Fernet(get_encryption_key())
        decrypted = f.decrypt(encrypted_token.encode())
        return decrypted.decode()
    except Exception as e:
        print(f"Error decrypting token: {e}")
        return None
