from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.schemas import TokenData
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = 'djfkjeifjidkfdknnnmnv,mdlkfjekjiojikfndfojoirieeuriueijfkdnfkdsjjf'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_at = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_at

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, credentials_exception)