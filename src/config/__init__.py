import os
from cryptography.fernet import  Fernet


def get_fernet_key():
    key = eval(os.getenv('FERNET_KEY'))
    fernet = Fernet(key)

    return fernet