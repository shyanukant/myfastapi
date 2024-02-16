from fastapi import  Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .database import  get_db
from . import models, schemas

router = APIRouter(
    prefix='posts',
    tags='Posts'
)

@router.post('/create', response_model=schemas.PostRespone)
async def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/', response_model=List[schemas.PostRespone])
async def get_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not exists")
    return posts

@router.get('/{id}', response_model=schemas.PostRespone)
async def get_post_by_id(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return post

@router.delete('/{id}')
async def delete_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schemas.PostRespone)
async def update_post(id: int, updated_post:schemas.PostCreate, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()