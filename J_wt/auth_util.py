from warnings import deprecated
from passlib import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRETE_KEY= 'Hacke?@$+#333'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFECYCLE=30

pwd_context = CryptContext(schemes=['bycrypt'], deprecated='auto')

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow()+(expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFECYCLE))
    to_encode.update({'exp': expire})