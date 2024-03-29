from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.schemas import TokenData
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .models import User
from .database import get_db
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# This function is used to create a token with user_id and expire time
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_at = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_at

# This function is used to verify the token and return the user_id
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception
    
# This function is used to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User authentication failed")
    return user