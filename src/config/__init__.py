import os
from cryptography.fernet import Fernet


def get_fernet_key() -> Fernet: 
    key = os.getenv('FERNET_KEY')
    
    if key:
        fernet = Fernet(eval(key))
        return fernet
    else:
        return "Encrpytion Key not found"


#Excluded paths for Middleware
excluded_endpoints = [
    '/wtf/',
    '/auth/v1/register/',
    '/auth/v1/login/',
    '/auth/v1/getAccessToken/',
    '/todo/'
]
