from sqlalchemy.orm import Session
from models.UserModel import User

class UserDataLayer:
    def getUser(self, db: Session, params: dict):
        return db.query(User).filter_by(**params).first()

    def getUsers(self, db: Session):
        return db.query(User).all()

    def createUser(self, db: Session, params: dict):
        userModel = User(**params)
        db.add(userModel)
        db.commit()
        db.refresh(userModel)
        return userModel