import os
from cryptography.fernet import Fernet
from celery import Celery
import src

def get_fernet_key() -> Fernet: 
    key = os.getenv('FERNET_KEY')
    
    if key:
        fernet = Fernet(eval(key))
        return fernet
    else:
        return "Encrpytion Key not found"


#Excluded paths for Middleware
excluded_endpoints = [
    '/auth/v1/register/',
    '/auth/v1/login/',
    '/auth/v1/getAccessToken/'
]



