from cryptography.fernet import Fernet
import base64
import os

key = Fernet.generate_key()
encryption_key = base64.urlsafe_b64encode(key).decode()
print(encryption_key)
