from passlib.context import CryptContext
pwd_cntx= CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password: str):
    return pwd_cntx.hash(password)

def verify(plain_pass, hash_pass):
    return pwd_cntx.verify(plain_pass, hash_pass)