from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = 'djfkjeifjidkfdknnnmnv,mdlkfjekjiojikfndfojoirieeuriueijfkdnfkdsjjf'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_at = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_at