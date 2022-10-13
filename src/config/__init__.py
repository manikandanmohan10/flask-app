import os
from cryptography.fernet import Fernet


def get_fernet_key() -> Fernet: 
    key = os.getenv('FERNET_KEY1')
    if key:
        fernet = Fernet(eval(key))
        return fernet
    else:
        return "Encrpytion Key not found"