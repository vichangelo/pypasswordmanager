import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = b'?\t^\xb2\x056o\x0f\x1f\x02"\r\x1e\x94\xdd\'\xa9\x17v\xa6\x13/o(\x1d\xc6o\x9a\xf0X\xc4\xab'

def generate_master_key(master_password):
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, 1000)
    master_password = master_password.encode("utf-8")
    master_key = kdf.derive(master_password)
    return master_key

def verify_master_key(input_key, stored_key):
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, 1000)
    return kdf.verify(input_key, stored_key)
