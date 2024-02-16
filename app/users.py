from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .utils import hash_password
from .database import get_db
from . import models, schemas

router = APIRouter(
    prefix='/users',
    tags="Users"
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', status_code=status.HTTP_404_NOT_FOUND, response_model=schemas.UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user