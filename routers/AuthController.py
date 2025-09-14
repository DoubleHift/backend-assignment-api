from fastapi import HTTPException
from core.Exceptions import CustomException
from requestModels.AuthRequestModels import Signup, Login
from services.UserService import UserService


class AuthController:
    def login(user: Login):
        if not user.email:
            raise HTTPException(status_code=400, detail="Please enter your email")
        if not user.password:
            raise HTTPException(status_code=400, detail="Please enter your password")
        try:
            userService = UserService()
            return userService.login(user.email, user.password)
        except CustomException as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as d:
            raise d
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def signup(user: Signup):
        if not user.email:
            raise HTTPException(status_code=400, detail="Please enter your email")
        if not user.password:
            raise HTTPException(status_code=400, detail="Please enter your password")
        try:
            userService = UserService()
            return userService.signup(user.email, user.password)
        except CustomException as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
        except Exception as d:
            raise d
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")
