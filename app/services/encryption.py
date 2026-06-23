# app/services/encryption.py
from cryptography.fernet import Fernet

# Esta llave debe estar en tu .env (nunca hardcodeada)
key = Fernet.generate_key() 
cipher_suite = Fernet(key)

def encrypt_message(message: str) -> bytes:
    return cipher_suite.encrypt(message.encode())

def decrypt_message(encrypted_message: bytes) -> str:
    return cipher_suite.decrypt(encrypted_message).decode()
