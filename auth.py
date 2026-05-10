from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# bcrypt is the hashing algorithm — intentionally slow to prevent brute force attacks
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# reads the Authorization header from incoming requests
oauth2_scheme = HTTPBearer()

def hash_password(password: str):
    # never store plain text passwords — always hash before saving to database
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    # hashes the plain password and compares to stored hash — never compares plain text
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    # copy to avoid modifying the original dictionary
    to_encode = data.copy()

    # token expires 30 minutes from now
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        # sub is standard JWT convention for the subject (who the token belongs to)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        # catches both expired tokens and tampered tokens
        raise HTTPException(status_code=401, detail="Invalid token")