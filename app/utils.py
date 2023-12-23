from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashfunc(passw: str):
    return pwd_context.hash(passw)

def verify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)