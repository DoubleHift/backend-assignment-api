from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.UserService import UserService
from core.Database import get_db
import requestModels.AuthRequestModels as schemas

router = APIRouter(tags=["Authentication"])
user_service = UserService()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: schemas.Signup, db: Session = Depends(get_db)):
    return user_service.signup(db, email=user_data.email, password=user_data.password)

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm, email yerine 'username' alanı bekler.
    return user_service.login(db, email=form_data.username, password=form_data.password)