from fastapi import  Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from ..utils import hash_password
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse
from ..oauth2 import get_current_user


router = APIRouter(
    prefix='/users',
    tags=["Users"]
)
# This route is used to create a new user and add to the database
@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db:Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Phone number already exists")
    return new_user

# This route is used to get all users
@router.get('/', status_code=status.HTTP_200_OK, 
            response_model=List[UserResponse])
async def get_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not exists")
    return users

# This route is used to get a user by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user

# This route is used to delete a user by id and only owner of the user can delete the user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete this user")
    user_query = db.query(User).filter(User.id==id)
    if not user_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    user_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"User {id} deleted successfully"}

# This route is used to update a user by id and only owner of the user can update the user
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(id:int, updated_user:UserCreate, db:Session = Depends(get_db), 
                      current_user: User = Depends(get_current_user)):
    if current_user.id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to update this user")
    user_query = db.query(User).filter(User.id==id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    try:
        user_query.update(updated_user.model_dump(), synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Phone number already exists")
    return user_query.first()