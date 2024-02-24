from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
# from ..schemas import UserLogin
from ..models import User
from ..utils import verify_password
from ..oauth2 import create_access_token
from app.schemas import Token

router = APIRouter(
    tags=["Authentications"]
)
# This route is used to login a user with email and password and return a token to access other routes which are protected by token
@router.post('/login', response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create token
    access_token = create_access_token(data={"user_id": user.id})
    return Token(access_token=access_token, token_type="bearer")