from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.Database import get_db
from core.config import settings
from dataLayers.UserDataLayer import UserDataLayer
from models.UserModel import User

bearer_scheme = HTTPBearer()

class UserService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    userDataLayer = UserDataLayer()

    def verifyPassword(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def getPasswordHash(self, password):
        return self.pwd_context.hash(password)

    def createAccessToken(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        currentDateTime = datetime.now(timezone.utc)
        if expires_delta:
            expire = currentDateTime + expires_delta
        else:
            expire = currentDateTime + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def login(self, db: Session, email, password):
        registeredUser = self.userDataLayer.getUser(db, {"email": email})
        if not registeredUser or not self.verifyPassword(password, registeredUser.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.createAccessToken(data={"sub": registeredUser.email})
        return {"access_token": access_token, "token_type": "bearer"}

    def signup(self, db: Session, email, password):
        isRegisteredUser = self.userDataLayer.getUser(db, {"email": email})
        if isRegisteredUser:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = self.getPasswordHash(password)
        all_users = self.userDataLayer.getUsers(db)
        is_first_user = not all_users
        
        user_data = {"email": email, "hashed_password": hashed_password, "is_admin": is_first_user}
        self.userDataLayer.createUser(db, user_data)
        
        access_token = self.createAccessToken(data={"sub": email})
        return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = UserDataLayer().getUser(db, {"email": email})
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user