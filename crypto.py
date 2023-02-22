import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_master_key(master_password, salt):
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, 48000)
    master_password = master_password.encode("utf-8")
    master_key = kdf.derive(master_password)
    master_key = base64.urlsafe_b64encode(master_key)
    return master_key

def fernet_encrypt(password, master_password, salt):
    master_key = generate_master_key(master_password, salt)
    f = Fernet(master_key)
    token = f.encrypt(password)
    return token


def fernet_decrypt(token, master_password, salt):
    master_key = generate_master_key(master_password, salt)
    f = Fernet(master_key)
    decrypted = f.decrypt(token)
    return decrypted
