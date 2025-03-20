from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, Base
from sqlalchemy import Column, Integer, String

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Therapist model
class Therapist(Base):
    __tablename__ = "therapists"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    specialty = Column(String, nullable=True)
    location = Column(String, nullable=True)

# Pydantic schemas
class TherapistCreate(BaseModel):
    username: str
    email: str
    password: str

class TherapistResponse(BaseModel):
    id: int
    username: str
    email: str
    name: str | None = None
    bio: str | None = None
    specialty: str | None = None
    location: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_therapist(db: Session, username: str, password: str):
    therapist = db.query(Therapist).filter(Therapist.username == username).first()
    if not therapist or not verify_password(password, therapist.hashed_password):
        return None
    return therapist
