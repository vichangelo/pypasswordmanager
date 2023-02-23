"""Cryptography module for pypasswordmanager.

Imports
-------
:mod:`base64`: for safer encoding of master key during program runs.

:class:`Fernet`: for encryption and decryption of passwords.

:mod:`hashes`: for access to hashing functions.

:class:`PBKDF2HMAC`: for generating a master key.

Functions
---------
:func:`generate_master_key`: for generating a master key from a master
password.

:func:`fernet_encrypt`: for encrypting a password.

:func:`fernet_decrypt`: for decrypting a password.
"""
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_master_key(master_password, salt):
    """Generate a master key to be temporarily used by other functions.

    Instantiates a PBKDF2HMAC object using secure hash function SHA256
    and 48000 iterations of the algorithm, then encodes master password
    to UTF-8 so it is bytes-like, generates the key, encodes it to
    url-safe format using ``base64.urlsafe_b64encode`` and returns it.

    :return: safe master key to be used in encryption and decryption.
    :rtype: bytes
    """
    kdf = PBKDF2HMAC(hashes.SHA256, 32, salt, 48000)
    master_password = master_password.encode("utf-8")
    master_key = kdf.derive(master_password)
    master_key = base64.urlsafe_b64encode(master_key)
    return master_key

def fernet_encrypt(password, master_password, salt):
    """Uses Fernet object to encrypt a password"""
    master_key = generate_master_key(master_password, salt)
    f = Fernet(master_key)
    token = f.encrypt(password)
    return token


def fernet_decrypt(token, master_password, salt):
    """Uses Fernet object to decrypt a password."""
    master_key = generate_master_key(master_password, salt)
    f = Fernet(master_key)
    decrypted = f.decrypt(token)
    return decrypted
